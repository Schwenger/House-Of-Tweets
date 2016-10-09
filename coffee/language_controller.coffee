#= require <global.coffee>
#= require <model.coffee>
#= require <voices_lists.coffee>
#= require <citizen_user.coffee>
#= require <tweet_controller.coffee>

class LanguageController 

	@init: (lang) ->
		$("#change-language-flag").click (-> 
			newLang = if Global.language is "german" then "english" else "german"
			LanguageController.changeLanguage(newLang)
			)
		LanguageController.changeLanguage(lang)

	@changeLanguage: (langString) ->
		Global.language = langString
		console.log "Changing language to #{langString}"
		
		$("[translatestring]").each ((index) -> 
			obj = $(this)
			identifier = obj.attr("stringID")
			string = Model.msg.get(identifier)
			obj.text(string)
			)

		placeholderPoli = Model.msg.get("search_placeholder_poli")
		placeholderBird = Model.msg.get("search_placeholder_bird")
		$("#voices-list-poli-search-bar").attr("placeholder", placeholderPoli).val("").focus().blur();
		$("#voices-list-bird-search-bar").attr("placeholder", placeholderBird).val("").focus().blur();
		$("#citizen-user-search-bar").attr("placeholder", placeholderBird).val("").focus().blur();
		
		VoicesLists.translateBirds()
		CitizenUser.translateBirds()
		TweetController.translateBirds()