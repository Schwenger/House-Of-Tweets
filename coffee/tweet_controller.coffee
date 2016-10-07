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
		intervall: 5 * 1000
		size: 10
	_poliTweetsOnly: true
	_threshold: 6
	_sanityPattern: /\w*/

	init: ->
		$('#play-tweets-1-button').click(() -> TweetController._timeTravel(1))
		$('#play-tweets-6-button').click(() -> TweetController._timeTravel(6))
		$('#play-tweets-24-button').click(() -> TweetController._timeTravel(24))
		$('#chirping-of-switch').change(@_changeSoundOrigin)
		$('#voices-switch').change(@_changeBirdSelection)
		$('#citizen-tweets-switch').change(@_changeShownTweets)

		@_poliTweetsOnly = $("citizen-tweets-switch").prop('checked')
		@_usePoliBirds = $("voices-switch").prop('checked')

		new Connector(Connector.config.tweetsQueue, (data) -> TweetController.consume(data))

	# Interface
	triggerTweetManually: () ->
		incoming =  [Model.manualTweets[Global.manualTweetID]]
		Global.manualTweetID = (Global.manualTweetID + 1) % Model.manualTweets.length
		@consume(incoming)

	# ARCHIVE
	_addToArchive: (entry) ->
		@_archiveRoot.append entry.obj
		@_archive.push entry
		@_removeTweets(@_archive[@_archiveThreshold..])
		@_archive = @_archive[..@_archiveThreshold]

	# USER SETTINGS
	_changeSoundOrigin: ->
		bird = $(@).prop('checked')
		SoundCtrl.setSoundMode(if bird then "B" else "M")

	_changeBirdSelection: ->
		poli = $(@).prop('checked')
		TweetController._usePoliBirds = poli
		SoundCtrl.setBirdMode(if poli then "P" else "C")
		for own key, list of TweetController._tLists
			for elem in list
				mode = if poli then "poli" else "citizen"
				bird = Model.birds[elem.bid[mode]][Util.addLang("name")]
				$("#tweet-#{elem.id}-bird").text(bird)

	_changeShownTweets: ->
		TweetController._poliTweetsOnly = $(@).prop('checked')
		TweetController._switchView()

	# TIME TRAVEL

	_timeTravel: (timeSpan) ->
		now = Util.time()
		diff = timeSpan * 60 * 60 * 1000
		thresholdTime = now - diff
		agenda = @_createBatches (tweet) -> tweet.time > thresholdTime
		@_timeTravelId += 1
		@_startPlaybackHandler(@_timeTravelId, agenda)

	_createBatches: (pred) ->
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
		return if agenda.length is 0 or @_timeTravelId != id
		[upcoming..., current] = agenda
		tweet.play(SoundCtrl.getMode(), @_batch.duration) for tweet in current
		startNext = () -> TweetController._startPlaybackHandler(id, upcoming)
		setTimeout startNext, @_batch.intervall

	# CONSUME INCOMING TWEETS

	consume: (incomingTweets) ->
		console.log "Tweets incoming!"
		@_removeTweets(@_tLists.mixed)
		@_removeTweets(@_tLists.poli)

		@_process tweet for tweet in incomingTweets
		@_trimLists()
		
		list = if @_poliTweetsOnly then @_tLists.poli else @_tLists.mixed

		@_displayTweets(list)
		byPoli = Util.count(list, (t) -> t.byPoli) # I miss lazy variables.
		toPlay = if @_poliTweetsOnly then byPoli else incomingTweets.length
		@_playTweets(list[-toPlay...], SoundCtrl.getMode())

	# selects the last @_threshold elements
	_trimLists: () ->
		@_tLists.mixed = @_tLists.mixed[-@_threshold...]
		@_tLists.poli = @_tLists.poli[-@_threshold...]

	_process: (tweet) ->
		tweet.time = new Date(parseInt tweet.time) 
		transformed = @_transform(tweet)
		@_addToArchive(transformed)
		@_updatePoliBird(tweet.refresh) if tweet.refresh?
		@_tLists.mixed.push transformed 
		@_tLists.poli.push transformed if tweet.byPoli

	_updatePoliBird: (info) ->
		pid = info.politicianId
		bid = info.birdId
		Model.politicians[pid].self_bird = bid
		VoicesLists.update()

	_switchView: ->
		oldL = if @_poliTweetsOnly then @_tLists.mixed else @_tLists.poli
		newL = if @_poliTweetsOnly then @_tLists.poli else @_tLists.mixed
		tweet.obj.remove() for tweet in oldL
		root = $('#tweet-list')
		root.append tweet.obj for tweet in newL
		@_playTweets(newL)

	_removeTweets: (tweets) ->
		tweet.obj.remove() for tweet in tweets

	_displayTweets: (tweets) ->
		domList = $('#tweet-list')
		domList.append tweet.obj for tweet in tweets

	_playTweets: (list, mode) ->
		tweet.play(mode) for tweet in list

	_sanitize: (tags) ->
		for tag in tags
			if tag.match @_sanityPattern then tag else "--warning--"

	_transform: (tweet) ->

		choice = if @_usePoliBirds and tweet.poli? then "poli" else "citizen"
		bid = tweet.sound[choice].bid

		data = 
			time: Util.transformTime tweet.time
			bird: Model.birds[bid][Util.addLang("name")]
			content: @_enhance tweet.content, tweet.hashtags
			name: tweet.name
			twitterName: tweet.twitterName
			id: tweet.id
			borderColor: tweet.partycolor
			imageSrc: tweet.image
			retweetSrc: Global.basePath + "/images/vogel2.png"
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
			$("<audio id='audio-#{tweet.id}-PB' src='#{tweet.sound.poli.natural}'>") if tweet.sound.poli?,
			$("<audio id='audio-#{tweet.id}-PM' src='#{tweet.sound.poli.synth}'>") if tweet.sound.poli?,
			$("<audio id='audio-#{tweet.id}-CB' src='#{tweet.sound.citizen.natural}'>"),
			$("<audio id='audio-#{tweet.id}-CM' src='#{tweet.sound.citizen.synth}'>")
		]

		for audio in audioElems
			tweetElement.append(audio)

		tweetCompound = 
			obj: tweetElement
			play: (mode, duration = tweet.sound.duration) -> SoundCtrl.play(tweet.id, duration, mode)
			time: tweet.time
			id: tweet.id
			bid:
				poli: tweet.sound.poli?.bid
				citizen: tweet.sound.citizen.bid

		speakerElement = tweetElement.find("#tweet-#{tweet.id}-speaker")
		speakerElement.click () -> tweetCompound.play(SoundCtrl.getMode())

		return tweetCompound

	_enhance: (tweet, hashtags) ->
		return tweet unless hashtags?
		for hashtag in @_sanitize hashtags
			tweet = tweet.replace('#'+hashtag, "<span style='color: blue'>##{hashtag}</span>")
		return tweet






