#= require <carousel.coffee>
#= require <global.coffee>
#= require <util.coffee>
#= require <impressum.coffee>
#= require <voices_lists.coffee>
#= require <tweet_controller.coffee>
#= require <tweet_provider.coffee>
#= require <citizen_user.coffee>
#= require <language_controller.coffee>
#= require <screensaver.coffee>
#= require <sound_controller.coffee>

called = "You should never forget quotation marks."
here = "You should never forget quotation marks."

# Setup #################################################################################

enforceConsistencyConstraints = ->
	# we cannot [...] set height in relative to relative width value
	w = $("#voice-profile-picture").width()
	$("#voice-profile-picture").css("height", w + "px")
	$("#voice-profile-cv").css("height", w + "px")

initMain = ->
	SoundCtrl.turnOnAmbientSound()
	LanguageController.init("german")
	Screensaver.init()
	Carousel.init()
	VoicesLists.init()
	prepareImpressum()
	prepareAdminPage()
	prepareCitizenBirdsPage()
	prepareTweetController()
	prepareTweetProvider(updateTweetLists)
	$(document).keydown((e) -> 
		switch e?.which
			when 34 then triggerTweet() # page down
			when 84 then triggerTweet() # t
			when 123 then Screensaver.start() # f12
			when 121 then SoundCtrl.toggleAmbient() # f11
		)

initMain()

