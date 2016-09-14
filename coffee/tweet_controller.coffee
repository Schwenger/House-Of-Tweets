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
		SoundCtrl.setBirdMode(if poli then "P" else "C")

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
		retweetImage = $("<img class='retweet-bird' src='#{Global.basePath}/images/vogel2.png'>") if tweet.retweet
		tweetElement = $("<div id='tweet-#{tweet.id}' class='tweet' tweetid='#{tweet.id}'>")

		tweetProfileInfo = $("<div id='tweet-#{tweet.id}-profile' class='tweet-profile-info'>")
		tweetContent = $("<div id='tweet-#{tweet.id}-content' class='tweet-content'>")
		birdNameContainer = $("<span class='bird-name-container'>")
		birdNamePoli = $("<span translatestring stringID='birds:#{tweet.sound.poli.bid}'>") if tweet.sound.poli?
		birdNamePoli.text(Model.birds[tweet.sound.poli.bid][Util.addLang("name")]) if tweet.sound.poli?
		birdNameCitizen = $("<span translatestring stringID='birds:#{tweet.sound.citizen.bid}'>") 
		birdNameCitizen.text(Model.birds[tweet.sound.citizen.bid][Util.addLang("name")])
		speakerElement = $("<i class='speaker fa fa-music fa-2x' id='tweet-#{tweet.id}-speaker'>")
		profileImg = $("<img src=#{tweet.image}>")
		profileName = $("<div class='profile-name'>")
		profileName.text(tweet.name)
		twitterName = $("<div class='twitter-name'>")
		tweetText = $("<div class='textfield'>")
		tweetTime = $("<div class='time'>")

		birdNameContainer.append(birdNamePoli) if tweet.sound.poli?
		birdNameContainer.append(birdNameCitizen)

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
		tweetElement.append(birdNameContainer)

		audioElems = [
			$("<audio id='audio-#{tweet.id}-PB' src='#{tweet.sound.poli.natural}'>") if tweet.sound.poli?,
			$("<audio id='audio-#{tweet.id}-PM' src='#{tweet.sound.poli.synth}'>") if tweet.sound.poli?,
			$("<audio id='audio-#{tweet.id}-CB' src='#{tweet.sound.citizen.natural}'>"),
			$("<audio id='audio-#{tweet.id}-CM' src='#{tweet.sound.citizen.synth}'>")
		]

		for audio in audioElems
			tweetElement.append(audio)

		profileImg.css("border-color", "#{tweet.partycolor}") if tweet.partycolor?

		tweetCompound = 
			obj: tweetElement
			play: (mode, duration = tweet.sound.duration) -> SoundCtrl.play(tweet.id, duration, mode)
			time: tweet.time
			id: tweet.id

		speakerElement.click () -> tweetCompound.play(SoundCtrl.getMode())

		return tweetCompound

	_enhance: (tweet, hashtags) ->
		return tweet unless hashtags?
		for hashtag in @_sanitize hashtags
			tweet = tweet.replace('#'+hashtag, "<span style='color: blue'>##{hashtag}</span>")
		return tweet






