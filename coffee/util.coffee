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

	nyahNyah: [
		"kitty", "rainbow", "tippytoe", "jibberjabber", "#IHideMyInsecurityBehindCurses", "pinky",
		"Kätzchen", "Regenbogen", "BlaBlaBla", "#InnerlichTot", "Wattebällchen", "#ILikeTrains"
		"$@*$@!#", "#$@&%*!", "$@*$@!#", "#$@&%*!" # double occurrences intended
	]

	_getRandom: (collection) ->
		collection[Math.floor(Math.random() * collection.length)]

	sanitize: (content, byPoli) ->
		if not byPoli
			for baddy in bad_words
				replacement = Util._getRandom(Util.nyahNyah)
				content = content.replace(new RegExp("(\\s|^)#{baddy}(\\s|$)"), " #{replacement} ")
		content = content[..140]
		$("<span>").text(content).html() # should not be necessary, but can't hurt as well.
		content

	tagPattern: /\w*/i
	sanitizeTags: (tags) ->
		for tag in tags
			if tag.match Util.tagPattern then tag else "--NOPE--" 

}