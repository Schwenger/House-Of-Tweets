#= require <carousel.coffee>
#= require <global.coffee>
#= require <util.coffee>
#= require <impressum.coffee>
#= require <voices_controller.coffee>
#= require <tweet_controller.coffee>
#= require <tweet_provider.coffee>
#= require <citizen_birds.coffee>
#= require <language_controller.coffee>

called = "You should never forget quotation marks."
here = "You should never forget quotation marks."

# Setup #################################################################################

startScreensaver = ->
	return if Global.screensaver.active isnt -1
	Global.screensaver.active = 0 # we only have one screen saver, type 0
	saver = $("#screensaver-element-#{r}")
	saver.removeClass "invisible"
	saver.addClass "load"
	saver.children().each () -> $(this).addClass "load"
	setTimeout(stopScreensaver, Global.screensaver.duration)

stopScreensaver = ->
	return if Global.screensaver.active is -1
	saver = $("#screensaver-element-0")
	saver.addClass "invisible"
	saver.removeClass "load"
	saver.children().each () -> $(this).removeClass "load"
	Global.screensaver.active = -1
	Global.screensaver.lastTouch = Util.time()

testSimple = () ->
	tweetTest = {name:"Michaela Klauckington", content: "Working all morning long. #awesome", time: "12:00", hashtags: []}
	$("#tweet-list").append(transform tweetTest)

Global.screensaver.lastTouch = Util.time()

enforceConsistencyConstraints = ->
	# we cannot [...] set height in relative to relative width value
	w = $("#voice-profile-picture").width()
	$("#voice-profile-picture").css("height", w + "px")
	$("#voice-profile-cv").css("height", w + "px")

initScreensaver = ->
	$(document).click (->
		Global.screensaver.lastTouch = Util.time()
		stopScreensaver()
		)

	setInterval (->
		startScreensaver() if Util.time() - Global.screensaver.lastTouch > Global.screensaver.startThreshold
		), Global.screensaver.checkFrequency

turnOnAmbientSound = () ->
	src = "../ext/sounds/ambient.mp3"
	container = $('<div style="position: absolute; z-index: -1; opacity: 0;">')
	audio = $("<audio loop id='ambient-sound-container' src='#{src}'>")
	container.append audio
	$('#carousel').append container
	audio[0].play()

toggleAmbient = () ->
	sound = $('#ambient-sound-container')
	if sound[0].paused then sound[0].play() else sound[0].pause()

initMain = ->
	changeLanguage("german")
	turnOnAmbientSound()
	initScreensaver()
	prepareVoicesPage()
	prepareImpressum()
	prepareAdminPage()
	prepareCitizenBirdsPage()
	prepareTweetController()
	prepareTweetProvider(updateTweetLists)
	$(document).keydown((e) -> 
		switch e?.which
			when 34 then triggerTweet() # page down
			when 84 then triggerTweet() # t
			when 123 then startScreensaver() # f12
			when 121 then toggleAmbient() # f11
		)

initCarousel()
initMain()

# openImpressum()
# openAdminPage()

# TODOS
# Language overlay fades in