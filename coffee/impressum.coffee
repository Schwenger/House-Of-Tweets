#= require <global.coffee>
#= require <util.coffee>
#= require <model.coffee>
#= require <connector.coffee>

prepareImpressum = ->
	$("#impressum-button").click openImpressum
	$("#admin-button").click showSimpleAuth
	$("#simple-auth-button").click simpleAuthentication
	$("#simple-auth-input").keypress((e) -> 
		if e.keyCode is 13 # Enter
			e.preventDefault()
			simpleAuthentication() 
		)
	$("#impressum-back-button").click closeImpressum
	$("#admin-page-back-button").click closeAdminPage

showSimpleAuth = ->
	$("#admin-button").addClass "invisible"
	$("#simple-auth").removeClass "invisible"
	$("#simple-auth-input").focus()

hideSimpleAuth = ->
	$("#admin-button").removeClass "invisible"
	$("#simple-auth").addClass "invisible"
	$("#simple-auth-input").val("")

simpleAuthentication = ->
	uname = $("#simple-auth-input").val()
	openAdminPage() if uname is "admin@houseoftweets.hot" or uname is "admin"
	hideSimpleAuth()

openImpressum = ->
	$("#tweets").removeClass "active"
	$("#carousel-control-prev").addClass "invisible"
	$("#carousel-control-next").addClass "invisible"
	$("#impressum").addClass "active"

closeImpressum = ->
	$("#impressum").removeClass "active"
	$("#tweets").addClass "active"
	$("#carousel-control-prev").removeClass "invisible"
	$("#carousel-control-next").removeClass "invisible"
	hideSimpleAuth
	Global.handleStalledTweets()

openAdminPage = ->
	$("#impressum").removeClass "active"
	$("#admin-page").addClass "active"
	constructAdminPage()

closeAdminPage = ->
	$("#impressum").addClass "active"
	$("#admin-page").removeClass "active"
	destructAdminPage()



# ADMIN PAGE

impressumMQ = undefined

poliChanges = []

addPoli = (e) ->
	e.preventDefault()
	poli = {
		name: $('#new-poli-name').val()
		party: $('#new-poli-party').val()
		cv: $('#new-poli-cv').val()
		twittername: $('#new-poli-twittername').val()
		male: $('#sex-input-male').prop("checked")
		imagelink: $('#new-poli-imageurl').val()
	}
	id = poli.name.toLowerCase().replace(" ", "_") + poli.party.toLowerCase().replace(" ", "_")
	model.politicians[id] = Util.clone(poli)
	poli["remove"] = false
	poli["id"] = id
	poliChanges.push poli
	addRemoveListEntry($('#remove-entry-list-poli'), id, "poli", poli.name, undefined)
	$('#new-poli-name').val("")
	$('#new-poli-party').val("")
	$('#new-poli-cv').val("")
	$('#new-poli-twittername').val("")
	$('#new-poli-imageurl').val("")
	$('#sex-input-male').prop("checked", true)

displayError = (error) ->
	Util.createError(error, 10000)

rollbackExtChanges = (obj) ->
	rollbackChanges obj.values
	displayError(obj.error)

rollbackChanges = (changes) ->
	for change in changes
		if change.remove
			model.politicians[change.id] = change
			delete change.id
			delete change.remove
		else 
			delete model[change.id]


# addBird = (e) ->
# 	e.preventDefault()
# 	bird = {
# 		name: $('#new-bird-name').val()
# 		latin: $('#new-bird-latin').val()
# 		cv: $('#new-bird-cv').val()
# 	}
# 	id = bird.name.toLowerCase().replace(" ", "_")
# 	model.birds[id] = bird
# 	addRemoveListEntry($('#remove-entry-list-bird'), id, "bird", bird.name, undefined)
# 	$('#new-bird-name').val("")
# 	$('#new-bird-latin').val("")
# 	$('#new-bird-cv').val("")

inputValid = ->
	uname = $("#username-input").val()
	if uname?.length < 1
		msg = Model.msg.get("missing_uname")
		return [false, msg]
	pw = $("#password-input").val()
	if pw?.length < 1
		msg = Model.msg.get("missing_pw")
		return [false, msg]
	return [true, undefined]

fetchLoginInfo = () ->
	{uname: $("#username-input").val(), h: Sha256.hash($("#password-input").val())}

assembleData = () ->
	login = {uname: $("#username-input").val(), h: Sha256.hash($("#password-input").val())}
	values = poliChanges
	return {login: login, values: values}

saveChanges = (e) ->
	e.preventDefault()
	data = assembleData()
	sendToQueue(impressumMQ, data)
	poliChanges = []
	updateVoicesPage()

prepareAdminPage = () ->
	impressumMQ = new Connector(Global.rabbitMQ.persistQueue, undefined)
	ackMQ = new Connector(Global.rabbitMQ.acknowledgeQueue, rollbackExtChanges)
	$('#add-poli-button').click addPoli
	# $('#add-bird-button').click addBird
	$("#save-changes-button").click saveChanges

constructAdminPage = ->
	vivifyRemoveLists()

vivifyRemoveLists = ->
	vivifyRemoveList("poli", "name", undefined, model.politicians)
	# vivifyRemoveList("bird", "name", undefined, model.birds)

getRespectiveList = (item) ->
		kind = item.attr("kind")
		kind = "politician" if kind is "poli"
		model[kind + "s"]

_deleteClickFactory = (id) ->
	() ->
		entry = $("#" + id)
		list = getRespectiveList entry
		id = entry.attr("value")
		poli = Util.clone(list[id])
		poli["remove"] = true
		poli["id"] = id
		poliChanges.push poli
		delete list[id]
		entry.parent().remove()

addRemoveListEntry = (list, id, listId, v1, v2) ->
	iconId = "remove-list-entry-icon-#{id}"
	entry = $("<div class='remove-list-entry'>")
	icon = $("<i class='fa fa-trash' kind='#{listId}' value='#{id}' id='#{iconId}'>")
	text = $("<span class='name'>")

	content = v1
	content += " " + v2 if v2?
	entry.append(icon)
	text.text(content)
	entry.append(text)
	list.append(entry)

	icon.click(_deleteClickFactory iconId)

vivifyRemoveList = (listId, attr1, attr2, modellist) ->
	list = $("#remove-entry-list-#{listId}")
	for own id, item of modellist
		addRemoveListEntry(list, id, listId, item[attr1], item[attr2])

mortifyRemoveLists = ->
	$(".remove-list-entry").each(() -> $(this).remove())

destructAdminPage = ->
	mortifyRemoveLists()
	rollbackChanges(poliChanges)
	poliChanges = []