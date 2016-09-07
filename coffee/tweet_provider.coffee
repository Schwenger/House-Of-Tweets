#= require <global.coffee>
#= require <connector.coffee>
#= require <model.coffee>

class TweetProvider

	constructor: (@callback) ->
		new Connector(Connector.tweetsQueue, @consume)

	consume: (tweets) ->
		console.log "New incoming tweet."
		for tweet in tweets
			if tweet.refresh?
				pid = tweet.refresh.politicianId
				bid = tweet.refresh.birdId
				Model.politicians[pid].self_bird = bid
				Global.pendingBirdListUpdate = true
		# VoicesLists.update() -> introduce mechanism for updating birds after respective tweet.
		if Global.state isnt "center"
			Global.pendingTweets.push tweets
		else
			@callback tweets
