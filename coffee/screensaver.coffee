#= require <global.coffee>
#= require <util.coffee>

class Screensaver

  active: false
  lastTouch: -1

  @config:
    duration: 6000000,
    startThreshold: 1500000,
    checkFrequency: 500000,

  constructor: ->
    $(document).click (->
      @lastTouch = Util.time()
      @stop()
    )
    setInterval (->
      @start() if Util.time() - @lastTouch > Screensaver.config.startThreshold
    ), Screensaver.config.checkFrequency
    @lastTouch = Util.time()

start = ->
  return if @active
  @active = 0 # we only have one screen saver, type 0
  saver = $("#screensaver-element-#{r}")
  saver.removeClass "invisible"
  saver.addClass "load"
  saver.children().each () -> $(this).addClass "load"
  setTimeout(@stop, Screensaver.config.duration)

stop = ->
  return unless @active
  saver = $("#screensaver-element-0")
  saver.addClass "invisible"
  saver.removeClass "load"
  saver.children().each () -> $(this).removeClass "load"
  @active = -1
  @lastTouch = Util.time()
