#= require <global.coffee>
#= require <util.coffee>
#= require <model.coffee>

Display =

	pageMoveDelay: 600

	controls: {
		left: $('#carousel-control-prev')
		right: $('#carousel-control-next')
		down: $("#impressum-button")
		up: $("#impressum-back-button")
	}

	pages: {
		tweets: $("#tweets")
		impressum: $("#impressum")
	}

	right: {
		color: "sidebar-right-coloring"
		text: Model.msg.get("eigeneT")
		textContainer: $("#carousel-control-right-text-string")
	}
	left: {
		color: "sidebar-left-coloring"
		text: Model.msg.get("vogelstimmen")
		textContainer: $("#carousel-control-left-text-string")
	}

	state: "center" # center, right, left, U1, U2

	init: ->
		for own id, ctrl of @controls
			do(id, ctrl) ->
				ctrl.click(() -> Display._trigger(id))

	_trigger: (dir) ->
		@state = @_delta(@state, dir)
		switch dir
			when "up" then @_panUp()
			when "down" then @_panDown()
			else
				@_removeSidebars()
				timeoutAction = switch @state
					when "center" then @_openCenter()
					when "right" then @_openSide("right", "left")
					when "left" then @_openSide("left", "right")
				setTimeout(timeoutAction, @pageMoveDelay)

	_panUp: ->
		@_addSidebars()
		@_resetImpressum()
		TweetController.update()
		@_deactivate(@pages.impressum)
		@_activate(@pages.tweets)

	_panDown: ->
		@_removeSidebars()
		@_deactivate(@pages.tweets)
		@_activate(@pages.impressum)

	_openSide: (side, otherSide) ->
		ctrl = @controls[otherSide]
		@_addSidebar(ctrl)

		# invert colors
		ctrl.addClass(@[side].color)
		ctrl.removeClass(@[otherSide].color)

		text = Model.msg.get("zurückZuT")
		@[otherSide].textContainer.text(text)
		# I'm not entirely certain why we need an explicit return here.
		# W/o, container.text(text)'s will be returned which should be valid as well.
		return

	_openCenter: ->
		#reset colors & text
		for side in ["right", "left"]
			@controls[side].addClass @[side].color
			@[side].textContainer.text(@[side].text)
		@_addSidebars()
		VoicesLists.leavePage()
		CitizenUser.leavePage()
		TweetController.update()

	_resetImpressum: ->
		# "go from U2/U1 to U1"

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
