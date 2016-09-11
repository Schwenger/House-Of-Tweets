#= require <global.coffee>

Util = {

	count: (list, pred) ->
		list.reduce (sum, elem) -> sum += pred(elem)

	birdPath: (id, add) ->
		Global.birdPath + id + (if add? then add else "") + ".jpg"

	politicianPath: (id) ->
		Global.politicianPath + if id? then id else "placeholder.png"

	composeFunctions: (functions...) ->
		(args...) -> 
			f(args) for f in functions

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
		switch Global.language
			when "english" then "en_" + str
			when "german"  then "de_" + str
			when "french"  then "fr_" + str

	createError: (msg, time) ->
		errorObj = $("<div class='error-message'>")
		errorObj.text(msg)
		$("#carousel").append(errorObj)
		setTimeout (-> errorObj.remove()), time
}