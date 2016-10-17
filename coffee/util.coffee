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
		"Kätzchen", "Regenbogen", "BlaBlaBla", "#InnerlichTot", "Wattebällchen", "#ILikeTrains",
		"UNICORN", "Einhorn", "$@*$@!#", "#$@&%*!", "$@*$@!#", "#$@&%*!" # double occurrences intended
	]

	_getRandom: (collection) ->
		collection[Math.floor(Math.random() * collection.length)]

	sanitize: (content, byPoli) ->
		if not byPoli
			for baddy in bad_words
				replacement = Util._getRandom(Util.nyahNyah)
				content = content.replace(new RegExp("(\\s|^)#{baddy}(\\s|$)", "i"), " #{replacement} ")
		content = content[...140]
		$("<span>").text(content).html() # should not be necessary, but can't hurt as well.
		content

	tagPattern: /\w*/i
	sanitizeTags: (tags) ->
		for tag in tags
			if tag.match Util.tagPattern then tag else "--NOPE--" 

	# Transforms `list`'s elements into entries and appends them to the `root`. 
	# The entries' ids start with `prefix` and end with the bird's id.
	# `addon` had to provide html given an id. The result is positioned 
	# on the right hand side of the name.
	# After each element's creation, modifier is called on them and the id. 
	createBirdList: (root, prefix, list, addon, modifier, latinName = true) ->
		respName = Util.addLang "name"
		cmp = (a,b) ->
			if a[1][respName] < b[1][respName] then -1
			else if b[1][respName] < a[1][respName] then 1
			else 0
		sortable = ([id, bird] for own id, bird of list)
		sortable.sort(cmp)
		sortable
		for [id, b] in sortable
			do(id, b) ->
				image = Util.birdPath id
				secondLine = if latinName then b.latin_name else ""
				obj = Util.createListEntry id, b[respName], secondLine, image, prefix, addon
				root.append obj
				modifier(obj, id) if modifier?

	createListEntry: (id, first_line, second_line, image, prefix, addon) ->		
		data = 
			id: id
			imagePath: image
			firstLine: first_line
			secondLine: second_line
			firstLineStyle: if first_line.length >= 30 then "font-size: 25px;" else ""
			addon: if addon? then addon(id) else ""
			prefix: prefix

		template = """
		<div id="{{prefix}}-{{id}}" class="list-entry">
			{{{addon}}}
			<img src="{{imagePath}}">
			<div class="two-line-wrapper">
				<div class="first-line" style="{{firstLineStyle}}">{{firstLine}}</div>
				<div class="second-line">{{secondLine}}</div>
			</div>
		</div>
		"""
		$(Mustache.render(template, data))

	initSearchBar: (id, model, add, remove, qualifies) ->
		searchBar = $("##{id}-search-bar")
		handler = (event) ->
			oldString = Global.searchString[id]
			newString = searchBar.val().toLowerCase()
			return if oldString is newString
			Global.searchString[id] = newString
			remaining = {}
			remaining[id] = entity for id, entity of model when qualifies(entity, newString)
			remove()
			add remaining
		$(document).keyup handler

}