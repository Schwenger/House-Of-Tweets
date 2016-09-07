#= require <global.coffee>
#= require <util.coffee>

Stomp = require('../ext/node_modules/stompjs')

class Connector

	constructor: (qname, callback) ->
		console.log "*** Opening connection to >>> #{qname}"

		@ws       = if location.search is "?ws" then new WebSocket("ws://#{Global.rabbitMQ.url}:#{Global.rabbitMQ.port}/ws") else new SockJS("http://#{Global.rabbitMQ.url}:#{Global.rabbitMQ.port}/stomp")
		@client   = Stomp.over(@ws)
		# disable heartbeats
		@client.heartbeat.outgoing = 0
		@client.heartbeat.incoming = 0
		@name     = qname
		@callback = callback
		@uname    = Global.rabbitMQ.uname
		@passcode = Global.rabbitMQ.passcode

		@client.debug = (str) -> $("#debug").append(str + "\n");
		@client.connect @name, @passcode, Connector._subscribe(@client, @callback, @name), Connector._on_error(@name), '/'
	
	@_subscribe: (client, callback, name) ->
		->
			console.log "Connected to #{MQ.name};" + (if callback? then " Subscribing..." else "")
			client.subscribe name, Connector._consumeWrapper(callback, name) if callback?


	@_consumeWrapper: (consume, code) ->
		(msg) ->
			console.log "Received data from #{code}. Processing..."
			console.log Connector._extractContent msg
			consume(Connector._extractContent msg)

	@_on_error: (name) ->
		(err) ->
			console.log 'error on ' + name
			console.log err

	@_extractContent: (txt) ->
		Util.str2obj(txt.body)

	@_consume: (msg) ->
		tweets = Connector._extractContent msg
		console.log(" [x] Received %s", tweet.content) for tweet in tweets

	sendToQueue: (data) ->
		console.log "Sending data to " + @name
		console.log data
		@client.send(@name, {}, Util.obj2str(data))
