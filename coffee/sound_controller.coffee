
turnOnSound = (incomingTweetIds) ->
	for id in incomingTweetIds
		playSound id

playSound = (tweetId) ->
	audio = $("#audio-#{tweetId}-P")
	useCitizenBirds = not global.usePoliBirds
	if useCitizenBirds or not audio[0]?
		audio = $("#audio-#{tweetId}-C")
	audio[0]?.play()
	$("#tweet-#{tweetId}-speaker").addClass("speaker-active")
	sound_length = audio.attr("hotlength")
	setTimeout (() -> 
		audio.stop()
		$("#tweet-#{tweetId}-speaker").removeClass("speaker-active")
		), parseInt(sound_length)