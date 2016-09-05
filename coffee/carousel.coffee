#= require <global.coffee>
#= require <util.coffee>
#= require <model.coffee>

_resetState = (prevCtrl, nextCtrl) ->
	nextCtrl.removeClass("invisible")
	prevCtrl.removeClass("invisible")
	nextCtrl.removeClass "sidebar-voices-coloring"
	prevCtrl.removeClass "sidebar-owntweets-coloring"
	nextCtrl.removeClass "sidebar-owntweets-coloring"
	prevCtrl.removeClass "sidebar-voices-coloring"

_setUpInitialState = (prevCtrl, nextCtrl, prevCtrlTextContainer, nextCtrlTextContainer, prevCtrlTextContainerString, nextCtrlTextContainerString) ->
	prevCtrl.addClass "sidebar-voices-coloring"
	nextCtrl.addClass "sidebar-owntweets-coloring"
	content = Model.msg.get("eigeneT")
	nextCtrlTextContainerString.text(content)
	nextCtrlTextContainer.removeClass "invisible"
	content = Model.msg.get("vogelstimmen")
	prevCtrlTextContainerString.text(content)
	prevCtrlTextContainer.removeClass "invisible"

triggerCarousel = (state, swipeLeft) ->
	prevCtrl = $('#carousel-control-prev')
	prevCtrlTextContainer = $("#carousel-control-prev-text")
	prevCtrlTextContainerString = $("#carousel-control-prev-text-string")
	nextCtrl = $('#carousel-control-next')
	nextCtrlTextContainer = $("#carousel-control-next-text") # includes icons
	nextCtrlTextContainerString = $("#carousel-control-next-text-string")

	newState = _transition(state, swipeLeft)
	# We do not need information about the former state: we just reset everything and set it up new.
	# However, we remove the text and wait for the animation to finish until re-adding it.
	nextCtrlTextContainer.addClass "invisible"
	prevCtrlTextContainer.addClass "invisible"

	if newState is "center" 
		_resetState(prevCtrl, nextCtrl)
		timeoutAction = ->
			_setUpInitialState(
				prevCtrl, nextCtrl, prevCtrlTextContainer, nextCtrlTextContainer, 
				prevCtrlTextContainerString, nextCtrlTextContainerString
				)
	if newState is "left"
		prevCtrl.addClass "invisible"
		nextCtrl.addClass "sidebar-voices-coloring"
		nextCtrl.removeClass "sidebar-owntweets-coloring"
		content = Model.msg.get("zurückZuT")
		timeoutAction = -> 
			nextCtrlTextContainerString.text(content)
			nextCtrlTextContainer.removeClass "invisible"
	if newState is "right"
		nextCtrl.addClass "invisible"
		prevCtrl.addClass "sidebar-owntweets-coloring"
		prevCtrl.removeClass "sidebar-voices-coloring"
		content = Model.msg.get("zurückZuT")
		timeoutAction = ->
			prevCtrlTextContainerString.text(content)
			prevCtrlTextContainer.removeClass "invisible"

	updateVoicesPage() if state is "center" and Global.pendingBirdListUpdate

	timeoutAction = Util.composeFunctions([timeoutAction, closeProfilePage]) if state is "left"
	timeoutAction = Util.composeFunctions([timeoutAction, resetCitizenBird]) if state is "right"
	timeoutAction = Util.composeFunctions([timeoutAction, Global.handleStalledTweets]) if state isnt "center"

	setTimeout timeoutAction, 600
	Global.state = newState

_transition = (state, prev) ->
	if state is "center"
		if prev then "left" else "right"
	else 
		"center"

initCarousel = () ->
	prev = $('#carousel-control-prev')
	next = $('#carousel-control-next')
	prev.click(() -> triggerCarousel(Global.state, true))
	next.click(() -> triggerCarousel(Global.state, false))