
global = {
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

	rabbitMQ:
		tweetsQueue: "/queue/tweets"
		persistQueue: "/queue/persist"
		citizenBirdQueue: "/queue/citizenbirds"
		citizenUserQueue: "/queue/citizenuser"
		acknowledgeQueue: "/queue/ack"
		url: "127.0.0.1" # localhost
		port: "15674"
		uname: "guest"
		passcode: "guest"

	screensaver: {
		# duration: 60000,
		duration: 6000000,
		# startThreshold: 2 * 6 * 1000,
		startThreshold: 1500000,
		checkFrequency: 500000,
		# checkFrequency: 5000,
		active: -1,
		lastTouch: -1
	}
	screensaverOn: false
	
	transform: (langString) ->
		switch(langString)
			when "german" then "de"
			when "english" then "en"		
			when "french" then "fr"

	langId: () -> global.transform(global.language)

	handleStalledTweets: ->
		tmp = global.pendingTweets
		global.pendingTweets = []
		updateTweetLists(batch) for batch in tmp
}

util = {
	composeFunctions: (functions) ->
		() -> 
			f() for f in functions

	obj2str: (obj) ->
		JSON.stringify obj

	str2obj: (str) ->
		JSON.parse str

	time: ->
		new Date().getTime()

	transformTime: (time) ->
		mins = time.getMinutes()
		mins = "0" + mins if mins < 10
		"#{time.getHours()}:#{mins}"

	clone: (o) -> 
		JSON.parse(JSON.stringify(o))

	addLang: (str) -> 
		switch global.language
			when "english" then "en_" + str
			when "german"  then "de_" + str
			when "french"  then "fr_" + str

	createError: (msg, time) ->
		errorObj = $("<div class='error-message'>")
		errorObj.text(msg)
		$("#carousel").append(errorObj)
		setTimeout (-> errorObj.remove()), time
}