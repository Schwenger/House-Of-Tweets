# Public
Global = {
	# For testing only
	manualTweetID: 0
	# Human readable language string. german/english/french
	language: "german"
	# Base path for external files.
	basePath:  "../ext/"
	# Path to directory with birds' images.
	birdPath:  "../ext/images/birds/"
	# Path to directory with politicians' images.
	politicianPath: "../ext/images/politicians/"

	_transform: (langString) ->
		# transforms a human readable string into a shorter id.
		switch(langString)
			when "german" then "de"
			when "english" then "en"		

	# Provides the id for the currently selected language.
	langId: () -> Global._transform(Global.language)

	config:
		citizen_user_bird_entry_clickable: false
}

