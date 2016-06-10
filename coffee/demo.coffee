toggleDemo = () ->
	if global.no_demo
		tweet.remove() for tweet in global.displayedTweets
		$("#carousel-control-prev-text").text ""
		$("#carousel-control-next-text").text ""
		$("#tweet-list-footer").addClass "invisible"
		$("#tweet-list-header").addClass "invisible"
		$("#owntweets-bg").attr("src", "../ext/images/demo/demo-right.png")
		$("#tweets-bg").attr("src", "../ext/images/demo/demo-main.png")
		$("#voices-bg").attr("src", "../ext/images/demo/demo-left.png")
	else
		$("#carousel-control-prev-text").text "Vogelstimmen"
		$("#carousel-control-next-text").text "Eigene Tweets"
		$("#tweet-list-footer").removeClass "invisible"
		$("#tweet-list-header").removeClass "invisible"
		global.globalState = "center"
		global.manualTweetID = 0
		$("#owntweets-bg").attr("src", "../ext/images/backgrounds/background-right.jpg")
		$("#tweets-bg").attr("src", "../ext/images/backgrounds/background-center.jpg")
		$("#voices-bg").attr("src", "../ext/images/backgrounds/background-left.jpg")
	global.no_demo = not global.no_demo

toggle_demo_bg_additional = () ->
	return if global.no_demo or global.globalState isnt "left"
	profile_displayed = $("#voices-bg").attr("src") is "../ext/images/demo/demo-additional.png"
	$("#voices-bg").attr("src", if profile_displayed then "../ext/images/demo/demo-left.png" else "../ext/images/demo/demo-additional.png")
