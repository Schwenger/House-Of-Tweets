#= require <global.coffee>
#= require <model.coffee>
#= require <voices_lists.coffee>
#= require <citizen_user.coffee>
#= require <tweet_controller.coffee>

# There is no need to have a class here; there can be only one anyway.
class LanguageController 

	# Public
	@init: (lang) ->
		# Initialize the language flag on center page, set language to German.
		$("#change-language-flag").click (-> 
			newLang = if Global.language is "german" then "english" else "german"
			LanguageController.changeLanguage(newLang)
			)
		LanguageController.changeLanguage(lang)

	# Public
	@changeLanguage: (langString) ->
		# Changes the language of all elements of the page and notifies the 
		# respective controllers about the change.
		
		Global.language = langString
		console.log "Changing language to #{langString}"
		
		# Seek out every HTML element labeled as translate string and replace 
		# the text with respect to the new language.
		$("[translatestring]").each ((index) -> 
			obj = $(this)
			identifier = obj.attr("stringID")
			string = Model.msg.get(identifier)
			obj.html(string)
			)

		# Placeholders are no "real" HTML elements, so treat them separately.
		placeholderPoli = Model.msg.get("search_placeholder_poli")
		placeholderBird = Model.msg.get("search_placeholder_bird")
		$("#poli-search-bar").attr("placeholder", placeholderPoli).val("").focus().blur();
		$("#bird-search-bar").attr("placeholder", placeholderBird).val("").focus().blur();
		$("#citizen-search-bar").attr("placeholder", placeholderBird).val("").focus().blur();
		
		# Notify each page controller about the translation. Note that the 
		# impress is controller-less and is thus not notified.
		VoicesLists.translateBirds()
		CitizenUser.translateBirds()
		TweetController.translateBirds()