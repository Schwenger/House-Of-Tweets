#= require <global.coffee>

SoundCtrl = 

	bird: "P" # P or C for politician or citizen
	sound: "B" # B or M for bird or musician

	setBirdMode: (mode) ->
		@bird = mode

	setSoundMode: (mode) ->
		@sound = mode

	getMode: ->
		@bird + @sound

	play: (tweetId, duration, mode) ->
		# TODO THIS IS NO RIGHT, ITS JUST UNTIL THE BE HAS THIS FEATURE IMPLEMENTED
		duration = 10000
		audio = @_getAudio(tweetId, mode)
		audio[0].play()
		$("#tweet-#{tweetId}-speaker").addClass("speaker-active")
		setTimeout (() -> SoundCtrl.stop(tweetId, mode)),  duration
		return

	stop: (tweetId, mode) ->
		audio = @_getAudio(tweetId, mode)
		audio[0].pause()
		$("#tweet-#{tweetId}-speaker").removeClass("speaker-active")
		return

	_getAudio: (id, mode) ->
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