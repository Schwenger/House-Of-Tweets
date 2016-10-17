#= require <birds_de_dyn.coffee>
#= require <birds_en_dyn.coffee>

require('../ext/node_modules/jquery-on-infinite-scroll')

BirdFeeder =
	birds: null
	nextBirdIdx: 0

	init: ->
		# FIXME: assert(nextBirds is null)
		console.log "Auto-detect language"
		lang_tags = $("ul.navbar-right > li.active img")
		# FIXME: assert(len(lang_tags) == 1)
		lang_tag = $(lang_tags[0])
		lang = lang_tag.attr("alt")
		@birds = {"Deutsch": RawBirds_de, "English": RawBirds_en}[lang]
		# FIXME: assert(not @birds is undefined)
		# A single cell is 150 (image height) + 52 (text, padding, border)
		#     + 20 (div margin) + 145 (loading anim height)
		#     + (20+10) (loading anim description) = 397 pixels high
		$.onInfiniteScroll((() -> BirdFeeder.push()), { offset: 397 + 20 })
		# Trigger an initial check.  See https://github.com/artsy/jquery-on-infinite-scroll/issues/8
		$(window).trigger('scroll.infinite') for [1..4]

	bird_template: (bid, display, tweet) ->
		"""
		<div class="col-xs-12 col-sm-6 col-md-4 col-lg-3 text-center">
			<a href="https://twitter.com/intent/tweet?text=#{tweet}&button_hashtag=HouseOfTweets">
				<img src="imgs/#{bid}.jpg" alt="#{display}" width="200" height="150" />
                <p class="custom-bird-caption">
                    <span class="caption-text">#{display}</span>
                    <span class="tw-widget" style="width: 60px;">
                        <i class="tw-img"></i>
                        <span class="tw-label">Tweet</span>
                    </span>
                </p>
			</a>
		</div>
		"""

	placeBird: (bid, display, tweet) ->
		console.log "Loadin' moar"
		div_tag = $(BirdFeeder.bird_template(bid, display, tweet))
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
