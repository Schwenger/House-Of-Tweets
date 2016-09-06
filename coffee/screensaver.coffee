#= require <global.coffee>
#= require <util.coffee>

Screensaver = 
  active: false
  lastTouch: -1

  config:
    duration: 6000000,
    startThreshold: 1500000,
    checkFrequency: 500000,

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
    setTimeout(Screensaver.stop, Screensaver.config.duration)

  stop: ->
    return unless Screensaver.active
    saver = $("#screensaver-element-0")
    saver.addClass "invisible"
    saver.removeClass "load"
    saver.children().each () -> $(this).removeClass "load"
    Screensaver.active = -1
    Screensaver.lastTouch = Util.time()
