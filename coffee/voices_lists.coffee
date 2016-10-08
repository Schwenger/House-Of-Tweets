#= require <global.coffee>
#= require <util.coffee>
#= require <model.coffee>
#= require <profile.coffee>

VoicesLists = 

	birdListRoot: $("#voices-list-birds")
	politicianListRoot: $("#voices-list-politicians")

	init: ->
		@_initPoliticianList()
		@_initBirdList()
		Profiles.init(@_displayBirdList)
		@_initSearchBars()

	update: ->
		# no need to do anything because the profile is re-created each time anyway.
		return

	translateBirds: ->
		VoicesLists._removeBirds()
		VoicesLists._initBirdList()

	leavePage: ->
		Profiles.close()
		_searchString = ""
		$("#voices-list-search-bar").val("")
		@_removePolis()
		@_initPoliticianList()

	# SEARCH BAR

	_searchString: 
		poli: ""
		bird: ""
	_initSearchBars: ->
		handler = (which) ->
			searchBar = $("#voices-list-#{which}-search-bar")
			if which is "poli"
				model = Model.politicians
				root = VoicesLists.politicianListRoot
				display = VoicesLists._displayPolis
			else
				model = Model.birds
				root = VoicesLists.birdListRoot
				display = VoicesLists._displayBirds
			(event) ->
				return if VoicesLists._searchString[which] is searchBar.val().toLowerCase()
				VoicesLists._searchString[which] = searchBar.val().toLowerCase()
				if which is "poli"
					pred = (poli) -> 
						poli.name.toLowerCase().indexOf(VoicesLists._searchString[which]) isnt -1
					VoicesLists._removePolis()
				else 
					pred = (bird) ->
						bird[Util.addLang("name")].toLowerCase().indexOf(VoicesLists._searchString[which]) isnt -1
					VoicesLists._removeBirds()
				remaining = {}
				remaining[id] = entity for id, entity of model when pred(entity)
				display root, "voices-list-item", remaining
		$(document).keyup handler("poli")
		$(document).keyup handler("bird")

	# CREATE AND DISPLAY LISTS

	_removePolis: ->
		@_removeEntries(@politicianListRoot, ".voices-list-entry")

	_removeBirds: ->
		@_removeEntries(@birdListRoot, ".voices-list-entry")

	_removeEntries: (root, selector) ->
		root.children(selector).each -> $(this).remove()

	_initPoliticianList: ->
		@_displayPoliticians @politicianListRoot, "voices-list-item"

	_displayPoliticians: (root, prefix) ->
		@_displayPolis(root, prefix, Model.politicians)

	_displayPolis: (root, prefix, list) ->
		for own id, p of list
			do(id, p) ->
				firstLine = p.name
				image = Util.politicianPath p.images?.pathToThumb
				obj = VoicesLists._createListEntry id, firstLine, p.party, image, prefix, (p.twittering? and p.twittering isnt null) # TODO
				root.append obj
				obj.click () -> Profiles.openPoliticianPage id

	_displayBirds: (root, prefix, list) ->
		VoicesLists._displayBirdList root, prefix, ((id) -> Profiles.openBirdPage(id)), list

	_initBirdList: ->
		@_displayBirdList @birdListRoot, "voices-list-item", (id) -> Profiles.openBirdPage(id)

	# NB: This method is called from within profile, thus avoid using @.
	_displayBirdList: (root, prefix, handler, button = false, list = Model.birds) ->
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
				obj = VoicesLists._createListEntry id, b[respName], b.latin_name, image, prefix, false, button, handler
				root.append obj
				obj.click () -> handler(id) unless button

	_createListEntry: (id, first_line, second_line, image, prefix, twitterBird, button = false, handler) ->
		btnTemplate = """
		<div class="button btn">
			<span translateString stringid="select">@Auswählen</span>
		</div>
		"""
		data = 
			id: id
			imagePath: image
			firstLine: first_line
			secondLine: second_line
			firstLineStyle: if first_line.length >= 30 then "font-size: 25px;" else ""
			button: if button then btnTemplate else ""

		template = """
		<div id="{{prefix}}-{{id}}" class="voices-list-entry">
			<img src="{{imagePath}}">
			<div class="two-line-wrapper">
				<span class="first-line" style="{{firstLineStyle}}">{{firstLine}}</span>
				<br>
				<span class="second-line">{{secondLine}}</span>
			</div>
			{{{button}}}
		</div>
		"""

		item = $(Mustache.render(template, data))
		if button
			item.find('.button').each () -> $(@).click(() -> handler(id))

		item
