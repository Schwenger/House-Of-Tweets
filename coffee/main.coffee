#= require <display.coffee>
#= require <sound_controller.coffee>
#= require <screensaver.coffee>
#= require <voices_lists.coffee>
#= require <tweet_controller.coffee>
#= require <language_controller.coffee>
#= require <citizen_user.coffee>

called = "You should never forget quotation marks."
here = "You should never forget quotation marks."

# Setup #################################################################################

enforceConsistencyConstraints = ->
	# we cannot [...] set height relative to relative width value
	w = $("#voice-profile-picture").width()
	$("#voice-profile-picture").css("height", w + "px")
	$("#voice-profile-cv").css("height", w + "px")

# NB: Language needs CitizenUser and VoicesLists to be initialized.
initMain = ->
	CitizenUser.init()
	# SoundCtrl.turnOnAmbientSound()
	Screensaver.init()
	Display.init()
	VoicesLists.init()
	TweetController.init()
	LanguageController.init("german")
	# the nested carousel demands to not be `display: none`'ed. 
	# We obey and simply remove the active class in time.
	setTimeout (() ->
		$('#owntweets').removeClass("active")
		$('body').css('opacity', '1')
		), 1000

initMain()

