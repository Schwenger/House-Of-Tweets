#= require <global.coffee>
#= require <util.coffee>
#= require <connector.coffee>
#= require <model.coffee>
#= require <profile.coffee>

VoicesLists = 

	voicesMQ: undefined
	profiles: undefined
	init: ->
		VoicesLists.voicesMQ = new Connector(Global.rabbitMQ.citizenBirdQueue, undefined)
		VoicesLists.profiles = new Profiles(VoicesLists.voicesMQ, @_displayBirds)

		@_displayPoliticians $("#voices-list-politicians"), "voices-list-item"
		@_displayBirds $("#voices-list-birds"), "voices-list-item", false

	update: ->
		console.log "updating"
		list = $("#voices-list-politicians")
		list.children(".voices-list-entry").each -> $(this).remove()
		@displayPoliticians list, "voices-list-item"
		Global.pendingBirdListUpdate = false

	translateBirds: ->
		$("#voices-list-birds").children(".voices-list-entry").each ->
			[head..., id] = $(this).attr("id").split("-")
			newName = Model.birds[id][Util.addLang("name")]
			$(this).find('.first-line').text(newName)

	# CREATE AND DISPLAY LISTS

	_openPoliticianPageFactory: (id) ->
		() ->
			VoicesLists.profiles.openPoliticianPage id

	_openBirdPageFactory: (id) ->
		() ->
			VoicesLists.profiles.openBirdPage id

	_changeBirdFactory: (bid, pid) ->
		() ->
			VoicesLists.profiles.changeCitizenBird(bid, pid, true)

	_displayPoliticians: (root, prefix) ->
		for own id, p of Model.politicians
			firstLine = p.name
			image = Util.politicianPath p.images?.pathToThumb
			obj = @_createListEntry id, firstLine, p.party, image, prefix
			root.append obj
			obj.click (@_openPoliticianPageFactory(id))

	_displayBirds: (root, prefix, addon, info) ->
		for own id, b of Model.birds
			image = Util.birdPath id
			name = b[Util.addLang "name"]
			obj = VoicesLists._createListEntry id, name, b.latin_name, image, prefix
			handler = VoicesLists._changeBirdFactory id, info if addon
			root.append obj
			obj.click (if addon then handler else @_openBirdPageFactory(id))

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


