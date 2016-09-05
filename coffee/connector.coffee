#= require <global.coffee>
#= require <util.coffee>

Stomp = require('../ext/node_modules/stompjs')

_openConnection = (callback, qname) ->
	MQ = {}
	MQ.ws       = if location.search is "?ws" then new WebSocket("ws://#{Global.rabbitMQ.url}:#{Global.rabbitMQ.port}/ws") else new SockJS("http://#{Global.rabbitMQ.url}:#{Global.rabbitMQ.port}/stomp")
	MQ.client   = Stomp.over(MQ.ws)
	MQ.name     = qname
	MQ.callback = callback
	MQ.uname    = Global.rabbitMQ.uname
	MQ.passcode = Global.rabbitMQ.passcode
	# disable heartbeats
	MQ.client.heartbeat.outgoing = 0
	MQ.client.heartbeat.incoming = 0

	MQ.client.debug = (str) -> $("#debug").append(str + "\n");

	return MQ

_subscribe = (MQ) ->
	->
		console.log "Connected to #{MQ.name};" + (if MQ.callback? then " Subscibing..." else "")
		MQ.client.subscribe MQ.name, _consumeWrapper(MQ.callback, MQ.name) if MQ.callback?


_consumeWrapper = (consume, code) ->
	(msg) ->
		console.log "Received data from #{code}. Processing..."
		console.log _extractContent msg
		consume(_extractContent msg)

_on_error = (code) ->
	() ->
		console.log 'error on ' + code

_connect = (MQ) ->
	MQ.client.connect MQ.uname, MQ.passcode, _subscribe(MQ), _on_error(MQ.name), '/'

_extractContent = (txt) ->
	Util.str2obj(txt.body)

_consume = (msg) ->
	tweets = _extractContent msg
	console.log(" [x] Received %s", tweet.content) for tweet in tweets

openConnection = (qname, callback) ->
	console.log "*** Opening connection to >>> #{qname}"
	MQ = _openConnection(callback, qname)
	_connect MQ
	return MQ

sendToQueue = (MQ, data) ->
	console.log "Sending data to " + MQ.name
	console.log data
	MQ.client.send(MQ.name, {}, Util.obj2str(data))
