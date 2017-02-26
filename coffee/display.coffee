#= require <model.coffee>
#= require <citizen_user.coffee>
#= require <tweet_controller.coffee>
#= require <voices_lists.coffee>

Display =

	pageMoveDelay: 600

	controls: {
		left: $('#carousel-control-prev')
		right: $('#carousel-control-next')
		down: $("#impressum-button")
		up: $("#impressum-back")
	}

	pages: {
		tweets: $("#tweets")
		impressum: $("#impressum")
	}

	right: {
		color: "sidebar-right-coloring"
		getText: () -> Model.msg.get("own_tweets")
		textContainer: $("#carousel-control-right-text-string")
	}
	left: {
		color: "sidebar-left-coloring"
		getText: () -> Model.msg.get("bird_calls")
		textContainer: $("#carousel-control-left-text-string")
	}

	state: "center" # center, right, left, U1

	# Public
	init: ->
		for own id, ctrl of @controls
			do(id, ctrl) ->
				ctrl.click(() -> Display._trigger(id))

	# Public
	center: ->
		# Displays the center page regardless of the current state.
		switch @state
			when "right" then @controls.left.click()
			when "left" then @controls.right.click()
			when "U1" then @_trigger("up")

	_trigger: (dir) ->
		# Triggers a movement in a specified direction.
		# Assumption: No invalid movement.
		# 
		# TODO: Check for invalid movements, stay if so, warn on console.
		@state = @_delta(@state, dir)
		@_removeSidebars()
		Display.controls["down"].addClass "invisible"

		switch @state
			when "center" 
				@_panUp() if dir is "up" 
			when "U1" then @_panDown()
			when "right" then CitizenUser.prepareOpen()
			when "left" then VoicesLists.prepareOpen()

		timeoutAction = switch @state
			when "center" then -> 
				Display._openCenter()
				VoicesLists.leavePage()
				CitizenUser.leavePage()
			when "right" then -> Display._openSide("right", "left")
			when "left" then -> Display._openSide("left", "right")

		setTimeout(timeoutAction, @pageMoveDelay) if timeoutAction?
				
	_panUp: ->
		# Switches from U1/impress to center.
		$('#carousel').carousel 1 # tweets
		setTimeout (() -> 
			$('#carousel').removeClass "vertical"), Display.pageMoveDelay

	_panDown: ->
		# Switches from center to U1/impress.
		$('#carousel').addClass "vertical"
		$('#carousel').carousel 3 # impressum

	_openSide: (side, otherSide) ->
		# Switches from center page to left/right.
		# In the process, the sidebar's appearances have to be adapted.
		ctrl = @controls[otherSide]
		@_addSidebar(ctrl)

		# invert colors
		ctrl.addClass(@[side].color)
		ctrl.removeClass(@[otherSide].color)

		text = Model.msg.get("back_to_tweets")
		@[otherSide].textContainer.text(text)

		# notify page that it is now opened.
		if side is "left" then VoicesLists.open() else CitizenUser.open()

	_openCenter: ->
		#reset colors & text
		for side in ["right", "left"]
			@controls[side].addClass @[side].color
			@[side].textContainer.text(@[side].getText())
		# reset control elements
		Display.controls["down"].removeClass "invisible"
		@_addSidebars()

	# AUXILIARY
	_removeSidebars: ->
		@controls.left.addClass "invisible"
		@controls.right.addClass "invisible"

	_addSidebars: ->
		@_addSidebar(@controls.left)
		@_addSidebar(@controls.right)

	_addSidebar: (sb) ->
		sb.removeClass "invisible"

	_delta: (state, dir) ->
		# Computes the state transition.
		switch dir
			when "up" then "center"
			when "down" then "U1"
			else (if state is "center" then dir else "center")
