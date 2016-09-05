#= require <global.coffee>
#= require <util.coffee>
#= require <sound_controller.coffee>

### LOGIC: ###

tLists = {
	mixed: [undefined, undefined, undefined, undefined, undefined, undefined]
	poli: [undefined, undefined, undefined, undefined, undefined, undefined]
}

archive = []
toPlay = []
active = false
batchDuration = 10 * 1000
batchIntervall = 5 * 1000

archiveRoot = $('#archive-container')

addToArchive = (tweet) ->
	entry = [tweet.time, a = $("<audio src='#{(if Global.usePoliSounds and tweet.byPoli then tweet.soundp[0] else tweet.soundc[0])}'>")]
	archive.push entry

stopPlayback = (objs) ->
	() ->
		for obj in objs
			obj.stop()
			obj.remove()

startPlaybackHandler = () ->
	return if toPlay.length is 0
	[head..., tail] = toPlay
	toPlay = head
	for audioObj in tail
		archiveRoot.append(audioObj)
		audioObj[0].play()
	setTimeout stopPlayback(tail), batchDuration
	setTimeout startPlaybackHandler, batchIntervall

playSoundsFactory = (duration) ->
	() ->
		return if active
		qualifying = 0
		nowTime = Util.time()
		diff = duration * 60 * 60 * 1000
		for [time, audioObj] in archive
			if nowTime - time.getTime() < diff then qualifying += 1 else break 
		maxIndex = qualifying - 1
		for i in [0..(maxIndex / 10)]
			tmp = (audioObj for [time, audioObj] in archive[i * 10 ... Math.min((i+1) * 10, maxIndex+1)])
			toPlay.push tmp
		startPlaybackHandler()

prepareTweetController = ->
	$('#play-tweets-1-button').click(playSoundsFactory 1)
	$('#play-tweets-6-button').click(playSoundsFactory 6)
	$('#play-tweets-24-button').click(playSoundsFactory 24)

	birdsSwitch = $('#voices-switch')
	tweetsSwitch = $('#citizen-tweets-switch')
	
	birdsSwitch.change (-> 
		Global.usePoliBirds = birdsSwitch.prop('checked')
		changeView()
		)
	tweetsSwitch.change (-> 
		Global.poliTweetsOnly = tweetsSwitch.prop('checked')
		changeView()
		)

changeView = ->
	oldL = tLists[if Global.poliTweetsOnly then "mixed" else "poli"]
	newL = tLists[if Global.poliTweetsOnly then "poli" else "mixed"]
	tweet?.remove() for tweet in oldL
	root = $('#tweet-list')
	root.append tweet for tweet in newL
	turnOnSound (obj.attr('tweetid') for obj in newL when obj?)

updateTweetLists = (incomingTweets) ->
	tweet.time = new Date(parseInt tweet.time) for tweet in incomingTweets
	addToArchive(tweet) for tweet in incomingTweets
	newTweets = (transform tweet for tweet in incomingTweets)

	for tweet, index in newTweets
		tLists.mixed.push tweet # unless tweet.byPoli and Global.poliTweetsOnly
		tLists.poli.push tweet if incomingTweets[index].byPoli

	updateShownTweets(incomingTweets)

updateShownTweets = (incomingTweets) ->
	# update poli list
	newOnes = 0
	newOnes += 1 for tweet in incomingTweets when tweet.byPoli
	tweetsToRemove = tLists.poli[0..newOnes] if Global.poliTweetsOnly
	tLists.poli = tLists.poli[newOnes..]
	tLists.poli  = tLists.poli[tLists.poli.length - Global.threshold..]
	# update mixed list
	newOnes = incomingTweets.length
	tweetsToRemove = tLists.mixed[0..newOnes] unless Global.poliTweetsOnly
	tLists.mixed = tLists.mixed[newOnes..]
	tLists.mixed = tLists.mixed[tLists.mixed.length - Global.threshold..]

	tweet?.remove() for tweet in tweetsToRemove

	list = $('#tweet-list')
	respectiveList = if Global.poliTweetsOnly then tLists.poli else tLists.mixed
	for tweet in respectiveList
		list.append tweet 

	turnOnSound(tweet.id for tweet in incomingTweets)

sanitize = (tags) ->
	for tag in tags
		if tag.match Global.sanityPattern then tag else "--warning--"

triggerTweet = () ->
	updateTweetLists [model.manualTweets[Global.manualTweetID]]
	Global.manualTweetID = (Global.manualTweetID + 1) % model.manualTweets.length

appendTweet = (tweet) ->
	$("#tweet-list").append(transform tweet)

transform = (tweet) ->
	retweetImage = $("<img class='retweet-bird' src='#{Global.base_path}/images/vogel2.png'>") if tweet.retweet
	tweetElement = $("<div id='tweet-#{tweet.id}' class='tweet' tweetid='#{tweet.id}'>")
	console.log tweet.soundp
	console.log tweet.soundc
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

	tweetText.html(enhance tweet.content, tweet.hashtags)
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
		playSound tweet.id
		)	
	return tweetElement

enhance = (tweet, hashtags) ->
	return tweet unless hashtags?
	for hashtag in sanitize hashtags
		tweet = tweet.replace('#'+hashtag, "<span style='color: blue'>##{hashtag}</span>")
	return tweet






