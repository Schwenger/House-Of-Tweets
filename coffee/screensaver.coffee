#= require <util.coffee>
#= require <language_controller.coffee>

Screensaver = 
	active: false
	lastTouch: -1

	config:
		startThreshold: 1500000,
		checkFrequency: 500000,
		languageChangeDelay: 2500

	# Public
	init: ->
		# Initializes the screen saver by setting timeouts and interval checks.
		$(document).click (->
			Screensaver.lastTouch = Util.time()
			Screensaver.stop() if Screensaver.active
		)

		checkActivation = () ->
			Screensaver.start() if Util.time() - Screensaver.lastTouch > Screensaver.config.startThreshold

		setInterval(checkActivation, @config.checkFrequency)
		@lastTouch = Util.time()

	# Public
	start: ->
		# Turns the screen saver on by overlaying the screen with the saver, 
		# changing the language to German and switching to the center page.
		# No-op if already active.
		
		return if @active
		@active = true

		# Switch to German.
		toGerman = () -> LanguageController.changeLanguage("german")
		setTimeout(toGerman, @config.languageChangeDelay)

		# Center and turn on.
		delay = if Display.state isnt "center" then Display.pageMoveDelay else 0
		Display.center()
		setTimeout(@_turnOn, delay)

	_turnOn: ->
		# Overlays the screen saver element.
		saver = $("#screensaver-element-0")
		saver.removeClass "invisible"
		saver.addClass "fade-in"
		saver.children().each () -> $(@).addClass "load"
			
	# Public
	stop: ->
		# Turns the screensaver off by removing the respective element.
		console.log "Inconsistent state of screensaver." unless @active
		@active = false
		saver = $("#screensaver-element-0")
		saver.addClass "invisible"
		saver.removeClass "fade-in"
		saver.children().each () -> $(@).removeClass "load"
		@lastTouch = Util.time()
