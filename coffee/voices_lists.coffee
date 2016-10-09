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
		Profiles.init()
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
				obj = Util.createListEntry id, firstLine, p.party, image, prefix, undefined
				root.append obj
				obj.click () -> Profiles.openPoliticianPage id

	_displayBirds: (root, prefix, list) ->
		handler = (obj, id) -> obj.click(() -> Profiles.openBirdPage(id))
		Util.createBirdList root, prefix, list, undefined, handler

	_initBirdList: ->
		@_displayBirds(@birdListRoot, "voices-list-item", Model.birds)
