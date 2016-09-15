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
		@_initSearchBar()

	update: ->
		# no need to do anything because the profile is re-created each time anyway.
		return

	translateBirds: ->
		VoicesLists._removeBirds()
		VoicesLists._initBirdList()

	leavePage: ->
		Profiles.close()
		_searchString = ""
		$("voices-list-search-bar").val("")

	# SEARCH BAR

	_searchString: ""
	_initSearchBar: ->
		searchBar = $("#voices-list-search-bar")
		handler = (event) ->
			return if VoicesLists._searchString is searchBar.val()
			VoicesLists._searchString = searchBar.val()
			return unless VoicesLists._searchString.length > 2
			pred = (poli) -> 
				poli.name.indexOf(VoicesLists._searchString) isnt -1
			VoicesLists._removePolis()
			remaining = (poli for pid, poli of Model.politicians when pred(poli))
			VoicesLists._display VoicesLists.politicianListRoot, "voices-list-item", remaining
		$(document).keyup handler

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
		@_display(root, prefix, Model.politicians)

	_display: (root, prefix, list) ->
		for own id, p of list
			do(id, p) ->
				firstLine = p.name
				image = Util.politicianPath p.images?.pathToThumb
				obj = VoicesLists._createListEntry id, firstLine, p.party, image, prefix
				root.append obj
				obj.click () -> Profiles.openPoliticianPage id

	_initBirdList: ->
		@_displayBirdList @birdListRoot, "voices-list-item", (id) -> Profiles.openBirdPage(id)

	# NB: This method is called from within profile, thus avoid using @.
	_displayBirdList: (root, prefix, handler) ->
		respName = Util.addLang "name"
		cmp = (a,b) ->
			if a[1][respName] < b[1][respName] then -1
			else if b[1][respName] < a[1][respName] then 1
			else 0
		sortable = ([id, bird] for own id, bird of Model.birds)
		sortable.sort(cmp)
		for [id, b] in sortable
			do(id, b) ->
				image = Util.birdPath id
				obj = VoicesLists._createListEntry id, b[respName], b.latin_name, image, prefix
				root.append obj
				obj.click () -> handler(id)

	_createListEntry: (id, first_line, second_line, image, prefix, addon, info) ->
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


