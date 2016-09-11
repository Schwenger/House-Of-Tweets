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

    setInterval(checkActivation, Screensaver.config.checkFrequency)
    Screensaver.lastTouch = Util.time()

  start: ->
    return if Screensaver.active
    Screensaver.active = true

    # Switch to German.
    toGerman = () -> LanguageController.changeLanguage("german")
    setTimeout(toGerman, Screensaver.config.languageChangeDelay)

    # Center and turn on.
    delay = if Display.state isnt "center" then Display.pageMoveDelay else 0
    Display.center()
    setTimeout(Screensaver._turnOn, delay)

  _turnOn: ->
    saver = $("#screensaver-element-0")
    saver.removeClass "invisible"
    saver.addClass "fade-in"
    saver.children().each () -> $(this).addClass "load"
      
  stop: ->
    return unless Screensaver.active
    Screensaver.active = false
    saver = $("#screensaver-element-0")
    saver.addClass "invisible"
    saver.removeClass "fade-in"
    saver.children().each () -> $(this).removeClass "load"
    Screensaver.lastTouch = Util.time()
