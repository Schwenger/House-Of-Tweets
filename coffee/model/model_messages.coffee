	@msg: {
		get: (msg_id) ->
			split = msg_id.split(":")
			if split.length is 1
				switch Global.language
					when "german",  "de" then @_de[msg_id]
					when "english", "en" then @_en[msg_id]
					when "french",  "fr" then @_fr[msg_id]
			else
				[model_key, model_id] = split
				Model[model_key][model_id][Util.addLang("name")]

		_de: {

			concept_header: "Konzept"
			concept: """
				Bei House of Tweets handelt es sich um eine interdisziplinäre und interaktive Klangskulptur für den Deutschen Bundestag.
				<br>
				Jeder Politiker kann sich eine stellvertretende Vogelstimme auswählen, die genutzt wird um Tweets auditiv darzustellen. Diese Stimme reflektiert dann den Gefühlszustand des Politikers beim Tweeten; ein aggresiver Tweet wird in einen aggressiven Ton übersetzt.
				<br>
				So werden hitzige Bundestagsdebatten zu einem Konzert der Vögel, ein berauschender Mix verschiedener Stimmen, der sich stets ändert und niemals still steht.
				<br>
				Zudem können Besucher der Ausstellung den Politikern selbst einen passenden Vogel zuweisen und die folgenden Tweets mit den neuen Stimmen erleben.
				<br>
				Sie können auch für Ihren eigenen Twitteraccount einen Vogel aussuchen und selbst Teil der Ausstellung werden. Ihre Tweets werden nicht nur zusammen mit den der Politiker angezeigt, sondern sind auch zu hören und tragen zum Klangerlebnis bei.
				"""

			us_header: "Die Gesichter dahinter"

			dfki: "Deutsches Forschungszentrum für Künstliche Intelligenz"

			search_placeholder_poli: "Suche einen Politiker"
			search_placeholder_bird: "Suche einen Vogel"

			special_thanks: "Mit bestem Dank an:"
			
			purpose_volker: "Idee und Konzept"
			purpose_max: "Design und technische Umsetzung"
			purpose_ben: "Design und technische Umsetzung"

			select: "Auswählen"

			success_feedback_pre: "Nutzer"
			success_feedback_post: "wurde erfolgreich hinzugefügt. Frohes Tweeten!"

			error_feedback_pre: "Nutzer"
			error_feedback_post: "konnte nicht gefunden werden. Vertippt?"

			is_poli_feedback_pre: "Nutzer"
			is_poli_feedback_post: "ist ein Politiker und wird bereits angezeigt."

			choose_bird_prompt: "Jetzt noch den Lieblingsvogel aussuchen und abschicken!"

			photo: "Foto"
			drawing: "Zeichnung" #Kunst?
			
			bird_calls: "Vogelstimmen",
			own_tweets: "Eigene Tweets",
			back_to_tweets: "Zurück zu den Tweets",
			
			voices_of: "Stimmen von", 
			politicians: "Politikern",
			citizens: "Bürgern",
			
			citizens_tweets: "Tweets von Bürgern",
			footer_on: "an",
			footer_off: "aus",
			
			twitter_name_prompt: "Geben Sie Ihren Twitternamen an, um für mindestens 5 Minuten Ihre eigenen Tweets zu sehen und zu hören!",
			bird_prompt: "Wählen Sie Ihren Vogel aus:",
			button_text: "Vögel",
			
			deputies: "Abgeordnete",
			birds: "Vögel",
			
			back: "zurück",
			change: "ändern",

			open: "Öffnen",
			party: "Partei",

			play_last_x_sounds: "Tweets der letzten"
			select_bird: "Wählen Sie einen Vogel aus:"

			tweetername: "Twitter Username"

			own_bird: "Eigener Vogel"
			citizen_bird: "Bürgervogel"
		}

		_en: {

			concept_header: "Concept"

			concept: """
				House of Tweets is a interdisciplinary and interactive sound sculpture for the German Bundestag.
				<br>
				Each politician can choose a representative bird. The bird's voice will then be used to depict tweets aurally. It reflects the politician's mood while tweeting: an aggressive tweet will be translated into an aggressive bird call.
				<br>
				During a fiery debate in the Bundestag a concert of birds arises, a befuddling mix of different voices, constantly changing, never subsiding.
				<br>
				In addition, visitors of the exhibit can assign their own ideas of birds to the politicians and experience upcoming tweets with the new voice.
				<br>
				They can also add their own twitter account, choose a bird, and become themselves part of the exhibit. Their tweets will not only be displayed among the politicians', but become audible and contribute to the sound experience.
				"""

			us_header: "The faces behind it"

			dfki: "German Research Center for Artificial Intelligence"

			search_placeholder_poli: "Find a politician"
			search_placeholder_bird: "Find a bird"

			special_thanks: "Special thanks to:"
			
			purpose_volker: "Idea and Concept"
			purpose_max: "Design and technical Implementation"
			purpose_ben: "Design and technical Implementation"

			register: "Submit"
			select: "Select"

			error_feedback_pre: "User"
			error_feedback_post: "cannot be found. Typo?"
			
			success_feedback_pre: "User"
			success_feedback_post: "added successfully. Happy Tweeting!"

			is_poli_feedback_pre: "User"
			is_poli_feedback_post: "is a politician and being followed already."

			choose_bird_prompt: "Now choose you favourite bird and submit!"

			photo: "photo"
			drawing: "drawing"

			bird_calls: "Bird Calls",
			own_tweets: "Own Tweets",
			back_to_tweets: "Back to Tweets",
			
			voices_of: "Sounds of", 
			politicians: "Politicians",
			citizens: "Citizens",
			
			citizens_tweets: "Tweets of Citizens",
			footer_on: "on",
			footer_off: "off",
			
			twitter_name_prompt: "Fill in your Twittername to hear and see your own tweets for at least 5 minutes!",
			bird_prompt: "Choose your bird:",
			button_text: "birds",
			
			deputies: "Deputies",
			birds: "Birds",
			
			back: "back",
			change: "change",

			open: "Open",
			party: "Party",

			play_last_x_sounds: "Tweets of last"
			select_bird: "Select a bird:"

			own_bird: "Own Bird"
			citizen_bird: "Citizen-chosen Bird"
		}
	}
