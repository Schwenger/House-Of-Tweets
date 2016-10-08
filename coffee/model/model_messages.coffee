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
			us_header: "Das sind wir"

			search_placeholder_poli: "Suche einen Politiker"
			search_placeholder_bird: "Suche einen Vogel"

			register: "Abschicken"
			select: "Auswählen"

			positive_feedback_pre: "Nutzer"
			positive_feedback_post: "wurde erfolgreich hinzugefügt. Frohes Tweeten!"

			negative_feedback_pre: "Nutzer"
			negative_feedback_post: "konnte nicht gefunden werden. Vertippt?"

			birdsObl: "Vögeln"
			musicianObl: "Musikern"
			chirpingOf: "Zwitschern von"

			photo: "Foto"
			drawing: "Zeichnung" #Kunst?
			
			sprachen: "Sprachen",
			vogelstimmen: "Vogelstimmen",
			eigeneT: "Eigene Tweets",
			zurückZuT: "Zurück zu den Tweets",
			
			stimmenVon: "Stimmen von", 
			politikern: "Politikern",
			bürgern: "Bürgern",
			
			tweetsVonBürgern: "Tweets von Bürgern",
			footerAn: "an",
			footerAus: "aus",
			
			dieLetzten24: "die letzten 24 h",
			echtzeit: "Echtzeit",
			
			gelb_text1: "Geben Sie Ihren Twitternamen an, um für mindestens 5 Minuten Ihre eigenen Tweets zu sehen und zu hören!",
			gelb_text2: "Wähle deinen Vogel aus:",
			button_text: "Vögel",
			
			rot_Abgeordnete: "Abgeordnete",
			rot_Vögel: "Vögel",
			
			rot_zurück: "zurück",
			rot_ändern: "ändern",

			missing_uname: "Bitte gib deinen Nutzernamen an.",
			missing_pw: "Bitte gib ein Passwort an.",

			admin_page: "Admin Seite",
			open: "Öffnen",
			back: "Zurück",
			username: "Nutzername",
			password: "Passwort",
			save_changes: "Änderungen speichern",
			logout: "Abmelden",
			politicians: "Politiker",
			birds: "Vögel",
			add_politician: "Politiker hinzufügen",
			remove_politician: "Politiker entfernen",
			first_name: "Vorname",
			last_name: "Nachname",
			party: "Partei",
			description: "Beschreibung",
			tweets_q: "Twittert?",
			yes: "Ja",
			no: "Nein",
			add: "Hinzufügen",
			add_bird: "Vogel hinzufügen",
			remove_bird: "Vogel entfernen",
			latin: "Latein",
			name: "Name"

			playlastxsounds: "Tweets der letzten"
			select_bird: "Wählen Sie einen Vogel aus:"

			male: "männlich"
			female: "weiblich"

			imageurl: "Link zum Bild"

			tweetername: "Twitter Username"

			own_bird: "Eigener Vogel"
			citizen_bird: "Bürgervogel"
			
			a_project_by: "Ein Projekt von:"
			leader: "Marco Speicher (DFKI) und Volker Sieben (Künstler)"
			members: "HOT Mitglieder"
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
			us_header: "This is us"

			search_placeholder_poli: "Find a politician"
			search_placeholder_bird: "Find a bird"

			register: "Submit"
			select: "Select"

			negative_feedback_pre: "User"
			negative_feedback_post: "cannot be found. Typo?"
			
			positive_feedback_pre: "User"
			positive_feedback_post: "added successfully. Happy Tweeting!"

			birdsObl: "Birds"
			musicianObl: "Musicians"
			chirpingOf: "Chirping of"

			photo: "photo"
			drawing: "drawing"

			sprachen: "Languages",
			vogelstimmen: "Bird Calls",
			eigeneT: "Own Tweets",
			zurückZuT: "Back to Tweets",
			
			stimmenVon: "Sounds of", 
			politikern: "Politicians",
			bürgern: "Citizens",
			
			tweetsVonBürgern: "Tweets of Citizens",
			footerAn: "on",
			footerAus: "off",
			
			dieLetzten24: "the last 24 h",
			echtzeit: "Real-time",
			
			gelb_text1: "Fill in your Twittername to hear and see your own tweets for at least 5 minutes!",
			gelb_text2: "Choose your bird:",
			button_text: "birds",
			
			rot_Abgeordnete: "Deputies",
			rot_Vögel: "Birds",
			
			rot_zurück: "back",
			rot_ändern: "change",

			missing_uname: "Please insert a user name.",
			missing_password: "Please insert a password.",

			admin_page: "Admin Page",
			open: "Open",
			back: "back",
			username: "Username",
			password: "Password",
			save_changes: "Save changes",
			logout: "logout",
			politicians: "Politicians",
			birds: "Birds",
			add_politician: "Add politician",
			remove_politician: "Remove politician",
			first_name: "First name",
			last_name: "Last name",
			party: "Party",
			description: "Description",
			tweets_q: "Tweets?",
			yes: "Yes",
			no: "No",
			add: "Add",
			add_bird: "Add bird",
			remove_bird: "Remove bird",
			latin: "Latin",
			name: "Name"

			playlastxsounds: "Tweets of last"
			select_bird: "Select a bird:"

			male: "male"
			female: "female"

			imageurl: "Link to image"

			own_bird: "Own Bird"
			citizen_bird: "Citizen-chosen Bird"
			
			a_project_by: "A project by:"
			leader: "Marco Speicher (DFKI) and Volker Sieben (artist)"
			members: "HOT members"
		}
	}
