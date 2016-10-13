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
		getText: () -> Model.msg.get("bird_calls")
		textContainer: $("#carousel-control-right-text-string")
	}
	left: {
		color: "sidebar-left-coloring"
		getText: () -> Model.msg.get("bird_calls")
		textContainer: $("#carousel-control-left-text-string")
	}

	state: "center" # center, right, left, U1

	init: ->
		for own id, ctrl of @controls
			do(id, ctrl) ->
				ctrl.click(() -> Display._trigger(id))

	center: ->
		switch @state
			when "right" then @controls.left.click()
			when "left" then @controls.right.click()
			when "U1" then @_trigger("up")

	_trigger: (dir) ->
		@state = @_delta(@state, dir)
		switch dir
			when "up" then @_panUp()
			when "down" then @_panDown()
			else
				@_removeSidebars()
				timeoutAction = switch @state
					when "center" then () -> Display._openCenter()
					when "right" then () -> Display._openSide("right", "left")
					when "left" then () -> Display._openSide("left", "right")
				setTimeout(timeoutAction, @pageMoveDelay)

	_panUp: ->
		@_addSidebars()
		$('#impressum').slideUp() 

	_panDown: ->
		@_removeSidebars()
		$('#impressum').slideDown() 

	_openSide: (side, otherSide) ->
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
		@_addSidebars()
		VoicesLists.leavePage()
		CitizenUser.leavePage()

	# AUXILIARY
	_removeSidebars: ->
		@controls.left.addClass "invisible"
		@controls.right.addClass "invisible"

	_addSidebars: ->
		@_addSidebar(@controls.left)
		@_addSidebar(@controls.right)

	_addSidebar: (sb) ->
		sb.removeClass "invisible"

	_activate: (page) ->
		page.addClass "active"

	_deactivate: (page) ->
		page.removeClass "active"

	_delta: (state, dir) ->
		switch dir
			when "up" then "center"
			when "down" then "U1"
			else (if state is "center" then dir else "center")
