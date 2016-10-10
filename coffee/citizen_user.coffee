#= require <model.coffee>
#= require <connector.coffee>
#= require <util.coffee>

CitizenUser = 

	_citizenBirdMQ: undefined
	_listRoot: $('.main-gallery')
	_twitterNameInput: $('#citizen-user-name-input')

	maxTwitterNameLength: 15

	init: ->
		@_citizenBirdMQ = new Connector(Connector.config.citizenUserQueue, undefined)
		new Connector(Connector.config.acknowledgeQueue, @_consumeFeedback)

		@_listRoot.flickity({
  			draggable: true
  			freeScroll: true
  			freeScrollFriction: 0.05
  			lazyLoad: true
  			wrapAround: true
  			pageDots: false
		})

		@_initBirdList()
		$(document).keyup () -> CitizenUser._notifySelectButtons()

	leavePage: ->
		setTimeout (() ->
			CitizenUser._twitterNameInput.val("")
		), Display.pageMoveDelay

	translateBirds: ->
		CitizenUser._removeBirds()
		CitizenUser._initBirdList()

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

	_disableSelectButtons: () ->
		for own bid, bird of Model.birds
			btn = $("#citizen-user-select-bird-#{bid}")
			btn.addClass("btn-disabled")
			btn.attr('disabled', true)
	_enableSelectButtons: () ->
		for own bid, bird of Model.birds
			btn = $("#citizen-user-select-bird-#{bid}")
			btn.removeClass("btn-disabled")
			btn.attr('disabled', false)

	_notifySelectButtons: () ->
		enable = $('#citizen-user-name-input').val().length > 0
		if enable then @_enableSelectButtons() else @_disableSelectButtons()

	_submitCitizenBird: (bid) ->
		$('#citizen-tweets-switch').prop('checked', false);
		username = @_twitterNameInput.val()[...CitizenUser.maxTwitterNameLength]
		data = {twittername: username, birdid: bid}
		CitizenUser._citizenBirdMQ.sendToQueue(data)
		CitizenUser._leave()
		$("#carousel-control-prev").click()

	_removeBirds: ->
		@_listRoot.find('.gallery-cell').each () ->
			CitizenUser._listRoot.flickity('remove', $(@))

	_initBirdList: ->
		template = """
			  <div class="gallery-cell">
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
			data = 
				bird: bid
				name: bird[Util.addLang("name")]
				select: Model.msg.get("select")
			entry = $(Mustache.render(template, data))
			@_listRoot.flickity('append', entry)
			entry.find("#citizen-user-select-bird-#{bid}").click (
				() -> CitizenUser._submitCitizenBird(bid)
			)

		@_notifySelectButtons()

