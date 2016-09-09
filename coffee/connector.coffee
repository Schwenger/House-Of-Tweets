#= require <util.coffee>

Stomp = require('../ext/node_modules/stompjs')

class Connector

	@config: 
		tweetsQueue: "/queue/tweets"
		persistQueue: "/queue/persist"
		citizenBirdQueue: "/queue/citizenbirds"
		citizenUserQueue: "/queue/citizenuser"
		acknowledgeQueue: "/queue/ack"
		url: "127.0.0.1" # localhost
		port: "15674"
		uname: "guest"
		passcode: "guest"

	constructor: (qname, callback) ->
		console.log "Opening connection to #{qname}" + (if callback? then "; Subscribing..." else ".")

		addr = "#{Connector.config.url}:#{Connector.config.port}"

		@ws       = if location.search is "?ws" then new WebSocket("ws://#{addr}/ws") else new SockJS("http://#{addr}/stomp")
		@client   = Stomp.over(@ws)
		# disable heartbeats
		@client.heartbeat.outgoing = 0
		@client.heartbeat.incoming = 0
		@name     = qname
		@callback = callback
		@uname    = Connector.config.uname
		@passcode = Connector.config.passcode

		@client.debug = (str) -> $("#debug").append(str + "\n");
		@client.connect @uname, @passcode, Connector._subscribe(@client, @callback, @name), Connector._on_error(@name), '/'
	
	@_subscribe: (client, callback, qname) ->
		->
			client.subscribe qname, Connector._consumeWrapper(callback, qname) if callback?

	@_consumeWrapper: (consume, qname) ->
		(msg) ->
			console.log "Received data from #{qname}. Processing..."
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
		@client.send(@name, {}, Util.obj2str(data))
