#= require <model.coffee>
#= require <connector.coffee>
#= require <util.coffee>

CitizenUser = 

	_citizenBirdMQ: undefined
	_listRoot: $('.main-gallery')
	_twitterNameInput: $('#citizen-user-name-input')
	_feedback:
		open: []
		id: 0
		threshold: 100000
	_openFeedback: []


	maxTwitterNameLength: 20

	# Public
	init: ->
		@_citizenBirdMQ = new Connector(Connector.config.citizenUserQueue, undefined)
		new Connector(Connector.config.acknowledgeQueue, @_consumeFeedback)

		# Set up the scrollable bird list.
		@_listRoot.flickity({
  			draggable: true
  			freeScroll: true
  			freeScrollFriction: 0.05
  			lazyLoad: true
  			wrapAround: true
  			pageDots: false
		})

		@_initBirdList()
		# Enable buttons by default.
		$('.flickity-prev-next-button').each () -> $(@).removeProp('disabled')

		$(document).keyup () -> CitizenUser._notifySelectButtons()

	# Public
	leavePage: ->
		# Waits until the citizen user page is invisible, then resets all inputs.
		setTimeout (() ->
			CitizenUser._twitterNameInput.val("")
			CitizenUser._disableSelectButtons()
		), Display.pageMoveDelay

	# Public
	translateBirds: ->
		# Translates the bird names by removing and re-adding them. Adding
		# always selects the currently set language.
		CitizenUser._removeBirds()
		CitizenUser._initBirdList()

	# Public
	open: ->
		# No further initialization.
		$('#citizen-user-name-input').focus()

	# Public 
	prepareOpen: ->
		# No preparation.
		0

	# Public
	translate: ->
		@translateBirds()
		for container in @_feedback.open
			newMsg = container[Util.getLang()]
			$(container.selector).text(newMsg)

	_consumeFeedback: (msg) ->
		# Consumes a message from the feedback queue. That means, with respect
		# to the status, an appropriately colored message field shall be added
		# to the page.
		if msg.reason?
			console.log "**INFO** User: #{msg.twittername}. Status: #{msg.status}. Reason: #{msg.reason}."

		id = 'feedback-container-' + CitizenUser._feedback.id
		CitizenUser._feedback.id = (CitizenUser._feedback.id + 1) % CitizenUser._feedback.threshold

		internal = 
			de: msg.message.de
			en: msg.message.en
			selector: '#' + id

		CitizenUser._feedback.open.push internal
		data = 
			kind: msg.status
			id: id
			message: msg.message[Util.getLang()]
		template = """
			<div class="entry {{kind}}" id="{{id}}"> 
      			{{message}}
    		</div>
		"""

		elem = $(Mustache.render(template, data))
		$('#citizen-user-feedback-list').append(elem)
		setTimeout (() -> 
			CitizenUser._feedback.open.shift() # remove first
			elem.addClass("fade-out")
			setTimeout (() -> elem.remove()), 1500
		), 10000

	_leave: () ->
		# Leave the page without further user interaction.
		@leavePage()
		$('#carousel-control-prev').click()

	_disableSelectButtons: () ->
		# All buttons in the bird list will become disabled.
		for own bid, bird of Model.birds
			btn = $("#citizen-user-select-bird-#{bid}")
			btn.addClass("btn-disabled")
			btn.attr('disabled', true)

	_enableSelectButtons: () ->
		# All buttons in the bird list will become enabled.
		for own bid, bird of Model.birds
			btn = $("#citizen-user-select-bird-#{bid}")
			btn.removeClass("btn-disabled")
			btn.attr('disabled', false)

	_notifySelectButtons: () ->
		# Updates the status of the select buttons in the bird list.
		# When there is no input, disable. Otherwise enable.
		enable = $('#citizen-user-name-input').val().length > 0
		if enable then @_enableSelectButtons() else @_disableSelectButtons()

	_submitCitizenBird: (bid) ->
		# a) Notify backend about new citizen user.
		# b) Turn to center page.
		# c) Enable citizen user tweets on center page.
		TweetController.showAllTweets()
		username = @_twitterNameInput.val()[...CitizenUser.maxTwitterNameLength]
		data = {twittername: username, birdid: bid}
		CitizenUser._citizenBirdMQ.sendToQueue(data)
		CitizenUser._leave()

	_removeBirds: ->
		# Completely empties the bird list.
		@_listRoot.find('.gallery-cell').each () ->
			CitizenUser._listRoot.flickity('remove', $(@))

	_initBirdList: ->
		# Initialized the bird list with all bird in the respective language.
		template = """
			  <div class="gallery-cell" id="citizen-user-select-bird-{{bird}}-entry">
	            <div class="image">
	              <img src="../ext/images/birds/{{bird}}.jpg">
	            </div>
	            <div class="name">
	              {{name}}
	            </div>
	            <div class="btn" id="citizen-user-select-bird-{{bird}}"> 
	              <span translatestring stringID="select"> {{select}} </span>
	            </div>
	          </div>
			"""
		for own bid, bird of Model.birds
			do(bid, bird) ->
				data = 
					bird: bid
					name: bird[Util.addLang("name")]
					select: Model.msg.get("select")
				entry = $(Mustache.render(template, data))
				CitizenUser._listRoot.flickity('append', entry)
				selector = "#citizen-user-select-bird-#{bid}"
				if Global.config.citizen_user_bird_entry_clickable
					selector += "-entry"
				entry.find(selector).click (
					() -> CitizenUser._submitCitizenBird(bid)
				)
		@_notifySelectButtons()

