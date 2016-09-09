#= require <util.coffee>
#= require <global.coffee>

class Model

	@name2id: (name) ->
		name.replace(" ", "_").toLowerCase()

	@manualTweets: [{
		name:"Group Green", 
		content: "Hmm, wenn die Tagesschau beim NPD-Verbotsverfahren ne Schalte zu ihrem 'Rechtsexperten' macht, ist das irgendwie doppeldeutig...", 
		time: Util.time(), 
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
		content: "The tweet has intentionally been left blank.", 
		time: Util.time(), 
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
		time: Util.time(), 
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
	}] 
