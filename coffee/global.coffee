
Global = {
	threshold: 6;
	sanityPattern: /\w*/
	testData: []
	manualTweetID: 0
	state: "center"
	pendingTweets: []
	pendingBirdListUpdate: false
	no_demo: true
	useBlinking: false
	language: "german"
	base_path:  "../ext/"
	image_path: "../ext/images/"
	sound_path: "../ext/sounds/"
	bird_path:  "../ext/images/birds/"
	politician_path: "../ext/images/politicians/"
	
	usePoliBirds: true
	poliTweetsOnly: true
	
	transform: (langString) ->
		switch(langString)
			when "german" then "de"
			when "english" then "en"		
			when "french" then "fr"

	langId: () -> Global.transform(Global.language)

	handleStalledTweets: ->
		tmp = global.pendingTweets
		global.pendingTweets = []
		updateTweetLists(batch) for batch in tmp
}

