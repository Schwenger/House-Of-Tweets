#= require <birds.coffee>

require('../ext/node_modules/jquery-on-infinite-scroll')

###
	<!-- &url=https%3A%2F%2FHouseOfTweets.github.io -->

		<div class="col-xs-12 col-sm-6 col-md-4 col-lg-3 text-center">
			<a href="https://twitter.com/intent/tweet?text=Ara&button_hashtag=HouseOfTweets">
				<!-- &url=https%3A%2F%2FHouseOfTweets.github.io -->
				<img src="https://placekitten.com/200/150" alt="Ara" />
				<span>Tweet #HouseOfTweets</span>
			</a>
		</div>
###

placeBird = (name, bid) ->
	# Although I call it "_tag", it's always a jQuery wrapped tag, not a "raw" tag.
	img_tag = $("<img>")
	img_tag.src("imgs/#{bid}")
	img_tag.alt(name)
	span_tag = $("<span>")
	span_tag.text("#{name} #HouseOfTweets")
	a_tag = $("a")
	name_for_href = encodeURIComponent(name)
	a_tag.href("https://twitter.com/intent/tweet?text=#{name_for_href}&button_hashtag=HouseOfTweets")
	a_tag.append(img_tag)
	a_tag.append(span_tag)
	div_tag = $("<div class=\"col-xs-12 col-sm-6 col-md-4 col-lg-3 text-center\">")
	div_tag.append(a_tag)
	$("#hot-birdslist").append(div_tag)

placePseudoBird = ->
	placeBird("Weißkopfseeländer", "argh")

$.onInfiniteScroll(placePseudoBird, { offset: 100 })
