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

		@_initSearchbar()
		@_initBirdList()

		$("submit-citizen-bird").click @_submitCitizenBird
		new Connector(Connector.config.acknowledgeQueue, @_consumeFeedback)

	leavePage: ->
		setTimeout (() ->
			$('#citizen-user-name-input').val("")
		), Display.pageMoveDelay

	translateBirds: ->
		CitizenUser._removeBirds()
		CitizenUser._initBirdList()
		# TODO translate buttons

	_initSearchbar: ->
		# TODO

	_removeBirds: ->
		# TODO

	_initBirdList: ->
		root = $('#citizen-user-bird-list')
		prefix = 'citizen-user-list-item'
		addon = (id) -> "<div class='select btn'> Auswählen </div>"
		addClickHandlers = (obj, id) ->
			obj.click () ->
				c = "list-entry-selected"
				root.children().each () -> $(@).removeClass(c)
				obj.addClass c
				CitizenUser._citizenBirdSelection = id
				console.log CitizenUser._citizenBirdSelection
		Util.createBirdList(root, prefix, Model.birds, addon, addClickHandlers)
		root.children()[0].click()

	_consumeFeedback: (msg) ->
		if msg.error?
			console.log "Error adding user #{msg.twittername}. Reason: #{msg.error}"
		kind = if msg.error? then "negative" else "positive"
		data = 
			kind: kind
			name: Util.sanitize(msg.twittername[...CitizenUser.maxTwitterNameLength])
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
			
	_submitCitizenBird: (event) ->
		event.preventDefault()
		$('#citizen-tweets-switch').prop('checked', false);
		username = $('#citizen-user-name-input').val()[...CitizenUser.maxTwitterNameLength]
		data = {twittername: username, birdid: CitizenUser._citizenBirdSelection}
		CitizenUser._citizenBirdMQ.sendToQueue(data)
		CitizenUser._leave()
		$("#carousel-control-prev").click()

