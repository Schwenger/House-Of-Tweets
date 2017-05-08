#= require <global.coffee>

Util = {

	count: (list, pred) ->
		# Counts the number of elements satisfying `pred`.
		list.reduce (sum, elem) -> sum += pred(elem)

	birdPath: (id, add) ->
		# Returns the path to the bird's image. Attaches `add` to the id if 
		# specified.
		Global.birdPath + id + (if add? then add else "") + ".jpg"

	politicianPath: (id) ->
		# Returns the path to the politician's image.
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
		# Adds a language prefix w.r.t. the globally set time.
		@getLang() + '_' + str

	getLang: ->
		# Retrieves the language identifier w.r.t. the globally set time.
		switch Global.language
			when "english" then "en"
			when "german"  then "de"

	# List of potential replacements for swear words.
	nyahNyah: [
		"*****", "****", "#####", "*****", "#####",
		"$@*$@!#", "#$@&%*!", "$@*$@!#", "#$@&%*!",
		"█████", "█████", "██████",
		"*****" # duplicates and variations intentional
	]

	_getRandom: (collection) ->
		collection[Math.floor(Math.random() * collection.length)]

	sanitize: (content, byPoli) ->
		# Replaces bad words and sanitizes the input string.
		# When tweet is by a politician, no replacement will take place.
		if not byPoli
			for baddy in bad_words
				replacement = Util._getRandom(Util.nyahNyah)
				content = content.replace(new RegExp("(\\s|^)#{baddy}(\\s|$)", "i"), " #{replacement} ")
		content = content[...140]
		$("<span>").text(content).html() # should not be necessary, but can't hurt as well.
		content

	tagPattern: /\w*/i
	sanitizeTags: (tags) ->
		# Replaces all `tags` by a safe replacement string.
		for tag in tags
			if tag.match Util.tagPattern then tag else "--NOPE--" 

	createBirdList: (root, prefix, list, addon, modifier, latinName = true) ->
		# Transforms `list`'s elements into entries and appends them to the `root`. 
		# The entries' ids start with `prefix` and end with the bird's id.
		# `addon` had to provide html given an id. The result is positioned 
		# on the right hand side of the name.
		# After each element's creation, modifier is called on them and the id. 
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
		# Creates an entry suitable for a bird/politician list.
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

}
