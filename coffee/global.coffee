
Global = {
	manualTweetID: 0
	language: "german"
	basePath:  "../ext/"
	birdPath:  "../ext/images/birds/"
	politicianPath: "../ext/images/politicians/"
	twitterIconPath: "../ext/images/twitter-icon.png"

	_transform: (langString) ->
		switch(langString)
			when "german" then "de"
			when "english" then "en"		

	langId: () -> Global._transform(Global.language)
}

