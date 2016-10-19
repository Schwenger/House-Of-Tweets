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
				Bei HOUSE OF TWEETS handelt es sich um eine interdisziplinäre Klangskulptur für den Deutschen Bundestag, die dialogisch ausgerichtet ist.

				Die von den Politikern per TWITTER praktizierte Kommunikation wird in Vogelsprache transkribiert und ist von den Abgeordneten in aktiver Teilhabe persönlich wählbar. 
				Sie erstellen quasi eine stellvertretende Vogelstimme, eine Art Alter Ego-Vogel für ihren Twitter-Account. Eine öffentliche Schnittstelle ermöglicht es, dass diese tweets auch ausserhalb des Plenarsaals ab-hörbar sind.

				Die Messages werden übersetzt in "Zwitschern", #hashtags in Flügelschlagen als Beispiel. Zeitgenössische Musiker und Komponisten stellen eigene Interpretation wahlweise zur Verfügung - möglich ist es auch, einen Stimmen-Imitator einzusetzen oder gar selbst eine Melodie zu pfeifen. 

				Besucher des Bundestages, sowie die Adressaten der Tweets, die "Followers", können ebenfalls auf einer Internet-Plattform den Delegierten Vogelstimmen ihrer Wahl zuordnen. Als Filter für die Re-Tweets, die eingehenden Antworten der Beteiligten, kann man z.B. einen Vogel-Schwarm wählen oder pure Natur- Athmo (die Nebengeräusche in den mp3-files der ornithologischen recordings) einsetzen. Hörbar über Lautsprechersysteme (wahlweise Kopfhörer) an variablen Orten im Bundestag. 

				Durch die stattfindende Überlagerung der Tonspuren entsteht ein Soundmix, der sich autark - je nach Traffic, jeden Moment neu generiert. Es erwächst eine soziale Plastik, die -auditiv wahrgenommen- interaktiv eine sinnliche Form annimmt. 
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
				"House of  Tweets" is an interdisciplinary sound sculpture for the German Bundestag, which is oriented dialogue. 

				The communication practiced by politicians via Twitter is transcribed in bird language and is personally selected by the deputies in active participation. They create a deputy bird voice, a kind of alter ego bird for their Twitter account. A public interface enables these tweets to be audible from outside the Chamber. 

				The messages are translated into "chirping", #hashtags in beating of wings as an example. Contemporary composers and musicians provide their own interpretations to choose. It is also possible to use a voice impersonator or to whistle a tune itself. 

				Visitors of the Bundestag, as well as the addressee of the tweets or "followers" can also assign to an internet platform in order to delegate a birdsong their choice. As a filter for the re-tweets that incoming responses of the participants, you can select a bird swarm or pure natural ambient (the noise in the MP3 files of the ornithological recordings). As an alternative to the natural birdsong the visitor can select compositions/soundscapes by contemporary musicians - also artistic variations of the bird-image are applicable.
				Audible on speaker systems (optional headphones) at variable locations in the Bundestag. 

				By taking place superposition of soundtracks a symphony, a sound mix, the autarkic be created - depending on traffic, at any moment regenerated. It rises to a social sculpture that auditive-perceived interactively assumes a sensual form.

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
