## Workflow

This file tries to document what each file is supposed to do.

Intermediate results (roughly 60 MiB) and all raw image files (roughly 3.6 GiB)
are stored in the `cache` submodule.
So instead of running `crawl-*.py` from scratch, please contact me for access to it,
to go easy on their websites.

If there ever are politicians with duplicate name, you'll need to modify the
"sanitization"  code in `parse-each.py` so that it generates strictly unique
names for each politician, and optionally adapt the full-to-bare name conversion.
`aggregate.py` and all later stages assume that a `full_name` is strictly unique.

### First crawling: `crawl-roots.json`

- crawls the few "root" websites (roughly 30)
- input: none (duh)
- output: `crawl-roots.json`
- output format of each entry:
  - filename and URL of respective root website
  - owning party of the website (`bundestag.de` is `None`)

### First parsing: `parse-roots.py`

- parse them to generate a preliminary list of politicians.  Not presentable yet.
- input: `crawl-roots.json` (hard-coded)
- output: `parse-roots.json` (hard-coded)
- output format of each entry:
  - `page`: URL of respective politician (not downloaded or parsed yet)
  - `src`: owning party of the website (`bundestag.de` is `bundestag`)
  - `full_name`: name, including any titles, proper hyphenization
  - if from bundestag: `detect_party`, `name`  
    FIXME: kick `name`

### Second crawling: `crawl-each.py`

- crawls each politician-specific page, hosted on a party's website (where `bundestag.de` counts as a party)
- input: `parse-roots.json` (hard-coded)
- output: `crawl-each.json` (hard-coded)
- output format of each entry:
  - same as `parse-roots.json`
  - plus `page_file`, the relative path to the downloaded page

### Second parsing: `parse-each.py`

- parse them, extract all interesting infos
- input: `crawl-each.json` (hard-coded)
- output: `parse-each.json` (hard-coded)
- output format of each entry:
  - `full_name`: same as above
  - `name`: optional, if from bundestag  
    FIXME: kick `name`
  - `page`: URL from which this information was gathered
  - `possible_parties`: "list" (semantically a set) of reasonable
    party-associations (usually only a single party, or rarely `['cdu', 'csu']`)
  - `ejected` (optional): whether they are "ausgeschieden"
  - `src`: owning party of the website (`bundestag.de` is `bundestag`)
  - `twitter_handle` (optional): twitter account, without leading `@`
  - `img` (optional): JSON object, if there is a big enough photo to be usable

Where the format for `img`
  - `url`: url from the source's website
  - `license`: one of `cc-by-sa-3.0`, `unknown-bundestag`,
    `custom-linke`, `unknown-gruene`, `custom-spd`  
    FIXME: `cc-by-sa-3.0` should be uppercase.
  - `copyright` (optional): what it says
  - `is_compressed`: presence indicates that the download is a compressed file which
    has to be uncompressed to get an image file.

### Aggregation: `aggregate-each.py`

- aggregate by name, remove ejected politicians completely, make sure everything matches
- input: `parse-each.json` (hard-coded)
- output: `aggregate-each.json` (hard-coded)
- output format of each entry:
  - `full_name`: verified and consistent (else it throws)
  - `name`: simple name (derived from `full_name` by removing titles)
  - `party`: verified and consistent (else it throws)
  - `twitter_handle` (optional): twitter account, without leading `@`
  - `srcs`: dict of all the sources used to their respective URL.
    Keys are a superset of all `imgs`' `src`.
    May include `pols.json`, if appliccable.  FIXME: Hmm.
  - `imgs`: JSON object

The format of `imgs` is:
- key: owning party of the website (`bundestag.de` is `bundestag`)
- value: JSON object
  - `url`: URL of the image itself
  - `license`: see Second Parsing
  - `copyright` (otpional): what it says
  - `is_compressed`: presence indicates that the download is a compressed file which
    has to be uncompressed to get an image file.

### Third Crawling: `wikify-each.py`

- download the Wikipedia pages for each politician
- input: `aggregate-each.json` (hard-coded)
- output: `wikify-each.json` (hard-coded)
- output format of each entry:
  - same as `aggregate-each.json`
  - if a Wikipedia entry with image exists, the image URL is added to
    the `imgs` entry, and `wiki` is added to the `srcs` list/set.  
    Note that this doesn't actually download the image, just determine its URL.

### Converging with existing `pols.json` (`converge-each.py`)

- agree with `pols.json` on all data, and spell out every addition/deletion
- input: `wikify-each.json` (hard-coded) *and* the currently used `/backend/pols.json`
- output: `polify-each.json` (hard-coded)
- output format of each entry:
  - same order and same fields as `pols.json`, except:
  - `images` gets replaced by `imgs` (see "Aggregation")
  - `twitterId` may be left unassigned


### Creating a new `pols.json` (`pols.py`)

FIXME: find out "which" images to use, where "which" means:
- resolution (rescaling necessary?)
- manual blacklist of source-politician pairs
- after pairing with pols.json, chuck out files!


## About the cache

All web requests go through `nice.py`, which uses some kind of "cache", namely the subfolder `./cache/`.
In `cache_index_TEMPLATE.json` you can see how to initialize the cache by yourself.
Just drop it into the `cache` folder, drop the `_TEPLATE` part, and you're good to go.

But again, that's a horrible idea.  Please re-use the files I already have cached, at least for the
heavy stuff like image data.

### Checks

There's `check-cache.py` to assert that every file mentioned in the index is actually there.
However, it doesn't check any of these things:
- whether the file is actually valid (which is a pretty difficult thing)
- whether the file is what we *indended* (impossible)
- whether the file is still up-to-date (impossible, without contacting the server again)
- whether identical files could be re-used
- whether every file in the filesystem is referenced by the index

So please don't expect too much of it.
