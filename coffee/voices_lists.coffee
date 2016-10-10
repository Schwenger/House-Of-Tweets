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
		$("#bird-search-bar").val("")
		$("#poli-search-bar").val("")
		Global.searchString.bird = ""
		Global.searchString.poli = ""
		@_removePolis()
		@_initPoliticianList()

	_initSearchBars: ->
		# bird search bar
		birdAdd = (birds) -> 
			VoicesLists._displayBirds(VoicesLists.birdListRoot, "voices-list-item", birds)
		birdQualifies = (bird, search) -> 
			bird[Util.addLang("name")].toLowerCase().indexOf(search) isnt -1
		birdRemove = () -> VoicesLists._removeBirds()
		Util.initSearchBar("bird", Model.birds, birdAdd, birdRemove, birdQualifies)
		# poli search bar
		poliAdd = (polis) -> 
			VoicesLists._displayPolis(VoicesLists.politicianListRoot, "voices-list-item", polis)
		poliQualifies = (poli, search) ->
			poli.name.toLowerCase().indexOf(search) isnt -1
		poliRemove = () -> VoicesLists._removePolis()
		Util.initSearchBar("poli", Model.politicians, poliAdd, poliRemove, poliQualifies)


	# CREATE AND DISPLAY LISTS

	_removePolis: ->
		@_removeEntries(@politicianListRoot, ".list-entry")

	_removeBirds: ->
		@_removeEntries(@birdListRoot, ".list-entry")

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
