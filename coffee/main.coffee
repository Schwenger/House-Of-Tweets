
# manualTweets = [{name:"Bettina K.", content: "House of Tweets hat mein Leben verändert. #HouseOfTweets #life #art", time: "09:14", hashtags: ["HouseOfTweets", "art", "life"], image: "../ext/images/bettinak.png"},
# {name:"Saarland University", content: "House of Tweets is very promising. We should consider repurposing CIPSA's funds. #WeMeanIt", time: "tomorrow", hashtags: ["WeMeanIt"], image: "../ext/images/eule.png"},
# {name:"Albert Einstein", content: "You will never fail until you stop tweeting. #clever", time: "12:58", hashtags: ["clever"], image: "../ext/images/einstein.jpg"},
# {name:"Angela Merkel", content: "Die Saarbrücker Informatik ist das stärkste Standbein unserer Wirtschaft. #investitionen", time: "not yet", hashtags: ["investitionen"], image: "../ext/images/merkel.png"},
# {name:"Group Green", content: "Haben eben eine 1.0 auf unser Projekt bekommen!! #yay", time: "soon", hashtags: ["yay"], image: "../ext/images/groupgreen.png"}]

called = "You should never forget quotation marks."
here = "You should never forget quotation marks."

# Setup #################################################################################

startScreensaver = ->
	return if global.screensaver.active isnt -1
	# r = Math.floor(Math.random() * 5) # leq 4
	r = 0
	global.screensaver.active = r
	saver = $("#screensaver-element-#{r}")
	saver.removeClass "invisible"
	saver.addClass "load"
	saver.children().each () -> $(this).addClass "load"
	setTimeout(stopScreensaver, global.screensaver.duration)

stopScreensaver = ->
	return if global.screensaver.active is -1
	saver = $("#screensaver-element-0")
	saver.addClass "invisible"
	saver.removeClass "load"
	saver.children().each () -> $(this).removeClass "load"
	global.screensaver.active = -1
	global.screensaver.lastTouch = util.time()

testSimple = () ->
	tweetTest = {name:"Michaela Klauckington", content: "Working all morning long. #awesome", time: "12:00", hashtags: []}
	$("#tweet-list").append(transform tweetTest)

global.screensaver.lastTouch = util.time()

enforceConsistencyConstraints = ->
	# we cannot [...] set height in relative to relative width value
	w = $("#voice-profile-picture").width()
	$("#voice-profile-picture").css("height", w + "px")
	$("#voice-profile-cv").css("height", w + "px")

initScreensaver = ->
	$(document).click (->
		global.screensaver.lastTouch = util.time()
		stopScreensaver()
		)

	setInterval (->
		startScreensaver() if util.time() - global.screensaver.lastTouch > global.screensaver.startThreshold
		), global.screensaver.checkFrequency

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
			# when 68 then toggleDemo() # d
			# when 65 then toggle_demo_bg_additional() # a
			# when 86 then toggle_demo_bg_additional() # v
			when 34 then triggerTweet() # page down
			# when 84 then triggerTweet() # t
			# when 87 then useBlinking = not useBlinking # w
			# when 66 then useBlinking = not useBlinking # b
			when 123 then startScreensaver() # f12
			when 121 then toggleAmbient() # f11
		)

initCarousel()
initMain()

# console.log(""" \
# Controls:
# 	d: open demo page
# 	a | v: open Altmeier's page ('Vogelstimmen' view only)
# 	t | page_down: fire tweet (Non-demo view only)
# 	b | w: enables blinking of incoming tweets""")

# openImpressum()
# openAdminPage()

# TODOS
# Language overlay fades in
# sidebar elements' texts change during scroll animation, not instantly.
# extend demo (remove all the elements)