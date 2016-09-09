#= require <model.coffee>
#= require <global.coffee>
#= require <voices_lists.coffee>
#= require <connector.coffee>

class TweetProvider

	constructor: (@callback) ->
		new Connector(Connector.config.tweetsQueue, @consume)

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
