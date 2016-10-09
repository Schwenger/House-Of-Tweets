#= require <birds_de_dyn.coffee>
#= require <birds_en_dyn.coffee>

require('../ext/node_modules/jquery-on-infinite-scroll')

###
	<!-- &url=https%3A%2F%2FHouseOfTweets.github.io -->

		<div class="col-xs-12 col-sm-6 col-md-4 col-lg-3 text-center">
            <a href="https://twitter.com/intent/tweet?text={tweet}&button_hashtag=HouseOfTweets">
                <img src="imgs/{bid}.jpg" alt="{display}" width="200" height="150" />
                <p class="custom-bird-caption">{display} #HouseOfTweets</p>
            </a>
        </div>
###

placeBird = (bid, display, tweet) ->
	console.log "Loadin' moar"
	# Although I call it "_tag", it's always a jQuery wrapped tag, not a "raw" tag.
	img_tag = $("<img src=\"imgs/#{bid}.jpg\" alt=\"#{display}\" width=\"200\" height=\"150\">")
	p_tag = $("<p class=\"custom-bird-caption\">")
	# TODO: Why can't I just write the text in the jQuery call?
	p_tag.text("#{display} #HouseOfTweets")
	a_tag = $("<a>")
	name_for_href = encodeURIComponent(tweet)
	a_tag.attr("href", "https://twitter.com/intent/tweet?text=#{name_for_href}&button_hashtag=HouseOfTweets")
	a_tag.append(img_tag)
	a_tag.append(p_tag)
	div_tag = $('<div class="col-xs-12 col-sm-6 col-md-4 col-lg-3 text-center">')
	div_tag.append(a_tag)
	$("#hot-birdslist").append(div_tag)

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

	push: ->
		# I'm sure there's a proper way to do it.
		if @nextBirdIdx < @birds.length
			[bid, display, tweet] = @birds[@nextBirdIdx]
			console.log @birds[@nextBirdIdx]
			@nextBirdIdx += 1
			placeBird(bid, display, tweet)
			# Trigger another check.  See https://github.com/artsy/jquery-on-infinite-scroll/issues/8
			$(window).trigger('scroll.infinite') for [1..4]
		else
			$("#hot-load-gif").remove()
			$.destroyInfiniteScroll()

BirdFeeder.init()
