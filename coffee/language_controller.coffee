#= require <global.coffee>
#= require <model.coffee>
#= require <voices_controller.coffee>
#= require <citizen_birds.coffee>

$("#tweet-list-header").click (-> $("#language-control").removeClass "invisible")

$("#language-control").click (->	
	$("#language-control").addClass "invisible"
	)

addLanguageClickHandler = (lang) ->
	$("##{lang}-flag").click (-> changeLanguage(lang))

addLanguageClickHandler lang for lang in ["german", "english", "french"]

changeLanguage = (langString) ->
	Global.language = langString
	console.log "Changing language to #{langString}"
	
	$("[translatestring]").each ((index) -> 
		obj = $(this)
		identifier = obj.attr("stringID")
		string = Model.msg.get(identifier)
		obj.text(string)
		)
	translateBirds()
	translateCitizenBirds()