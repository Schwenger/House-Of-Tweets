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
				global.pendingBirdListUpdate = true
		# updateVoicesPage()
		if global.state isnt "center"
			global.pendingTweets.push tweets
		else
			callback tweets

prepareTweetProvider = (callback) ->
	openConnection(global.rabbitMQ.tweetsQueue, wrap callback)
