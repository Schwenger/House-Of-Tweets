## Data flow

See attached file `dataflow.png`:

![](dataflow.png)

## Data format

### Queue "tweets"

Direction: backend → frontend

- `poli`: string, the HoT-internal ID of the politician or `null` if citizen, e.g. `null` or `"649"`
- `content`: string, e.g. `"Wir dürfen uns nicht auseinander dividieren lassen!"`
- `hashtags`: possibly empty array, each element is a string, containing a single hashtag, without the leading hash, e.g. `[]` or `["what", "doomed"]`
    Note that frontend should NOT parse this for `HoT` or something.
- `id`: number, any unique id, assigned by the Backend, e.g. `1`
- `image`: string, valid URL to Twitter profile image, e.g. `"- `https`://pbs.twimg.com/profile_images/573488117560295424/5qsXbC5W.jpeg"`
- `name`: string, e.g. `"Angela Merkel"`
- `partycolor`: string, any valid CSS color as a string, e.g. `"#00cc00"`
- `refresh`: JSON object, only present if the backend detected a valid usage of `#HoT`
    - `politicianId`: string, only present if 'byPoli' is true, HoT-defined ID, e.g. `"hot"` or `"384"`
    - `birdId`: string, the newly assigned bird, e.g. `"amsel"` (always a valid key in birds.json)
- `retweet`: boolean, e.g. `true`
- `sound`: JSON object
    - `duration`: integer, length, in milliseconds, of the sounds
    - `citizen`: JSON object, describing the bird chosen by the citizen
        - `natural`: string, valid path to the bird's natural sound, e.g. `"/home/eispin/workspace/House-Of-Tweets/ext/sounds/processed/774316458742583296r-c_n.mp3"`
        - `synth`: string, valid path to the bird's "synthesized" sound or "artistic interpretation", e.g. `"/home/eispin/workspace/House-Of-Tweets/ext/sounds/processed/774316458742583296r-c_s.mp3"`
        - `bid`: string, containing the raw bird ID, and a valid key for `coffee/model/model_birds.coffee`
    - `poli`: same, but chosen by the politician.  If not a politician, `null`.
- `time`: string, containing unix timestamp (seconds since 1970-01-01), e.g. `"1453840647"`
- `twitterName`: string, twitter-handle without '@' char, e.g. `"pes04"`

### Queue "userBirdNack"

Direction: backend → frontend

- `twittername`: same as from the `citizenuser` request
- `birdid`: same as from the `citizenuser` request
- `error`: string, contains the id of any error.  Possible values are:
    - `null`: no error occurred
    - `"unknown-user"`: couldn't resolve `twittername` (note that inclusion of the
      initial `@` does not matter, and twitter-handles are case-insensitive)
    - `"unknown-bird"`: couldn't resolve `birdid`

### Queue "citizenbirds"

Direction: frontend → backend

- `politicianid`: string, the HoT-internal politician-ID, e.g. `"195"` or `"notavalidpolitician"`
- `birdid`: string, the (unsanitized) bird name, e.g. `"ara"` or `"notavalidbird"`

### Queue "citizenuser"

Direction: frontend → backend

- `twittername`: string, the (unsanitized) twitter handle of the user,
  may (but does not need to) include the `@` character, e.g. `"HouseOfTweetsSB"`
  or `"@HouseOfTweetsSB"` or `"notavalidtwitterhandle"`
- `birdid`: string, the (unsanitized) bird name, e.g. `"ara"` or `"notavalidbird"`

## Known Threads

- `batching.py` creates a Timer.  Concurrency between this Timer and the owner of the `TweetBatcher` is synchronized
  via a lock inside the `TweetBatcher`.  However, nobody else should access the same connection.
- Each "incoming" RabbitMQ queue has its own thread. Locking: must happen in the called functions,
  namely `TwitterConnection.addCitizen` and `PoliticianBackend.setBird`
- *unsure*: The twitter connection itself spawns at least one thread. Locking: *unknown*
- Note that `TwitterConnection` creates one `filter` for all politicians
  together, and then one for *each* active citizen. `TwitterConnection`
  also creates threads (`Timer` objects) to remove citizens.
  Locking: giant `TwitterConnection` lock
- the main thread just sets everything up, finishes immediately, and waits on all other threads.
  Locking: Python internal.
