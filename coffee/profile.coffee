#= require <util.coffee>
#= require <connector.coffee>
#= require <model.coffee>
#= require <global.coffee>

Profiles =

	voicesMQ: undefined

	birdPhoto: $("#voices-profile-picture-bird")
	birdDrawing: $("#voices-profile-picture-bird-drawing")

	init: ->
		@voicesMQ = new Connector(Connector.config.citizenBirdQueue, undefined)
		$("#profile-back-button-politician").click @close
		$("#profile-back-button-bird").click @close
		$("#picture-artist-image-switch").click @_changeArtStyle

	# CHANGE IMAGE DISPLAY

	_changeArtStyle: () ->
		picture = $(@).prop('checked')
		if picture 
			Profiles._switchVisibility(Profiles.birdPhoto, Profiles.birdDrawing)
		else 
			Profiles._switchVisibility(Profiles.birdDrawing, Profiles.birdPhoto)

	_switchVisibility: (vis, invis) ->
		invis.addClass "invisible"
		vis.removeClass "invisible"

	# CHANGE BIRD LOGIC

	changeCitizenBird: (bid, pid) ->
		Model.politicians[pid].citizen_bird = bid
		data = {politicianid: pid, birdid: bid}
		@voicesMQ.sendToQueue(data)
		# re-open profile to display changes
		@close()
		@openPoliticianPage pid

	closeCitizenBirdSelection: (bid, pid)->
		$('#cv-and-selection-wrapper').removeClass "invisible"
		$('#change-citizen-bird-wrapper').addClass "invisible"

	openCitizenBirdSelection: (bid, pid) ->
		root = $("#change-citizen-bird-wrapper")
		# prepare list
		o.remove() for o in root.children(".voices-list-entry")
		$('#cv-and-selection-wrapper').addClass "invisible"
		$('#change-citizen-bird-wrapper').removeClass "invisible"

		# prepare new list entries
		addon = (id) -> "<div class='button btn'> #{Model.msg.get('select')} </div>"
		handler = (bid) -> 
			Profiles.changeCitizenBird(bid, pid)
			Profiles.closeCitizenBirdSelection
		addClickHandler = (obj, bid) ->
			obj.find('.button').each () -> $(@).click(() -> handler(bid))
		prefix = "change-bird-list-entry"
		Util.createBirdList root, prefix, Model.birds, addon, addClickHandler

	# PROFILE PAGE

	_licenseString: (obj) ->
		intro = if Global.language is "german" then "bereitgestellt durch: " else "provided by: "
		res = switch obj.license
			when "unknown-bundestag" then intro + "Bundestag"
			when "custom-linke" then intro + "Linke"
			when "custom-gruene" then intro + "Grüne"
			when "custom-spd" then intro + "SPD"
			else obj.license
		res += "\n" + obj.copyright if obj.copyright?
		res

	close: ->
		Profiles.closeCitizenBirdSelection()
		$("#voices-lists-wrapper").css("opacity", 1)
		$("#voices-profile-container-politician").addClass "invisible"
		$("#voices-profile-container-bird").addClass "invisible"
		Profiles._switchVisibility(Profiles.birdPhoto, Profiles.birdDrawing)

	openPoliticianPage: (id) ->
		$("#voices-lists-wrapper").css("opacity", 0)
		$("#voices-profile-container-politician").removeClass "invisible"

		poli = Model.politicians[id]

		picObj = $("#voices-profile-picture-politician")
		picObj.css("height", picObj.width() + "px")

		changeButtonObj = $("#voices-profile-citizen-selection-change-button")
		changeButtonObj.off("click")
		changeButtonObj.click () -> Profiles.openCitizenBirdSelection(poli.citizen_bird, id)

		# NAME
		$("#voices-profile-name-politician").text(poli.name)

		# CV
		$("#voices-profile-cv-politician").text(poli.cv[Global.langId()])
		cvSrcObj = $("#voices-profile-cv-politician-src")
		cvSrcObj.text(if poli.cv.src? then poli.cv.src else "")

		# IMAGE
		imagepath = Util.politicianPath poli.images?.pathToImage
		$("#voices-profile-picture-politician").attr("src", imagepath)
		imgSrcObj = $("#voices-profile-picture-politician-src")
		license = Profiles._licenseString(poli.images)
		imgSrcObj.text(license)
		$("#voices-profile-self-selection-image-politician").attr("src", Util.birdPath poli.self_bird)
		$("#voices-profile-citizen-selection-image-politician").attr("src", Util.birdPath poli.citizen_bird)
		
		# BIRDS
		selectionContainer = $("#voices-bird-selection-container")
		if(poli.twittering?)
			selectionContainer.removeClass "invisible"
			citizenBirdName = Model.birds[poli.citizen_bird][Util.addLang "name"] if Model.birds[poli.citizen_bird]?
			$("#voices-profile-citizen-selection-text-politician").text(citizenBirdName)
			selfBirdName = Model.birds[poli.self_bird][Util.addLang "name"]
			$("#voices-profile-self-selection-text-politician").text(selfBirdName)
		else
			selectionContainer.addClass "invisible"

	openBirdPage: (id) ->
		$("#voices-lists-wrapper").css("opacity", 0)
		$("#voices-profile-container-bird").removeClass "invisible"

		picObj = $("#voices-profile-picture-bird")
		picObj.css("height", picObj.width() + "px")
		picObjDrawing = $("#voices-profile-picture-bird-drawing")
		picObjDrawing.css("height", picObj.width() + "px")

		bird = Model.birds[id]
		$("#voices-profile-name-bird").text(bird[Util.addLang "name"])
		$("#voices-profile-cv-bird").text(bird[Util.addLang "cv"])
		$("#voices-profile-picture-bird").attr("src", Util.birdPath id)
		
		if Model.birds[id].has_drawing
			$("#bird-photo-switch-container").removeClass "invisible"
			$("#voices-profile-picture-bird-drawing").attr("src", Util.birdPath(id, "-drawing"))
		else
			$("#bird-photo-switch-container").addClass "invisible" 

