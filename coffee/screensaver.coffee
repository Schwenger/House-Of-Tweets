#= require <util.coffee>
#= require <language_controller.coffee>

Screensaver = 
	active: false
	lastTouch: -1

	config:
		startThreshold: 1500000,
		checkFrequency: 500000,
		languageChangeDelay: 2500

	init: ->
		$(document).click (->
			Screensaver.lastTouch = Util.time()
			Screensaver.stop()
		)

		checkActivation = () ->
			Screensaver.start() if Util.time() - Screensaver.lastTouch > Screensaver.config.startThreshold

		setInterval(checkActivation, @config.checkFrequency)
		@lastTouch = Util.time()

	start: ->
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
		saver = $("#screensaver-element-0")
		saver.removeClass "invisible"
		saver.addClass "fade-in"
		saver.children().each () -> $(@).addClass "load"
			
	stop: ->
		console.log "Inconsistent state of screensaver." unless @active
		@active = false
		saver = $("#screensaver-element-0")
		saver.addClass "invisible"
		saver.removeClass "fade-in"
		saver.children().each () -> $(@).removeClass "load"
		@lastTouch = Util.time()
