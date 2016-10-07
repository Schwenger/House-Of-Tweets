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
	_displayBirdList: (root, prefix, handler, list = Model.birds) ->
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
				obj = VoicesLists._createListEntry id, b[respName], b.latin_name, image, prefix, false
				root.append obj
				obj.click () -> handler(id)

	_createListEntry: (id, first_line, second_line, image, prefix, twitterBird) ->
		item_o = $("<div id='#{prefix}-#{id}' class='voices-list-entry'>")
		
		if first_line.length >= 30
			first_line_o = $("<span class='first-line' style='font-size: 25px;'>")
		else
			first_line_o = $("<span class='first-line'>")
		first_line_o.text(first_line)
		
		lineBreak_o = $("<br>")
		
		span_o = $("<div class='two-line-wrapper'>")

		second_line_o = $("<span class='second-line'>")
		second_line_o.text(second_line)

		image_o = $("<img src='#{image}'>")

		span_o.append first_line_o
		span_o.append lineBreak_o
		span_o.append second_line_o

		item_o.append image_o
		item_o.append span_o

		return item_o


