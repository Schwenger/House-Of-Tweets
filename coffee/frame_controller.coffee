#= require <global.coffee>
#= require <lang.coffee>
#= require <voices_controller.coffee>

$("#tweet-list-header").click (-> $("#language-control").removeClass "invisible")

$("#language-control").click (->	
	$("#language-control").addClass "invisible"
	)

addLanguageClickHandler = (lang) ->
	$("##{lang}-flag").click (-> changeLanguage(lang))

addLanguageClickHandler lang for lang in ["german", "english", "french"]

changeLanguage = (langString) ->
	global.language = langString
	console.log(langString)
	
	switch(langString)
			when "german" then langID = "de"
				
			when "english" then langID = "en"
			
			when "french" then langID = "fr"
			
	$("[translatestring]").each ((index) -> 
		obj = $(this)
		identifier = obj.attr("stringID")
		string = SiteLanguage[langID][identifier]
		obj.text(string)
		)
	translateBirds()
	translateCitizenBirds()