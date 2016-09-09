#= require <model.coffee>
#= require <connector.coffee>
#= require <util.coffee>

CitizenUser = 

	_citizenBirdMQ: undefined
	_citizenBirdSelection: undefined
	_dropdownTrigger: undefined
	_dropdownList: undefined

	init: ->
		# attach handler to save button
		@_citizenBirdMQ = new Connector(Connector.config.citizenUserQueue, undefined)
		@_vivifyCitizenBirdsList()
		$('#submit-citizen-bird').click(@_submitCitizenBird)
		@_dropdownTrigger = $('#bird-dropdown-button')
		@_dropdownList = $('#bird-dropdown-list')

		@_dropdownTrigger.click @_toggleDropdown

		$("submit-citizen-bird").click @_submitCitizenBird
		@_resetDropdownTrigger()

	leavePage: ->
		@_resetDropdownTrigger()
		@_closeDropdown()
		$('#citizen-user-name-input').val("")

	translateBirds: ->
		@_dropdownList?.children().each(() -> $(this).remove())
		list = $('#bird-dropdown-list')
		for own id, bird of Model.birds 
			optionObject = $("<li class='bird-dropdown-entry' value=#{id}>")
			optionObject.text(bird[Util.addLang "name"])
			list.append(optionObject)
			optionObject.click(() -> CitizenUser._selectCitizenBird(id))
		@_resetDropdownTrigger()

	_leave: () ->
		@leavePage()
		$("carousel-control-prev").click()

	_resetDropdownTrigger: ->
		for own id, bird of Model.birds
			@_citizenBirdSelection = id
			@_dropdownTrigger.text(bird[Util.addLang "name"])
			# We are only interested in the first element.
			break
		
	_toggleDropdown: ->
		CitizenUser._dropdownTrigger.toggleClass('active')
		CitizenUser._dropdownList.slideToggle(200)

	_closeDropdown: ->
		@_toggleDropdown() if @_dropdownTrigger.hasClass('active')

	_selectCitizenBird: (id) ->
		@_citizenBirdSelection = id
		@_dropdownTrigger.text(Model.birds[id][Util.addLang("name")])
		@_toggleDropdown()

	_vivifyCitizenBirdsList: ->
		list = $('#bird-dropdown-list')
		for own id, bird of Model.birds 
			option_object = $("<li class='bird-dropdown-entry' value=#{id}>")
			option_object.text(bird[Util.addLang "name"])
			list.append(option_object)
			option_object.click (() -> selectCitizenBird(id))
			
	_submitCitizenBird: (event) ->
		event.preventDefault()
		username = $('#citizen-user-name-input').val()
		data = {twittername: username, birdid: CitizenUser._citizenBirdSelection}
		CitizenUser._citizenBirdMQ.sendToQueue(data)
		CitizenUser._leave()
		$("#carousel-control-prev").click()

