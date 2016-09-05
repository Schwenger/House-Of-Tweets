#= require <global.coffee>
#= require <connector.coffee>
#= require <model.coffee>

wrap = (callback) ->
	(tweets) ->
		console.log "New incoming tweet."
		for tweet in tweets
			if tweet.refresh?
				pid = tweet.refresh.politicianId
				bid = tweet.refresh.birdId
				Model.politicians[pid].self_bird = bid
				Global.pendingBirdListUpdate = true
		# updateVoicesPage()
		if Global.state isnt "center"
			Global.pendingTweets.push tweets
		else
			callback tweets

prepareTweetProvider = (callback) ->
	openConnection(Global.rabbitMQ.tweetsQueue, wrap callback)
