#= require <global.coffee>

SoundCtrl = 

	bird: "P" # P or C for politician or citizen, resp.

	# Public
	setBirdMode: (mode) ->
		@bird = mode

	# Public
	getMode: ->
		@bird

	# Public
	play: (tweetId, duration, mode) ->
		# Turns on the sound of the audio element for the passed params.
		# Sound will be turned off automatically after `duration`.
		audio = @getAudio(tweetId, mode)
		audio[0]?.play() if audio[0]?.paused
		$("#tweet-#{tweetId}-speaker").addClass("speaker-active")
		setTimeout (() -> SoundCtrl.stop(tweetId, mode)),  duration
		return
	
	# Public
	stop: (tweetId, mode) ->
		# Turns off the audio played by the specified audio element.
		audio = @getAudio(tweetId, mode)
		# Bug in chromium:
		# https://bugs.chromium.org/p/chromium/issues/detail?id=593273
		# This has no significant impact in the user experience but 
		# prevents the console to be flooded with the respective exception.
		setTimeout ( ->
			audio[0]?.pause() unless audio[0]?.paused 
			$("#tweet-#{tweetId}-speaker")?.removeClass("speaker-active")
			), 150
		return

	# Public
	getAudio: (id, mode) ->
		# Selects the respective audio-DOM element based on the id and desired 
		# mode.
		$("#audio-#{id}-#{mode}")

	# Public
	turnOnAmbientSound: () ->
		# Places audio element in DOM and starts the sound. Should only be 
		# called once.
		src = "../ext/sounds/ambient.mp3"
		container = $('<div style="position: absolute; z-index: -1; opacity: 0;">')
		audio = $("<audio loop id='ambient-sound-container' src='#{src}'>")
		container.append audio
		$('#carousel').append container
		audio[0].play()

	# Public
	# Deprecated; only used for demonstration.
	toggleAmbient: () ->
		sound = $('#ambient-sound-container')
		if sound[0].paused then sound[0].play() else sound[0].pause()