
Global = {
	manualTweetID: 0
	language: "german"
	basePath:  "../ext/"
	birdPath:  "../ext/images/birds/"
	politicianPath: "../ext/images/politicians/"

	_transform: (langString) ->
		switch(langString)
			when "german" then "de"
			when "english" then "en"		

	langId: () -> Global._transform(Global.language)
}

