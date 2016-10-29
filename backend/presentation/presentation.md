# Recording the presentation

Note that you may want to do some other tests beforehand so you
don't run all this in vain.

## Setup

- Open `gen_sounds.py` and set `QUICK_FOR_PRESENTATION = True`, then run it.
- Make sure there is NO backend running, and open the frontend
- Set up screen capture (e.g., align it to the browser window, make sure no
  other audio is playing, etc.)
- You may want to set the browser window to "always on top", as you will need
  to press enter in the commandline twice during the presentation
- Type `./presentation.py` where you would normally type `./starBackend.py test_foo`,
  but don't press enter yet.

## Running the presentation

- Start screen and audio capture
- Press enter on the command line.  This triggers the first of two tweet-batches.
  Wait until complete
- Go to the right, enter "equu0ae4", select "Blaumeise" (if you don't,
  then the hard-coded "response" won't work.)
- Press enter on the command line again.  `presentation.py` was waiting patiently
  for you, and now sends the second of the two batches of tweets.
- Demonstrate the "Show Citizen Tweets" button by flipping it.  The user tweet will vanish.
- After the sound settles, demonstrate the "Voices of" button.  Circle some bird before and
  after you do the switch, to "show" it to the viewer.
- After the sound settles, shouw impress, politician, politician bird, and bird pages
- Flip language, show a *bird* page.
- Stop recording
