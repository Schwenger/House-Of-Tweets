#= require <model.coffee>
#= require <connector.coffee>
#= require <util.coffee>

CitizenUser = 

	_citizenBirdMQ: undefined
	_citizenBirdSelection: undefined
	_dropdownTrigger: undefined
	_dropdownList: undefined

	maxTwitterNameLength: 15

	init: ->
		@_citizenBirdMQ = new Connector(Connector.config.citizenUserQueue, undefined)
		$('#submit-citizen-bird').click(@_submitCitizenBird)
		@_dropdownTrigger = $('#bird-dropdown-button')
		@_dropdownList = $('#bird-dropdown-list')
		@_dropdownTrigger.click @_toggleDropdown
		@translateBirds()
		$('#owntweets').click () -> CitizenUser._closeDropdown()

		$("submit-citizen-bird").click @_submitCitizenBird
		@_resetDropdownTrigger()
		new Connector(Connector.config.acknowledgeQueue, @_consumeFeedback)

	leavePage: ->
		setTimeout (() ->
			CitizenUser._resetDropdownTrigger()
			CitizenUser._closeDropdown()
			$('#citizen-user-name-input').val("")
		), Display.pageMoveDelay

	translateBirds: ->
		@_dropdownList?.children().each(() -> $(@).remove())
		list = $('#bird-dropdown-list')
		for own id, bird of Model.birds 
			do(id, bird) ->
				optionObject = $("<li class='bird-dropdown-entry' value=#{id}>")
				optionObject.text(bird[Util.addLang "name"])
				list.append(optionObject)
				optionObject.click(() -> CitizenUser._selectCitizenBird(id))
		@_resetDropdownTrigger()

	_consumeFeedback: (msg) ->
		if msg.error?
			console.log "Error adding user #{msg.twittername}. Reason: #{msg.error}"
		kind = if msg.error? then "negative" else "positive"
		data = 
			kind: kind
			name: Util.sanitize(msg.twittername[..CitizenUser.maxTwitterNameLength])
			pre: Model.msg.get("#{kind}_feedback_pre")
			post: Model.msg.get("#{kind}_feedback_post")
		template = """
			<div class="entry {{kind}}"> 
      			<div>
        			<span translatestring stringID="{{kind}}_feedback_pre"> {{pre}} </span>
        			<span class="twittername"> {{name}} </span>
        			<span translatestring stringID="{{kind}}_feedback_post"> {{post}} </span>
      			</div>
    		</div>
		"""
		elem = $(Mustache.render(template, data))
		$('#citizen-user-feedback-list').append(elem)
		setTimeout (() -> 
			elem.addClass("fade-out")
			setTimeout (() -> elem.remove()), 1500
		), 10000

	_leave: () ->
		@leavePage()
		$("carousel-control-prev").click()

	_resetDropdownTrigger: ->
		for own id, bird of Model.birds
			@_citizenBirdSelection = id
			@_dropdownTrigger.text(bird[Util.addLang "name"])
			# We are only interested in the first element.
			break
		
	_toggleDropdown: (e) ->
		event = e || window.event
		event.stopPropagation()
		CitizenUser._dropdownTrigger.toggleClass('active')
		CitizenUser._dropdownList.slideToggle(200)

	_closeDropdown: ->
		@_toggleDropdown() if @_dropdownTrigger.hasClass('active')

	_selectCitizenBird: (id) ->
		@_citizenBirdSelection = id
		@_dropdownTrigger.text(Model.birds[id][Util.addLang("name")])
		@_toggleDropdown()
			
	_submitCitizenBird: (event) ->
		event.preventDefault()
		$('#citizen-tweets-switch').prop('checked', false);
		username = $('#citizen-user-name-input').val()[..CitizenUser.maxTwitterNameLength]
		data = {twittername: username, birdid: CitizenUser._citizenBirdSelection}
		CitizenUser._citizenBirdMQ.sendToQueue(data)
		CitizenUser._leave()
		$("#carousel-control-prev").click()

