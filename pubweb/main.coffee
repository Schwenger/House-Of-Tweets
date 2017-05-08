#= require <birds_de_dyn.coffee>
#= require <birds_en_dyn.coffee>
#= require <template.coffee>

require('../ext/node_modules/jquery-on-infinite-scroll')

BirdFeeder =
	birds: null
	nextBirdIdx: 0

	init: ->
		# TODO: assert(nextBirds is null)
		console.log "Auto-detect language"
		lang_tags = $("ul.navbar-right > li.active img")
		# TODO: assert(len(lang_tags) == 1)
		lang_tag = $(lang_tags[0])
		lang = lang_tag.attr("alt")
		@birds = {"Deutsch": RawBirds_de, "English": RawBirds_en}[lang]
		# TODO: assert(not @birds is undefined)
		# A single cell is 150 (image height) + 52 (text, padding, border)
		#     + 20 (div margin) + 145 (loading anim height)
		#     + (20+10) (loading anim description) = 397 pixels high
		$.onInfiniteScroll((() -> BirdFeeder.push()), { offset: 397 + 20 })
		# Trigger an initial check.  See https://github.com/artsy/jquery-on-infinite-scroll/issues/8
		$(window).trigger('scroll.infinite') for [1..4]

	placeBird: (bid, display, tweet) ->
		console.log "Loadin' moar"
		# Can't use imported "bird_template" function.  Why?
		div_tag = $(bird_template(bid, display, tweet))
		$("#hot-birdslist").append(div_tag)

	push: ->
		# I'm sure there's a proper way to do it.
		if @nextBirdIdx < @birds.length
			[bid, display, tweet] = @birds[@nextBirdIdx]
			console.log @birds[@nextBirdIdx]
			@nextBirdIdx += 1
			BirdFeeder.placeBird(bid, display, tweet)
			# Trigger another check.  See https://github.com/artsy/jquery-on-infinite-scroll/issues/8
			$(window).trigger('scroll.infinite') for [1..4]
		else
			$("#hot-load-gif").remove()
			$.destroyInfiniteScroll()

BirdFeeder.init()
