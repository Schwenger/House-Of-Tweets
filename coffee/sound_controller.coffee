#= require <global.coffee>
SoundCtrl = 
	turnOnSound: (incomingTweetIds) ->
		for id in incomingTweetIds
			@playSound id

	playSound: (tweetId) ->
		audio = $("#audio-#{tweetId}-P")
		useCitizenBirds = not Global.usePoliBirds
		if useCitizenBirds or not audio[0]?
			audio = $("#audio-#{tweetId}-C")
		audio[0]?.play()
		$("#tweet-#{tweetId}-speaker").addClass("speaker-active")
		sound_length = audio.attr("hotlength")
		setTimeout (() -> 
			audio.stop()
			$("#tweet-#{tweetId}-speaker").removeClass("speaker-active")
			), parseInt(sound_length)

	turnOnAmbientSound: () ->
		src = "../ext/sounds/ambient.mp3"
		container = $('<div style="position: absolute; z-index: -1; opacity: 0;">')
		audio = $("<audio loop id='ambient-sound-container' src='#{src}'>")
		container.append audio
		$('#carousel').append container
		audio[0].play()

	toggleAmbient: () ->
		sound = $('#ambient-sound-container')
		if sound[0].paused then sound[0].play() else sound[0].pause()