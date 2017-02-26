#= require <global.coffee>
#= require <util.coffee>
#= require <model.coffee>
#= require <profile.coffee>

VoicesLists = 

	birdListRoot: $("#voices-list-birds")
	politicianListRoot: $("#voices-list-politicians")

	searchString: 
		poli: ""
		bird: ""

	# Public
	init: ->
		@_initPoliticianList()
		@_initBirdList()
		Profiles.init()
		@_initSearchBars()
		@_initScrollHandler()

	# Public
	update: ->
		# no need to do anything because the profile is re-created each time anyway.
		return

	# Public
	translateBirds: ->
		# Translates all bird names.
		VoicesLists._removeBirds()
		VoicesLists._initBirdList()

	# Public
	leavePage: ->
		# Resets all input fields, closes an open profile.
		Profiles.close()
		$("#bird-search-bar").val("")
		$("#poli-search-bar").val("")
		@searchString.bird = ""
		@searchString.poli = ""
		# Remove filtered list of politicians, re-add all of them.
		@_removePolis()
		@_initPoliticianList()

	# Public 
	prepareOpen: ->
		# Temporarily disable click handlers so that no profiles can be opened
		# before the panning is over.
		remove = (root) ->
			root.children('.list-entry').each () ->
				$(@).attr('frozen', true)
		remove @politicianListRoot
		remove @birdListRoot
		# Re-enable the handlers.
		enable = (rootName) ->
			reEnableHandler = ->
				VoicesLists[rootName].children('.list-entry').each () ->
					# Passing `undefined` here is indistinguishable from no second
					# argument, so `false` has to do.
					$(@).attr('frozen', false)
			setTimeout(reEnableHandler, Display.pageMoveDelay * 10)
		enable("politicianListRoot")
		enable("birdListRoot")

	# Public
	open: ->
		# Prepare scroll bars.
		@_handleScroll "bird"
		@_handleScroll "poli"

	_initSearchBars: ->
		# Initializes both search bars.

		# bird search bar
		birdAdd = (birds) -> 
			VoicesLists._displayBirds(VoicesLists.birdListRoot, "voices-list-item", birds)
		birdQualifies = (bird, search) -> 
			bird[Util.addLang("name")].toLowerCase().indexOf(search) isnt -1
		birdRemove = () -> VoicesLists._removeBirds()
		@_initSearchBar("bird", Model.birds, birdAdd, birdRemove, birdQualifies)
		# poli search bar
		poliAdd = (polis) -> 
			VoicesLists._displayPolis(VoicesLists.politicianListRoot, "voices-list-item", polis)
		poliQualifies = (poli, search) ->
			poli.name.toLowerCase().indexOf(search) isnt -1
		poliRemove = () -> VoicesLists._removePolis()
		@_initSearchBar("poli", Model.politicians, poliAdd, poliRemove, poliQualifies)

	# Provides convenient access to scrollbar-related elements.
	_scroll:
		bird:
			top: $("#voices-list-top-blur-bird")
			bot: $("#voices-list-bot-blur-bird")
			list: $("#voices-list-birds")
		poli:
			top: $("#voices-list-top-blur-poli")
			bot: $("#voices-list-bot-blur-poli")
			list: $("#voices-list-politicians")

	_initScrollHandler: () ->
		# Attaches handlers to lists.
		@birdListRoot.scroll () -> VoicesLists._handleScroll("bird")
		@politicianListRoot.scroll () -> VoicesLists._handleScroll("poli")

	_handleScroll: (mode) ->
		# Removes or displays Not-End-Of-List indicators.
		list = @_scroll[mode].list
		top = @_scroll[mode].top
		bot = @_scroll[mode].bot
		maxHeight = list.prop("scrollHeight")
		height = list.height()
		current = list.scrollTop()
		onTop = current == 0
		onBot = current >= maxHeight - height - 1
		top.remove()
		bot.remove()
		list.append(top) unless onTop
		list.append(bot) unless onBot

	# CREATE AND DISPLAY LISTS

	_removePolis: ->
		# Removes all politicians from the list.
		@_removeEntries(@politicianListRoot, ".list-entry")

	_removeBirds: ->
		# Removes all birds from the list.
		@_removeEntries(@birdListRoot, ".list-entry")

	_removeEntries: (root, selector) ->
		# Removes all entries which are children of `root` and are matched by
		# the `selector`.
		root.children(selector).each -> $(this).remove()

	_initPoliticianList: ->
		# Displays all birds. Attach respective handlers.
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
				obj.click () -> 
					frozen = $(@).attr("frozen") is "true"
					Profiles.openPoliticianPage id unless frozen
		@_handleScroll("poli")

	_displayBirds: (root, prefix, list) ->
		handler = (obj, id) -> 
			obj.click () -> 
				frozen = $(@).attr("frozen") is "true"
				Profiles.openBirdPage(id) unless frozen
		Util.createBirdList root, prefix, list, undefined, handler
		@_handleScroll("bird")

	_initBirdList: ->
		# Displays all birds. Attach respective handlers.
		@_displayBirds(@birdListRoot, "voices-list-item", Model.birds)

	_initSearchBar: (id, model, add, remove, qualifies) ->
		# Attaches handler for keystrokes updating the search bars.
		searchBar = $("##{id}-search-bar")
		handler = (event) ->
			oldString = VoicesLists.searchString[id]
			newString = searchBar.val().toLowerCase()
			return if oldString is newString
			VoicesLists.searchString[id] = newString
			remaining = {}
			remaining[id] = entity for id, entity of model when qualifies(entity, newString)
			remove()
			add remaining
		$(document).keyup handler
