#= require <model.coffee>
#= require <sound_controller.coffee>
#= require <global.coffee>
#= require <util.coffee>
#= require <voices_lists.coffee>

TweetController =
	_tLists: {
		mixed: []
		poli: []
	}

	_archive: []
	_archiveThreshold: 10000
	_timeTravelId: -1
	_archiveRoot: $('#archive-container')
	_batch:
		duration: 10 * 1000
		interval: 5 * 1000
		size: 10
	_threshold: 8

	_ALL_TWEETS: false

	init: ->
		@_initSwitches()
		@_initTimeTravel()
		new Connector(Connector.config.tweetsQueue, (data) -> TweetController.consume(data))

	_initTimeTravel: ->
		$('#play-tweets-1-button').click(() -> TweetController._timeTravel(1))
		$('#play-tweets-6-button').click(() -> TweetController._timeTravel(6))
		$('#play-tweets-24-button').click(() -> TweetController._timeTravel(24))

	_initSwitches: ->
		voicesSwitch = 
			selec: '#voices-switch', 
			dft: true, 
			handlerGen: (obj) ->
				() -> TweetController._toggleBirdSelection(obj)
		leftLabelV = 
			selec: '#voices-switch-label-citizens'
			handlerGen: (obj) ->
				() -> TweetController._selectCitizenBirds(obj)
		rightLabelV = 
			selec: '#voices-switch-label-politicians', 
			handlerGen: (obj) ->
				() -> TweetController._selectPoliBirds(obj)
		@_initSwitch(voicesSwitch, leftLabelV, rightLabelV)
		@_usePoliBirds = true # Put default in class-global scope.

		tweetsSwitch = 
			selec: '#citizen-tweets-switch',
			dft: @_ALL_TWEETS, 
			handlerGen: (obj) ->
				() -> TweetController._toggleShownTweets(obj)
		leftLabelT = 
			selec: '#tweets-switch-label-on', 
			handlerGen: (obj) ->
				() -> TweetController._showPoliTweetsOnly(obj)
		rightLabelT = 
			selec: '#tweets-switch-label-off', 
			handlerGen: (obj) ->
				() -> TweetController._showAllTweets(obj)
		@_initSwitch(tweetsSwitch, leftLabelT, rightLabelT)
		@_poliTweetsOnly = @_ALL_TWEETS # Put default in class-global scope.

	_initSwitch: (switchObj, left, right) ->
		# TODO: DOCUMENTATION
		# switchObj: {selec, dft, handlerGen}
		# 	selec: Selector uniquely identifying the respective switch
		# 	dft: Default value for the switch.
		# 	handlerGen: SwitchObject -> ClickHandler
		# left/right: {selec, handlerGen}
		# 	selec: selector uniquely identifying the switch's left/right label.
		# 	handlerGen: SwitchObject -> ClickHandler
		sw = $(switchObj.selec)
		# Set value to default.
		sw.prop('checked', switchObj.dft)
		# Attach change handler
		sw.change(switchObj.handlerGen(sw))
		# Attach handlers to labels.
		leftObj = $(left.selec)
		leftObj.click (left.handlerGen(sw))
		rightObj = $(right.selec)
		rightObj.click (right.handlerGen(sw))

	# Public
	triggerTweetManually: () ->
		# Debug only
		incoming = [Model.manualTweets[Global.manualTweetID]]
		Global.manualTweetID = (Global.manualTweetID + 1) % Model.manualTweets.length
		@consume(incoming)

	# Public
	translateBirds: () ->
		# Translates all language specific data in the displayed tweets.
		@_updateBirdNames()

	# Public
	showAllTweets: () ->
		# Displays politician tweets as well as citizen user tweets.
		$('#citizen-tweets-switch').prop('checked', @_ALL_TWEETS);
		@_changeShownTweets()

	# Public
	consume: (incomingTweets) ->
		# Consumes an incoming tweets, i.e.
		# a) Archiving them.
		# b) Adding them to the respective tList(s).
		# c) Evicting displayed tweets if necessary.
		# d) Displaying the tweet and playing the sound if the mode is
		# 	 appropriate.

		newMixed = @_transformAll(incomingTweets)
		[newPoli, birdChange] = @_classify(newMixed)

		@_updatePoliBird(tweet.refresh) for tweet in birdChange
		@_addToArchive(tweet) for tweet in newMixed

		# Update tLists
		@_tLists.poli = @_tLists.poli.concat newPoli
		@_tLists.mixed = @_tLists.mixed.concat newMixed
		[evictedPoli, evictedMixed] = @_trimLists()

		# Select and display tweets w.r.t. the set mode.
		if @_poliTweetsOnly
			list = newPoli
			@_removeTweets(evictedPoli)
		else
			list = newMixed
			@_removeTweets(evictedMixed)
		@_displayTweets(list)

		# Play sounds.
		@_playTweets(list, SoundCtrl.getMode())

	# ARCHIVE
	_addToArchive: (entry) ->
		# Adds entry to the archive for the time travel function.
		@_archiveRoot.append entry.obj
		@_archive.push entry
		# Evict far-too-old tweets irreversibly.
		@_removeTweets(@_archive[@_archiveThreshold..])
		@_archive = @_archive[..@_archiveThreshold]

	# USER SETTINGS

	_selectPoliBirds: (switchObj) ->
		switchObj.prop('checked', true)
		@_changeBirdSelection (poliBirds=true)

	_selectCitizenBirds: (switchObj) ->
		switchObj.prop('checked', false)
		@_changeBirdSelection (poliBirds=false)

	_toggleBirdSelection: (switchObj) ->
		mode = $(switchObj).prop('checked')
		@_changeBirdSelection mode

	_changeBirdSelection: (poliBirds) ->
		# Changes display mode: Either only politicians' tweets or all.
		# Notifies the sound controller.
		TweetController._usePoliBirds = poliBirds
		SoundCtrl.setBirdMode(if poliBirds then "P" else "C")
		TweetController._updateBirdNames()
		TweetController._switchView()

	_showAllTweets: (switchObj) ->
		switchObj.prop('checked', true)
		@_changeShownTweets (all=true)

	_showPoliTweetsOnly: (switchObj) ->
		switchObj.prop('checked', false)
		@_changeShownTweets (all=false)

	_toggleShownTweets: (switchObj) ->
		@_changeShownTweets not $(switchObj).prop('checked')

	_changeShownTweets: (all) ->
		# Adapts the list of tweets w.r.t. the selected mode.
		TweetController._poliTweetsOnly = not all
		TweetController._switchView()

	# TIME TRAVEL

	_timeTravel: (timeSpan) ->
		# Starts the time travel, i.e. batches tweets and starts playing
		# tweets of a batch for a fixed amount of time before turning them off
		# again automatically. Batches overlap.
		now = Util.time()
		diff = timeSpan * 60 * 60 * 1000
		thresholdTime = now - diff
		agenda = @_createBatches (tweet) -> tweet.time > thresholdTime
		@_timeTravelId += 1
		@_startPlaybackHandler(@_timeTravelId, agenda)

	_createBatches: (pred) ->
		# Batches the archive in reverse arrival time order until `pred` is 
		# violated once.
		result = []
		batch = []
		for tweet in @_archive
			break unless pred(tweet)
			if batch.length is @_batch.size
				result.push batch
				batch = []
			batch.push tweet
		result.push batch
		return result

	_startPlaybackHandler: (id, agenda) ->
		# Picks the last batch in the agenda-queue and plays all tweets sounds.
		# Waits a fixed amount of time before working the other batches 
		# recursively.

		# If a different time travel has been started in the mean time -> stop
		# starting new tweets. The already playing ones will keep playing.
		return if agenda.length is 0 or @_timeTravelId != id

		[upcoming..., current] = agenda
		tweet.play(SoundCtrl.getMode(), @_batch.duration) for tweet in current
		startNext = () -> TweetController._startPlaybackHandler(id, upcoming)
		setTimeout startNext, @_batch.interval

	_trimLists: () ->
		# selects the last @_threshold elements, returns evicted ones
		numEvictedPoli = Math.max(0, @_tLists.poli.length - @_threshold)
		numEvictedMixed = Math.max(0, @_tLists.mixed.length - @_threshold)
		evictedPoli = @_tLists.poli[...numEvictedPoli]
		evictedMixed = @_tLists.mixed[...numEvictedMixed]
		@_tLists.poli = @_tLists.poli[numEvictedPoli...]
		@_tLists.mixed = @_tLists.mixed[numEvictedMixed...]
		[evictedPoli, evictedMixed]

	_transformAll: (tweets) ->
		# Transforms tweets in the internal representation.
		tweet.time = new Date(parseInt tweet.time) for tweet in tweets
		@_transform(tweet) for tweet in tweets

	_classify: (tweets) ->
		# Returns a list with tweets by politicians and tweets with a change in 
		# bird. Potentially overlapping
		poli = (tweet for tweet in tweets when tweet.bid.poli?)
		birdChange = (tweet for tweet in tweets when tweet.refresh?)
		[poli, birdChange]

	_removeTweets: (tweets) ->
		# Remove tweet objects from DOM.
		tweet.obj.remove() for tweet in tweets

	_updateBirdNames: ->
		# Removes and re-adds the bird name in tweets. Language sensitive.
		for own key, list of TweetController._tLists
			for elem in list
				mode = if TweetController._usePoliBirds then "poli" else "citizen"
				mode = "citizen" unless elem.bid.poli?
				bird = Model.birds[elem.bid[mode]][Util.addLang("name")]
				$("#tweet-#{elem.id}-bird").text(bird)

	_updatePoliBird: (info) ->
		# Applies a change in the politician's bird.
		pid = info.politicianId
		bid = info.birdId
		Model.politicians[pid].self_bird = bid
		VoicesLists.update()

	_switchView: ->
		# Switches view from "politicians only" to "all" or back.
		oldL = if @_poliTweetsOnly then @_tLists.mixed else @_tLists.poli
		newL = if @_poliTweetsOnly then @_tLists.poli else @_tLists.mixed
		tweet.obj.remove() for tweet in oldL
		root = $('#tweet-list')
		root.append tweet.obj for tweet in newL
		@_playTweets(newL, SoundCtrl.getMode())
		@_attachClickHandler tweet for tweet in newL 

	_displayTweets: (tweets) ->
		# Adds `tweets` to the list of displayed birds and attaches the click
		# handler.
		domList = $('#tweet-list')
		for tweet in tweets
			do (tweet) ->
				domList.append tweet.obj
				TweetController._attachClickHandler(tweet)

	_playTweets: (list, mode) ->
		# Plays all passed tweets' sounds in the respective mode.
		tweet.play(mode) for tweet in list

	_transform: (tweet) ->
		# Transforms a tweets from the backend into a tweet in the internal
		# representation including the DOM object.
		choice = if @_usePoliBirds and tweet.poli? then "poli" else "citizen"
		bid = tweet.sound[choice].bid
		sanitized = Util.sanitize(tweet.content, tweet.poli?)
		tags = Util.sanitizeTags tweet.hashtags
		enhanced = @_enhance sanitized, tags

		data = 
			time: Util.transformTime tweet.time
			bird: Model.birds[bid][Util.addLang("name")]
			content: enhanced
			name: tweet.name
			twitterName: tweet.twitterName
			id: tweet.id
			borderColor: tweet.partycolor
			imageSrc: tweet.image
			retweetSrc: if tweet.retweet then Global.basePath + "/images/vogel2.png" else ""
			party: tweet.party

		html = """
<div class="entry" id="tweet-{{id}}">
  <div class="retweet">
    <img src="{{retweetSrc}}"/>
  </div>
  <div class="tweet">

    <div class="top">
      <div class="author-img">
        <img src="{{imageSrc}}" style="border-color: {{borderColor}}"/>
      </div>
      <div class="author-info">
        <div class="name"> {{name}} </div>
        <div class="twitter-name"> @{{twitterName}} </div>
        <div class="party"> {{party}} </div>
      </div>
      <div class="replay">
        <span class="speaker fa fa-play-circle fa-3x" id="tweet-{{id}}-speaker"/>
      </div>
    </div>

    <div class="content">
      {{{content}}}
    </div>

    <div class="footer">
      <span class="time-stamp"> {{time}} </span>
      <span class="bird" id="tweet-{{id}}-bird"> {{bird}} </span>
    </div>

  </div>
</div> 
"""
	
		tweetElement = $(Mustache.render(html, data))

		audioElems = [
			$("<audio id='audio-#{tweet.id}-P' src='#{tweet.sound.poli.natural}'>") if tweet.sound.poli?,
			$("<audio id='audio-#{tweet.id}-C' src='#{tweet.sound.citizen.natural}'>"),
		]

		for audio in audioElems
			tweetElement.append(audio)

		tweetCompound = 
			obj: tweetElement
			play: (mode, duration) -> 
				effectiveDuration = TweetController._getDuration(duration, tweet, mode)
				mode = "C" unless tweet.poli? # there is no P mode for citizens
				SoundCtrl.play(tweet.id, effectiveDuration, mode)
			time: tweet.time
			id: tweet.id
			bid:
				poli: tweet.sound.poli?.bid
				citizen: tweet.sound.citizen.bid

		return tweetCompound

	_enhance: (tweet, hashtags) ->
		# Turns hashtags in the tweet green.
		for hashtag in hashtags
			tweet = tweet.replace('#'+hashtag, "<span style='color: green'>##{hashtag}</span>")
		return tweet

	_getDuration: (suggestion, tweet, mode) ->
		# Computes the play-duration for a tweet. Uses the suggestion if 
		# possible. Otherwise returns the length of the sound referenced by
		# the tweet.
		return suggestion if suggestion?
		return tweet.sound.citizen.duration unless tweet.poli?
		selector = if mode is "P" then "poli" else "citizen"
		tweet.sound[selector].duration

	_attachClickHandler: (tweetCompound) ->
		# Attaches click handler playing the sound to the speaker icon.
		speakerElement = tweetCompound.obj.find("#tweet-#{tweetCompound.id}-speaker")
		speakerElement.click () -> 
			tweetCompound.play(SoundCtrl.getMode())



