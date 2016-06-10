model = {}

model.name2id = (name) ->
	name.replace(" ", "_").toLowerCase()

model.manualTweets = [
	{
		name:"Group Green", 
		content: "Hmm, wenn die Tagesschau beim NPD-Verbotsverfahren ne Schalte zu ihrem 'Rechtsexperten' macht, ist das irgendwie doppeldeutig...", 
		time: new Date().getTime(), 
		# hashtags: ["HouseOfTweets"], 
		image: "../ext/images/politicians/group_greengrün.jpg",
		birdp: "amsel",
		birdc: "ara",
		soundp: "../ext/sounds/amsel-neutral.mp3", 
		soundc: "../ext/sounds/ara-neutral.mp3", 
		id: 0,
		partycolor: "green",
		byPoli: true,
		twitterName: "groupgreen"
	},
	{
		name:"Group Green", 
		content: "EU: Lasst uns Griechenland auf ebay versteigern!",
		time: new Date().getTime(), 
		# hashtags: ["HouseOfTweets"], 
		image: "../ext/images/politicians/group_greengrün.jpg",
		birdp: "amsel",
		birdc: "ara",
		soundp: "../ext/sounds/amsel-neutral.mp3", 
		soundc: "../ext/sounds/ara-neutral.mp3", 
		id: 1,
		partycolor: "green",
		byPoli: true,
		twitterName: "groupgreen"
	},
	{
		name:"Group Green", 
		content: "The tweet has intentionally been left blank.", 
		time: new Date().getTime(), 
		# hashtags: ["HouseOfTweets"], 
		image: "../ext/images/politicians/group_greengrün.jpg",
		birdp: "amsel",
		birdc: "ara",
		soundp: "../ext/sounds/amsel-neutral.mp3", 
		soundc: "../ext/sounds/ara-neutral.mp3", 
		id: 2,
		partycolor: "green",
		byPoli: true,
		twitterName: "groupgreen"
	},
	{
		name:"Group Green", 
		content: "Politician should be spelled 'politian'. Deep thoughts...", 
		time: new Date().getTime(), 
		# hashtags: ["HouseOfTweets"], 
		image: "../ext/images/politicians/group_greengrün.jpg",
		birdp: "amsel",
		birdc: "ara",
		soundp: "../ext/sounds/amsel-neutral.mp3", 
		soundc: "../ext/sounds/ara-neutral.mp3", 
		id: 3,
		partycolor: "green",
		byPoli: true,
		twitterName: "groupgreen"
	},
	{
		name:"Group Green", 
		content: "Niemand hat die Absicht eine Mauer zu errichten. ~ Bob, der Baumeister.", 
		time: new Date().getTime(), 
		# hashtags: ["HouseOfTweets"], 
		image: "../ext/images/politicians/group_greengrün.jpg",
		birdp: "amsel",
		birdc: "ara",
		soundp: "../ext/sounds/amsel-neutral.mp3", 
		soundc: "../ext/sounds/ara-neutral.mp3", 
		id: 4,
		partycolor: "green",
		byPoli: true,
		twitterName: "groupgreen"
	},
	{
		name:"Group Green", 
		content: "We love Turing.", 
		time: new Date().getTime(), 
		# hashtags: ["HouseOfTweets"], 
		image: "../ext/images/politicians/group_greengrün.jpg",
		birdp: "amsel",
		birdc: "ara",
		soundp: "../ext/sounds/amsel-neutral.mp3", 
		soundc: "../ext/sounds/ara-neutral.mp3", 
		id: 5,
		partycolor: "green",
		byPoli: true,
		twitterName: "groupgreen"
	},
	{
		name:"Group Green", 
		content: "Aller guten Dinge sind drei. Sorry, Sarah.", 
		time: new Date().getTime(), 
		# hashtags: ["HouseOfTweets"], 
		image: "../ext/images/politicians/group_greengrün.jpg",
		birdp: "amsel",
		birdc: "ara",
		soundp: "../ext/sounds/amsel-neutral.mp3", 
		soundc: "../ext/sounds/ara-neutral.mp3", 
		id: 6,
		partycolor: "green",
		byPoli: true,
		twitterName: "groupgreen"
	}
] 

model.politicians = {
	"vonderleyen": { # <- use id here
		name: "Ursula von der Leyen",
		party: "CDU",
		twittering: true,
		self_bird: "Heckenbraunelle"
		citizen_bird: "Rotkehlchen"
		cv: "Hitler was ok, I guess."
	},
	"merkel": {
		name: "Angela Merkel",
		party: "CDU",
		twittering: true,
		self_bird: "Rotkehlchen"
		citizen_bird: "Weißkopfseeadler"
		cv: "Nobody plans on building a wall. ~Bob the Builder"
	}
}

model.birds = {
	"Rotkehlchen": {
		name: "Rotkehlchen",
		latin_name: "Sancta Simplicita",
		cv: "I wish I was a Tukan..."
	},
	"Tukan": {
		name: "Tukan",
		latin_name: "Avis est verbum",
		cv: "Tukans are awesome!"
	}
}

# TODO: only for citizen's tweets
bad_words_according_to_girls: [
	"fuck", "fick",
	"nigger",
	"penis",
	"skrotum",
	"scrotum",
	"white power",
	"wixxer",
	"fotze",
	"hure",
	"pussy",
	"whore",
	"bitch",
	"shit",
	"asshole",
	"arschloch"
]

actually_bad_words: [

]
