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
    saver = $("#screensaver-element-0")
    saver.removeClass "invisible"
    saver.addClass "load"
    saver.children().each () -> $(this).addClass "load"
    setTimeout (() -> LanguageController.changeLanguage("german")), Screensaver.config.languageChangeDelay

  stop: ->
    return unless Screensaver.active
    Screensaver.active = false
    saver = $("#screensaver-element-0")
    saver.addClass "invisible"
    saver.removeClass "load"
    saver.children().each () -> $(this).removeClass "load"
    Screensaver.active = -1
    Screensaver.lastTouch = Util.time()
