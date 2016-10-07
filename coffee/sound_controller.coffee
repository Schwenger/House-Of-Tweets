#= require <global.coffee>

SoundCtrl = 

	bird: "P" # P or C for politician or citizen

	setBirdMode: (mode) ->
		@bird = mode

	setSoundMode: (mode) ->
		@sound = mode

	getMode: ->
		@bird + @sound

	play: (tweetId, duration, mode) ->
		audio = @getAudio(tweetId, mode)
		audio[0]?.play()
		$("#tweet-#{tweetId}-speaker").addClass("speaker-active")
		setTimeout (() -> SoundCtrl.stop(tweetId, mode)),  duration
		return

	stop: (tweetId, mode) ->
		audio = @getAudio(tweetId, mode)
		# Bug in chromium:
		# https://bugs.chromium.org/p/chromium/issues/detail?id=593273
		# This has no significant impact in the user experience but 
		# prevents the console to be flooded with the respective exception.
		setTimeout ( ->
			audio[0]?.pause()
			$("#tweet-#{tweetId}-speaker")?.removeClass("speaker-active")
			), 150
		return

	getAudio: (id, mode) ->
		$("#audio-#{id}-#{mode}")

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