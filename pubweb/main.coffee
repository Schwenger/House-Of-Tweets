#= require <birds_de_dyn.coffee>
#= require <birds_en_dyn.coffee>

require('../ext/node_modules/jquery-on-infinite-scroll')

###
	<!-- &url=https%3A%2F%2FHouseOfTweets.github.io -->

		<div class="col-xs-12 col-sm-6 col-md-4 col-lg-3 text-center">
			<a href="https://twitter.com/intent/tweet?text=#{name}&button_hashtag=HouseOfTweets">
				<img src="imgs/#{bid}.jpg" alt="#{name}" width="200" height="150">
				<p>#{name} #HouseOfTweets</p>
			</a>
		</div>
###

placeBird = (name, bid) ->
	console.log "Loadin' moar"
	# Although I call it "_tag", it's always a jQuery wrapped tag, not a "raw" tag.
	img_tag = $("<img src=\"imgs/#{bid}.jpg\" alt=\"#{name}\" width=\"200\" height=\"150\">")
	p_tag = $("<p class=\"custom-bird-caption\">")
	# TODO: Why can't I just write the text in the jQuery call?
	p_tag.text("#{name} #HouseOfTweets")
	a_tag = $("<a>")
	name_for_href = encodeURIComponent(name)
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
		# A single cell is ${image height} + 52 = 202 pixels high
		# (unless there's word wrap, but we'll assume there isn't)
		$.onInfiniteScroll((() -> BirdFeeder.push()), { offset: 202 + 20 })

	push: ->
		# I'm sure there's a proper
		if @nextBirdIdx < @birds.length
			[bid, name] = @birds[@nextBirdIdx]
			@nextBirdIdx += 1
			placeBird(name, bid)
		else
			$.destroyInfiniteScroll()

BirdFeeder.init()
