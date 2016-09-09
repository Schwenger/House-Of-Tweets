	@msg: {
		get: (msg_id) ->
			switch Global.language
				when "german",  "de" then @_de[msg_id]
				when "english", "en" then @_en[msg_id]
				when "french",  "fr" then @_fr[msg_id]

		_de: {

			birdsObl: "Vögeln"
			musicianObl: "Musikern"
			chirpingOf: "Zwittern von"

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
			
			gelb_text1: "Gib deinen Twitternamen an, um für mindestens 5 Minuten deine eigenen Tweets zu sehen und zu hören!",
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

		_fr: {

			birdsObl: "Oiseaux"
			musicianObl: "Musiciens"
			chirpingOf: "Chant des"

			photo: "photo"
			drawing: "dressin" 
			
			sprachen: "Langues",
			vogelstimmen: "Chantes d´oiseaux",
			eigeneT: "Propres Tweets",
			zurückZuT: "Retourner aux Tweets",
			
			stimmenVon: "Voix de", 
			politikern: "Politiciens",
			bürgern: "Citoyens",
			
			tweetsVonBürgern: "Tweets des Citoyens",
			footerAn: "active",
			footerAus: "inactive",
			
			dieLetzten24: "les dernières 24 h",
			echtzeit: "temps réel",
			
			gelb_text1: "Tapes ton nom de Twitter, pour écouter et voir tes propres Tweets pour au moins 5 minutes!",
			gelb_text2: "Choissis ton oiseau:",
			button_text: "Oiseaux",
			
			rot_Abgeordnete: "Députés",
			rot_Vögel: "Oiseaux",
			
			rot_zurück: "retourner",
			rot_ändern: "changer",

			missing_uname: "Tapes ton nom d'utilisateur, s'il-vous-plaît",
			missing_password: "Tapes un mot de passe, s'il-vous-plaît",

			admin_page: "Page d´administrateur",
			open: "ouvrir",
			back: "retourner",
			username: "Nom d´utilisateur",
			password: "mot de passe",
			save_changes: "Enregistrer modifications",
			logout: "Déloguer",
			politicians: "Politicien",
			birds: "Oiseaux",
			add_politician: "Ajouter politiciens",
			remove_politician: "Écarter politiciens",
			first_name: "Prénom",
			last_name: "Nom",
			party: "Partie",
			description: "Description",
			tweets_q: "Active sur Twitter?",
			yes: "Oui",
			no: "Non",
			add: "Ajouter",
			add_bird: "Ajouter oiseau",
			remove_bird: "Écarter oiseau",
			latin: "Latin",
			name: "Nom"

			playlastxsounds: "Tweets des dernières"
			select_bird: "Choisis un oiseau:"

			male: "mâle"
			female: "femelle"

			imageurl: "Lien vers l'image"
			
			a_project_by: "Un projet de:"
			leader: "Marco Speicher (DFKI) et Volker Sieben (artiste)"
			members: "HOT membres"
		}

		_en: {

			birdsObl: "Birds"
			musicianObl: "Musicians"
			chirpingOf: "Chirping of"

			photo: "photo"
			drawing: "drawing"

			sprachen: "Languages",
			vogelstimmen: "Birdsounds",
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
			citizen_bird: "Citizens' Bird"
			
			a_project_by: "A project by:"
			leader: "Marco Speicher (DFKI) and Volker Sieben (artist)"
			members: "HOT members"
		}
	}
