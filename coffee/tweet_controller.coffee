#= require <model.coffee>
#= require <sound_controller.coffee>
#= require <global.coffee>
#= require <util.coffee>
#= require <tweet_provider.coffee>

TweetController =
	_tLists: {
		mixed: [undefined, undefined, undefined, undefined, undefined, undefined]
		poli: [undefined, undefined, undefined, undefined, undefined, undefined]
	}

	_archive: []
	_timeTravel: -1
	_timeTravelRoot: $('#time-travel-container')
	_batch:
		duration: 10 * 1000
		intervall: 5 * 1000
		size: 10
	_usePoliBirds: true
	_poliTweetsOnly: true
	_threshold: 6
	_sanityPattern: /\w*/
	_stalled: []

	init: ->
		$('#play-tweets-1-button').click(() -> @_timeTravel(1))
		$('#play-tweets-6-button').click(() -> @_timeTravel(6))
		$('#play-tweets-24-button').click(() -> @_timeTravel(24))

		birdsSwitch = $('#voices-switch')
		tweetsSwitch = $('#citizen-tweets-switch')
		@_usePoliBirds = birdsSwitch.prop('checked')
		@_poliTweetsOnly = tweetsSwitch.prop('checked')

		birdsSwitch.change (-> 
			@_usePoliBirds = birdsSwitch.prop('checked')
			@_changeView()
			)
		tweetsSwitch.change (-> 
			@_poliTweetsOnly = tweetsSwitch.prop('checked')
			@_changeView()
			)
		new TweetProvider(@_consumeTweets)

	# Interface
	triggerTweetManually: () ->
		incoming =  [Model.manualTweets[Global.manualTweetID]]
		Global.manualTweetID = (Global.manualTweetID + 1) % Model.manualTweets.length
		@_consumeTweets(incoming)

	update: () ->
		return unless Display.state is "center" or not Global.stallTweets
		@_consumeTweets(@_stalled)
		@_stalled = []

	# ARCHIVE
	_addToArchive: (tweet) ->
		entry = [tweet.time, a = $("<audio src='#{(if Global.usePoliSounds and tweet.byPoli then tweet.soundp[0] else tweet.soundc[0])}'>")]
		@_archive.push entry

	# TIME TRAVEL

	_timeTravel: (timeSpan) ->
		qualifying = 0
		nowTime = Util.time()
		diff = timeSpan * 60 * 60 * 1000
		for [time, audioObj] in @_archive
			if nowTime - time.getTime() < diff then qualifying += 1 else break 
		maxIndex = qualifying - 1
		agenda = []
		for i in [0..(maxIndex / @_batch.size)] # .. means inclusively
			batch = (audioObj for [time, audioObj] in @_archive[i * @_batch.size ... Math.min((i+1) * @_batch.size, maxIndex+1)])
			agenda.push batch
		id = @_timeTravel + 1
		@_timeTravel = id
		@_startPlaybackHandler(id, agenda)

	_startPlaybackHandler: (id, agenda) ->
		return if agenda.length is 0 or @_timeTravel != id
		[upcoming..., toStart] = agenda
		for audioObj in toStart
			archiveRoot.append(audioObj)
			audioObj[0].play()
		stopCurrent = () -> @_stopPlayback(toStart)
		setTimeout stopCurrent, @_batch.duration
		startNext = () -> @_startPlaybackHandler(id, upcoming)
		setTimeout startNext, @_batch.intervall

	_stopPlayback: (objs) ->
		for obj in objs
			obj.stop()
			obj.remove()

	# CONSUME INCOMING TWEETS

	_consumeTweets: (incomingTweets) ->
		if Display.state isnt "center" and Global.stallTweets
			@_stalled push incomingTweets
		else 
			tweet.time = new Date(parseInt tweet.time) for tweet in incomingTweets
			@_addToArchive(tweet) for tweet in incomingTweets
			newTweets = (@_transform tweet for tweet in incomingTweets)
			for tweet, index in newTweets
				@_tLists.mixed.push tweet # unless tweet.byPoli and Global.poliTweetsOnly
				@_tLists.poli.push tweet if incomingTweets[index].byPoli
			@_updateShownTweets(incomingTweets)

	_changeView: ->
		oldL = @_tLists[if @_poliTweetsOnly then "mixed" else "poli"]
		newL = @_tLists[if @_poliTweetsOnly then "poli" else "mixed"]
		tweet?.remove() for tweet in oldL
		root = $('#tweet-list')
		root.append tweet for tweet in newL
		# The next action is questionable:
		# If the user pushes the button, there should be _some_ auditive feedback.
		# But is playing all sounds on top of everything else the best idea?
		SoundCtrl.turnOnSound (obj.attr('tweetid') for obj in newL when obj?)

	_updateShownTweets: (incomingTweets) ->
		newOnes = 0
		# update poli list
		newOnes += 1 for tweet in incomingTweets when tweet.byPoli
		tweetsToRemove = @_tLists.poli[0..newOnes] if @_poliTweetsOnly
		@_tLists.poli = @_tLists.poli[newOnes..]
		@_tLists.poli  = @_tLists.poli[@_tLists.poli.length - @_threshold..]
		# update mixed list
		newOnes = incomingTweets.length
		tweetsToRemove = @_tLists.mixed[0..newOnes] unless @_poliTweetsOnly
		@_tLists.mixed = @_tLists.mixed[newOnes..]
		@_tLists.mixed = @_tLists.mixed[@_tLists.mixed.length - @_threshold..]

		tweet?.remove() for tweet in tweetsToRemove

		list = $('#tweet-list')
		respectiveList = if @_poliTweetsOnly then @_tLists.poli else @_tLists.mixed
		for tweet in respectiveList
			list.append tweet 

		SoundCtrl.turnOnSound(tweet.id for tweet in incomingTweets)

	_sanitize: (tags) ->
		for tag in tags
			if tag.match @_sanityPattern then tag else "--warning--"

	_appendTweet: (tweet) ->
		$("#tweet-list").append(@_transform tweet)

	_transform: (tweet) ->
		retweetImage = $("<img class='retweet-bird' src='#{Global.basePath}/images/vogel2.png'>") if tweet.retweet
		tweetElement = $("<div id='tweet-#{tweet.id}' class='tweet' tweetid='#{tweet.id}'>")
		soundElementP = $("<audio id='audio-#{tweet.id}-P' src='#{tweet.soundp[0]}' hotlength='#{tweet.soundp[1]}'>") if tweet.soundp?
		soundElementC = $("<audio id='audio-#{tweet.id}-C' src='#{tweet.soundc[0]}' hotlength='#{tweet.soundc[1]}'>")
		tweetProfileInfo = $("<div id='tweet-#{tweet.id}-profile' class='tweet-profile-info'>")
		tweetContent = $("<div id='tweet-#{tweet.id}-content' class='tweet-content'>")
		speakerElement = $("<i class='speaker fa fa-music fa-2x' id='tweet-#{tweet.id}-speaker'>")
		profileImg = $("<img src=#{tweet.image}>")
		profileName = $("<div class='profile-name'>")
		profileName.text(tweet.name)
		twitterName = $("<div class='twitter-name'>")
		tweetText = $("<div class='textfield'>")
		tweetTime = $("<div class='time'>")

		tweetProfileInfo.append(profileImg)
		tweetProfileInfo.append(speakerElement)
		tweetProfileInfo.append(tweetTime)

		tweetContent.append(profileName)
		tweetContent.append(twitterName)
		tweetContent.append(tweetText)

		tweetText.html(@_enhance tweet.content, tweet.hashtags)
		tweetTime.text(Util.transformTime tweet.time)
		twitterName.text("@" + tweet.twitterName)

		tweetElement.append(retweetImage) if tweet.retweet
		tweetElement.append(tweetProfileInfo)
		tweetElement.append(tweetContent)
		tweetElement.append(soundElementP) if soundElementP
		tweetElement.append(soundElementC)

		profileImg.css("border-color", "#{tweet.partycolor}") if tweet.partycolor?
		speakerElement.click( ->
			# see sound_controller
			SoundCtrl.playSound tweet.id
			)	
		return tweetElement

	_enhance: (tweet, hashtags) ->
		return tweet unless hashtags?
		for hashtag in @_sanitize hashtags
			tweet = tweet.replace('#'+hashtag, "<span style='color: blue'>##{hashtag}</span>")
		return tweet






