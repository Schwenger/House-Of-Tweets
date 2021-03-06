#= require <util.coffee>
#= require <global.coffee>

# Template for the model class. Will be enriched by data in the model/ directory
# automatically.

class Model

	@name2id: (name) ->
		# Removed spaces for a string by replacing them with an underscore.
		name.replace(" ", "_").toLowerCase()

	# For debugging only.
	@manualTweets: [{
		name:"Group Green", 
		content: "Hmm, wenn die Tagesschau beim NPD-Verbotsverfahren ne Schalte zu ihrem 'Rechtsexperten' macht, ist das irgendwie doppeldeutig...", 
		time: Util.time(), 
		# hashtags: ["HouseOfTweets"], 
		image: "../ext/images/politicians/group_greengrün.jpg",
		sound:
			duration: 5000
			poli:
				natural: "../.heavy/sounds/amsel-neutral.mp3"
				synth: "../.heavy/sounds/amsel-neutral.mp3"
			citizen:
				natural: "../.heavy/sounds/amsel-neutral.mp3"
				synth: "../.heavy/sounds/amsel-neutral.mp3"
		birdp: "amsel",
		birdc: "ara",
		id: 0,
		partycolor: "green",
		byPoli: true,
		twitterName: "groupgreen"
	},
	{
		name:"Group Green", 
		content: "The tweet has intentionally been left blank.", 
		time: Util.time(), 
		# hashtags: ["HouseOfTweets"], 
		image: "../ext/images/politicians/group_greengrün.jpg",
		birdp: "amsel",
		birdc: "ara",
		sound:
			duration: 5000
			poli:
				natural: "../.heavy/sounds/amsel-neutral.mp3"
				synth: "../.heavy/sounds/amsel-neutral.mp3"
			citizen:
				natural: "../.heavy/sounds/amsel-neutral.mp3"
				synth: "../.heavy/sounds/amsel-neutral.mp3"
		id: 2,
		partycolor: "green",
		byPoli: true,
		twitterName: "groupgreen"
	},
	{
		name:"Group Green", 
		content: "Politician should be spelled 'politian'. Deep thoughts...", 
		time: Util.time(), 
		# hashtags: ["HouseOfTweets"], 
		image: "../ext/images/politicians/group_greengrün.jpg",
		birdp: "amsel",
		birdc: "ara",
		sound:
			duration: 5000
			poli:
				natural: "../.heavy/sounds/amsel-neutral.mp3"
				synth: "../.heavy/sounds/amsel-neutral.mp3"
			citizen:
				natural: "../.heavy/sounds/amsel-neutral.mp3"
				synth: "../.heavy/sounds/amsel-neutral.mp3"
		partycolor: "green",
		byPoli: true,
		twitterName: "groupgreen"
	}] 
