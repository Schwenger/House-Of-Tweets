#= require <global.coffee>
#= require <model.coffee>
#= require <voices_lists.coffee>
#= require <citizen_user.coffee>

class LanguageController 

	@init: (lang) ->
		$("#tweet-list-header").click (-> $("#language-control").removeClass "invisible")
		$("#language-control").click (-> $("#language-control").addClass "invisible")
		LanguageController._addLanguageClickHandler l for l in ["german", "english", "french"]
		LanguageController.changeLanguage(lang) if lang?

	@_addLanguageClickHandler: (lang) ->
		$("##{lang}-flag").click (-> LanguageController.changeLanguage(lang))

	@changeLanguage: (langString) ->
		Global.language = langString
		console.log "Changing language to #{langString}"
		
		$("[translatestring]").each ((index) -> 
			obj = $(this)
			identifier = obj.attr("stringID")
			string = Model.msg.get(identifier)
			obj.text(string)
			)
		VoicesLists.translateBirds()
		translateCitizenBirds()