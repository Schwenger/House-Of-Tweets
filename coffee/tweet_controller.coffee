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
	_timeTravel: -1
	_timeTravelRoot: $('#time-travel-container')
	_batch:
		duration: 10 * 1000
		intervall: 5 * 1000
		size: 10
	_poliTweetsOnly: true
	_threshold: 6
	_sanityPattern: /\w*/
	_stalled: []

	init: ->
		$('#play-tweets-1-button').click(() -> @_timeTravel(1))
		$('#play-tweets-6-button').click(() -> @_timeTravel(6))
		$('#play-tweets-24-button').click(() -> @_timeTravel(24))
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

	update: () ->
		return if Display.state isnt "center" and Global.stallTweets
		console.log "Consuming stalled tweets"
		@consume(@_stalled)
		@_stalled = []

	# ARCHIVE
	_addToArchive: (entry) ->
		@_archive.push entry
		@_archive = @_archive[..@_archiveThreshold]

	# USER SETTINGS
	_changeSoundOrigin: ->
		bird = $(@).prop('checked')
		SoundCtrl.setSoundMode(if bird then "B" else "M")

	_changeBirdSelection: ->
		poli = $(@).prop('checked')
		SoundCtrl.setBirdMode(if poli then "P" else "C")

	_changeShownTweets: ->
		TweetController._poliTweetsOnly = $(@).prop('checked')
		TweetController._switchView()

	# TIME TRAVEL
	_timeTravel: (timeSpan) ->
		qualifying = 0
		nowTime = Util.time()
		diff = timeSpan * 60 * 60 * 1000
		@_archive.reduce (sum, obj) -> sum + (nowTime - obj.time < diff)
		agenda = _createBatches(@archive[..qualifying])
		id = @_timeTravel + 1
		@_timeTravel = id
		@_startPlaybackHandler(id, agenda)

	_createBatches: (list) ->
		batchCount = list.length + (@_batch.size - 1) / @_batch.size
		return (for i in [0 ... batchCount]
			lb = @_batch.size * i
			up = Math.max(list.length, @_batch.size * (i+1))
			list[lb ... ub])

	_startPlaybackHandler: (id, agenda) ->
		return if agenda.length is 0 or @_timeTravel != id
		[upcoming..., current] = agenda
		for tweet in current
			archiveRoot.append(tweet.obj)
			tweet.play()
		stopCurrent = () -> @_stopPlayback(current)
		setTimeout stopCurrent, @_batch.duration
		startNext = () -> @_startPlaybackHandler(id, upcoming)
		setTimeout startNext, @_batch.intervall

	_stopPlayback: (tweets) ->
		for tweet in tweets
			tweet.stop()
			tweet.obj.remove()

	# CONSUME INCOMING TWEETS

	consume: (incomingTweets) ->
		console.log "Consuming"
		if Display.state isnt "center" and Global.stallTweets
			@_stalled push incomingTweets
		else 
			# remove everything 
			@_removeTweets(@_tLists.mixed)
			@_removeTweets(@_tLists.poli)
			newPoliTweets = incomingTweets.reduce (sum, tweet) -> sum + tweet.byPoli
			newMixedTweets = incomingTweets.length
			# process tweet
			for tweet in incomingTweets
				tweet.time = new Date(parseInt tweet.time) 
				transformed = @_transform(tweet)
				# archive
				@_addToArchive(transformed)
				# handle #houseoftweets
				@_updatePoliBird(tweet.refresh) if tweet.refresh?
				# file by origin
				@_tLists.mixed.push transformed 
				@_tLists.poli.push transformed if tweet.byPoli
			# update current lists
			@_tLists.mixed = @_tLists.mixed[..@_threshold]
			@_tLists.poli = @_tLists.poli[..@_threshold]
			# display and play w.r.t user settings
			list = if @_poliTweetsOnly then @_tLists.poli else @_tLists.mixed
			@_displayTweets(list)
			@_playTweets(@_tLists.poli[..newPoliTweets])

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

	_playTweets: (list) ->
		tweet.play() for tweet in list

	_sanitize: (tags) ->
		for tag in tags
			if tag.match @_sanityPattern then tag else "--warning--"

	_transform: (tweet) ->
		retweetImage = $("<img class='retweet-bird' src='#{Global.basePath}/images/vogel2.png'>") if tweet.retweet
		tweetElement = $("<div id='tweet-#{tweet.id}' class='tweet' tweetid='#{tweet.id}'>")

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

		audioElems = [
			$("<audio id='audio-#{tweet.id}-PB' src='#{tweet.soundp[0]}' hotlength='#{tweet.soundp[2]}'>") if tweet.soundp?,
			$("<audio id='audio-#{tweet.id}-PM' src='#{tweet.soundp[1]}' hotlength='#{tweet.soundp[2]}'>") if tweet.soundp?,
			$("<audio id='audio-#{tweet.id}-CB' src='#{tweet.soundc[0]}' hotlength='#{tweet.soundc[2]}'>"),
			$("<audio id='audio-#{tweet.id}-CM' src='#{tweet.soundc[1]}' hotlength='#{tweet.soundc[2]}'>")
		]

		for audio in audioElems
			tweetElement.append(audio)

		profileImg.css("border-color", "#{tweet.partycolor}") if tweet.partycolor?

		mode = SoundCtrl.getMode()
		tweetCompound = 
			obj: tweetElement
			play: () -> SoundCtrl.play(tweet.id, tweet.soundp[2], mode)
			stop: () -> SoundCtrl.stop(tweet.id, mode)
			time: tweet.time

		speakerElement.click tweetCompound.play

		return tweetCompound

	_enhance: (tweet, hashtags) ->
		return tweet unless hashtags?
		for hashtag in @_sanitize hashtags
			tweet = tweet.replace('#'+hashtag, "<span style='color: blue'>##{hashtag}</span>")
		return tweet






