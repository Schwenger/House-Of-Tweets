#= require <global.coffee>
#= require <util.coffee>
#= require <connector.coffee>
#= require <model.coffee>

_birdPath = (id) ->
	Global.bird_path + id + ".jpg"

_politicianPath = (id) ->
	Global.politician_path + if id? then id else "placeholder.png"

voicesMQ = undefined

changeCitizenBird = (bid, pid) ->
	model.politicians[pid].citizen_bird = bid
	data = {politicianid: pid, birdid: bid}
	sendToQueue(voicesMQ, data)
	closeProfilePage()
	openPoliticianPage pid

prepareVoicesPage = ->
	displayPoliticians $("#voices-list-politicians"), "voices-list-item"
	displayBirds $("#voices-list-birds"), "voices-list-item", false

	$("#profile-back-button-politician").click closeProfilePage
	$("#profile-back-button-bird").click closeProfilePage

	voicesMQ = openConnection(Global.rabbitMQ.citizenBirdQueue, undefined)

updateVoicesPage = ->
	console.log "updating"
	list = $("#voices-list-politicians")
	list.children(".voices-list-entry").each -> $(this).remove()
	displayPoliticians list, "voices-list-item"
	Global.pendingBirdListUpdate = false

	# TODO connection to change bird

# CHANGE BIRD LOGIC

changeBirdHandlerFactory = (bid, pid) ->
	() ->
		closeCitizenBirdSelection(true, bid, pid)

closeCitizenBirdSelection = (save, bid, pid)->
	changeCitizenBird(bid, pid) if save
	$('#cv-and-selection-wrapper').removeClass "invisible"
	$('#change-citizen-bird-wrapper').addClass "invisible"

openCitizenBirdSelection = (bid, pid) ->
	-> 
		root = $("#change-citizen-bird-wrapper")
		o.remove() for o in root.children(".voices-list-entry")
		$('#cv-and-selection-wrapper').addClass "invisible"
		$('#change-citizen-bird-wrapper').removeClass "invisible"
		displayBirds root, "change-bird-list-entry", true, pid

# PROFILE PAGES

closeProfilePage = ->
	$("#voices-list-container").css("opacity", 1)
	$("#voices-profile-container-politician").addClass "invisible"
	$("#voices-profile-container-bird").addClass "invisible"
	closeCitizenBirdSelection(false, 0, 0)

openPoliticianPage = (id) ->
	$("#voices-list-container").css("opacity", 0)
	$("#voices-profile-container-politician").removeClass "invisible"

	poli = Model.politicians[id]

	picObj = $("#voices-profile-picture-politician")
	picObj.css("height", picObj.width() + "px")

	changeButtonObj = $("#voices-profile-citizen-selection-change-button")
	changeButtonObj.off("click")
	changeButtonObj.click openCitizenBirdSelection(poli.citizen_bird, id)

	$("#voices-profile-name-politician").text(poli.name)
	$("#voices-profile-cv-politician").text(poli.cv[Global.langId()])
	imagepath = _politicianPath poli.images?.pathToImage
	$("#voices-profile-picture-politician").attr("src", imagepath)
	$("#voices-profile-self-selection-image-politician").attr("src", _birdPath poli.self_bird)
	$("#voices-profile-citizen-selection-image-politician").attr("src", _birdPath poli.citizen_bird)
	
	citizenBirdName = Model.birds[poli.citizen_bird][Util.addLang "name"] if Model.birds[poli.citizen_bird]?
	$("#voices-profile-citizen-selection-text-politician").text(citizenBirdName)
	selfBirdName = Model.birds[poli.self_bird][Util.addLang "name"]
	$("#voices-profile-self-selection-text-politician").text(selfBirdName)

openBirdPage = (id) ->
	$("#voices-list-container").css("opacity", 0)
	$("#voices-profile-container-bird").removeClass "invisible"

	picObj = $("#voices-profile-picture-bird")
	picObj.css("height", picObj.width() + "px")

	bird = Model.birds[id]
	$("#voices-profile-name-bird").text(bird[Util.addLang "name"])
	$("#voices-profile-cv-bird").text(bird[Util.addLang "cv"])
	$("#voices-profile-picture-bird").attr("src", _birdPath id)

translateBirds = ->
	$("#voices-list-birds").children(".voices-list-entry").each ->
		[head..., id] = $(this).attr("id").split("-")
		newName = Model.birds[id][Util.addLang("name")]
		$(this).find('.first-line').text(newName)


# CREATE AND DISPLAY LISTS

_openPoliticianPageFactory = (id) ->
	() ->
		openPoliticianPage id

_openBirdPageFactory = (id) ->
	() ->
		openBirdPage id

displayPoliticians = (root, prefix) ->
	for own id, p of Model.politicians
		firstLine = p.name
		image = _politicianPath p.images?.pathToThumb
		obj = transformItem id, firstLine, p.party, image, prefix
		root.append obj
		obj.click (_openPoliticianPageFactory(id))

displayBirds = (root, prefix, addon, info) ->
	for own id, b of Model.birds
		image = _birdPath id
		name = b[Util.addLang "name"]
		obj = transformItem id, name, b.latin_name, image, prefix
		handler = changeBirdHandlerFactory id, info if addon
		root.append obj
		obj.click (if addon then handler else _openBirdPageFactory(id))

transformItem = (id, first_line, second_line, image, prefix, addon, info) ->
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


