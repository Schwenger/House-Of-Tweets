#= require <display.coffee>
#= require <sound_controller.coffee>
#= require <screensaver.coffee>
#= require <voices_lists.coffee>
#= require <tweet_controller.coffee>
#= require <language_controller.coffee>
#= require <citizen_user.coffee>

# Debug variables: When typing `console.log "here"` to check whether a certain
# line of code is reached and forgetting the quotation marks in despair, this
# will prevent an error from occurring.
called = "You should never forget quotation marks."
here = "You should never forget quotation marks."

# Setup #################################################################################

# Needed to provide enough time for the carousels to set up without messing up
# the spacing.
citizenUserLoadingTime = 1000

# Public
enforceConsistencyConstraints = ->
	# we cannot [...] set height relative to relative width value
	w = $("#voice-profile-picture").width()
	$("#voice-profile-picture").css("height", w + "px")
	$("#voice-profile-cv").css("height", w + "px")


# Public
initMain = ->
	# NB: Language needs CitizenUser and VoicesLists to be initialized.
	CitizenUser.init()
	# SoundCtrl.turnOnAmbientSound() # TODO: TURN ON
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
		), citizenUserLoadingTime

initMain()

