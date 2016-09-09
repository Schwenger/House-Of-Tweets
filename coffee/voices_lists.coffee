#= require <global.coffee>
#= require <util.coffee>
#= require <model.coffee>
#= require <profile.coffee>

VoicesLists = 

	init: ->
		@_displayPoliticians $("#voices-list-politicians"), "voices-list-item"
		@_displayBirdList $("#voices-list-birds"), "voices-list-item", (id) -> Profiles.openBirdPage(id)
		Profiles.init(@_displayBirdList)

	update: ->
		console.log "updating"
		list = $("#voices-list-politicians")
		list.children(".voices-list-entry").each -> $(this).remove()
		@_displayPoliticians list, "voices-list-item"
		Global.pendingBirdListUpdate = false

	translateBirds: ->
		$("#voices-list-birds").children(".voices-list-entry").each ->
			[head..., id] = $(this).attr("id").split("-")
			newName = Model.birds[id][Util.addLang("name")]
			$(this).find('.first-line').text(newName)

	leavePage: ->
		Profiles.close()

	# CREATE AND DISPLAY LISTS

	_displayPoliticians: (root, prefix) ->
		for own id, p of Model.politicians
			do(id, p) ->
				firstLine = p.name
				image = Util.politicianPath p.images?.pathToThumb
				obj = VoicesLists._createListEntry id, firstLine, p.party, image, prefix
				root.append obj
				obj.click () -> Profiles.openPoliticianPage id

	# NB: This method is called from within profile, thus avoid using @.
	_displayBirdList: (root, prefix, handler) ->
		for own id, b of Model.birds
			do(id, b) ->
				image = Util.birdPath id
				name = b[Util.addLang "name"]
				obj = VoicesLists._createListEntry id, name, b.latin_name, image, prefix
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


