## Data flow

See attached file `dataflow.png`:

![](dataflow.png)

## Data format

### Queue "tweets"

- `byPoli`: boolean, whether this is a politician or not, e.g. `true`
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
- `soundc`: string, valid path to the bird, chosen by the citizen, e.g. `"/home/eispin/workspace/House-Of-Tweets/ext/sounds/amsel-aufgebracht.mp3"`
- `soundp`: same, but chosen by politician.  If not a politician, `null`.
- `time`: string, containing unix timestamp (seconds since 1970-01-01), e.g. `"1453840647"`
- `twitterName`: string, twitter-handle without '@' char, e.g. `"pes04"`

### Queue "citizenbirds"

FIXME

### Queue "citizenuser"

FIXME

## Known Threads

- `batching.py` creates a Timer.  Concurrency between this Timer and the owner of the `TweetBatcher` is synchronized
  via a lock inside the `TweetBatcher`.  However, nobody else should access the same connection.
- *unsure*: RabbitMQ callbacks. They might have their own threads per callback. Locking: *unknown*
- *unsure*: The twitter connection itself spawns at least one thread. Locking: *unknown*
- the main thread just sets everything up, finishes immediately, and waits on all other threads.
  Locking: Python internal.