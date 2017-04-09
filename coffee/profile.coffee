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
		# Turn artist's image off
		imageSwitch = $("#picture-artist-image-switch")
		imageSwitch.prop('checked', false)
		imageSwitch.change @_changeArtStyleHandler

	# CHANGE IMAGE DISPLAY

	_changeArtStyleHandler: ->
		drawing = $(@).prop('checked')
		Profiles._changeArtStyle(drawing)

	_changeArtStyle: (drawing) ->
		# Applies change in the display mode by turning photos on or off.
		if drawing 
			Profiles._switchVisibility(Profiles.birdDrawing, Profiles.birdPhoto)
		else 
			Profiles._switchVisibility(Profiles.birdPhoto, Profiles.birdDrawing)

	_switchVisibility: (vis, invis) ->
		# Makes `vis` invisible and `invis` visible.
		invis.addClass "invisible"
		vis.removeClass "invisible"

	# CHANGE BIRD LOGIC

	# Public
	changeCitizenBird: (bid, pid) ->
		# Applies a change in citizen bird for a politician by sending a message
		# to the queue.
		Model.politicians[pid].citizen_bird = bid
		data = {politicianid: pid, birdid: bid}
		@voicesMQ.sendToQueue(data)
		# re-open profile to display changes
		@close()
		@openPoliticianPage pid

	# Public
	closeCitizenBirdSelection: (bid, pid)->
		# Closes the list of birds to chose from for a politician.
		$('#cv-and-selection-wrapper').removeClass "invisible"
		$('#change-citizen-bird-wrapper').addClass "invisible"

	# Public
	openCitizenBirdSelection: (bid, pid) ->
		# Opens the list of birds to chose from for a politician.
		root = $("#change-citizen-bird-wrapper")
		# prepare list
		o.remove() for o in root.children(".list-entry")
		$('#cv-and-selection-wrapper').addClass "invisible"
		$('#change-citizen-bird-wrapper').removeClass "invisible"

		# prepare list entries
		addon = (id) -> "<div class='select-citizen-bird-button btn'> #{Model.msg.get('select')} </div>"
		handler = (bid) -> 
			Profiles.changeCitizenBird(bid, pid)
			Profiles.closeCitizenBirdSelection
		addClickHandler = (obj, bid) ->
			obj.click () -> handler(bid)
		prefix = "change-bird-list-entry"

		# Put entries in list.
		Util.createBirdList root, prefix, Model.birds, addon, addClickHandler

	# PROFILE PAGE

	_licenseString: (obj) ->
		# Puts the appropriate license information together. Language sensitive.
		intro = if Global.language is "german" then "bereitgestellt durch: " else "provided by: "
		res = switch obj.license
			when "unknown-bundestag" then intro + "Bundestag"
			when "custom-linke" then intro + "Linke"
			when "custom-gruene" then intro + "Grüne"
			when "custom-spd" then intro + "SPD"
			else obj.license
		res += "\n" + obj.copyright if obj.copyright?
		res

	# Public
	close: ->
		# Closes the currently open profile page.
		Profiles.closeCitizenBirdSelection()
		$("#voices-lists-wrapper").css("opacity", 1)
		$("#voices-profile-container-politician").addClass "invisible"
		$("#voices-profile-container-bird").addClass "invisible"
		Profiles._switchVisibility(Profiles.birdPhoto, Profiles.birdDrawing)

	# Public
	openPoliticianPage: (id) ->
		# Opens and sets up one politician's profile page. 
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
		cv = poli.cv[Global.langId()]
		cv = cv.replace("  ", "<br>")
		# CV data is from backend and thus assume to be sane.
		$("#voices-profile-cv-politician").html(cv)
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

	# Public
	openBirdPage: (id) ->
		# Opens and sets up one birds's profile page. 
		$("#voices-lists-wrapper").css("opacity", 0)
		$("#voices-profile-container-bird").removeClass "invisible"

		bird = Model.birds[id]

		# picture
		picObj = $("#voices-profile-picture-bird")
		picObj.css("height", picObj.width() + "px")
		picObjDrawing = $("#voices-profile-picture-bird-drawing")
		picObjDrawing.css("height", picObj.width() + "px")

		# license
		imgSrcObj = $("#voices-profile-picture-bird-src")
		license = Profiles._licenseString(bird.img) # TODO
		imgSrcObj.text(license)

		$("#voices-profile-name-bird").text(bird[Util.addLang "name"])
		$("#voices-profile-cv-bird").text(bird[Util.addLang "cv"])
		$("#voices-profile-picture-bird").attr("src", Util.birdPath id)
		
		if Global.config.allow_bird_drawings and Model.birds[id].has_drawing
			$("#bird-photo-switch-container").removeClass "invisible"
			$("#voices-profile-picture-bird-drawing").attr("src", Util.birdPath(id, "-drawing"))
			imageSwitch = $("#picture-artist-image-switch")
			showDrawing = imageSwitch.prop('checked')
			@_changeArtStyle(showDrawing)
		else
			$("#bird-photo-switch-container").addClass "invisible" 

