# Crawler, parser, preprocessing

This directory contains all "new" tools.
These tools care about correctness, safety, and copyright,
and allow for manual overrides in just about any step.

This file tries to document what each file is supposed to do.

Intermediate results and all raw image files (together roughly 4+ GiB)
are stored in the `cache` submodule.
So instead of running `crawl_*.py` or `checkout_*.py` from scratch,
please contact me for access to it,
to go easy on their websites.

## Workflow (politicians)

This is the subset of files that deal with the regeneration of `pols.json`
and `model_polis.json`.

If there ever are politicians with duplicate name, you'll need to modify the
"sanitization"  code in `parse_each.py` so that it generates strictly unique
names for each politician, and optionally adapt the full-to-bare name conversion.
`aggregate.py` and all later stages assume that a `full_name` is strictly unique.

### First crawling: `crawl_roots.py`

- crawls the few "root" websites (roughly 30)
- input: none (duh)
- output: `crawl_roots.json`
- output format of each entry:
  - filename and URL of respective root website
  - owning party of the website (`bundestag.de` is `None`)

FIXME: `bundestag.de` changed their architecture, and now loads
all politician-data via JSON.  This crawler currently can't cope with that.
Contact Ben to get the cached, and (as of Feb 2017 already!) slightly outdated versions.

### First parsing: `parse_roots.py`

- parse them to generate a preliminary list of politicians.  Not presentable yet.
- input: `crawl_roots.json` (hard-coded)
- output: `parse_roots.json` (hard-coded)
- output format of each entry:
  - `page`: URL of respective politician (not downloaded or parsed yet)
  - `src`: owning party of the website (`bundestag.de` is `bundestag`)
  - `full_name`: name, including any titles, proper hyphenization
  - if from bundestag: `detect_party`, `name`  
    FIXME: kick `name`

### Second crawling: `crawl_each.py`

- crawls each politician-specific page, hosted on a party's website (where `bundestag.de` counts as a party)
- input: `parse_roots.json` (hard-coded)
- output: `crawl_each.json` (hard-coded)
- output format of each entry:
  - same as `parse_roots.json`
  - plus `page_file`, the relative path to the downloaded page

### Second parsing: `parse_each.py`

- parse them, extract all interesting infos
- input: `crawl_each.json` (hard-coded)
- output: `parse_each.json` (hard-coded)
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
  - `license`: one of `CC-BY-SA-3.0`, `unknown-bundestag`,
    `custom-linke`, `custom-gruene`, `custom-spd`
  - `copyright` (optional): what it says
  - `is_compressed`: presence indicates that the download is a compressed file which
    has to be uncompressed to get an image file.

### Aggregation: `aggregate_each.py`

- aggregate by name, remove ejected politicians completely, make sure everything matches
- input: `parse_each.json` (hard-coded)
- output: `aggregate_each.json` (hard-coded)
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

### Third Crawling: `wikify_each.py`

- download the Wikipedia pages for each politician
- input: `aggregate_each.json` (hard-coded)
- output: `wikify_each.json` (hard-coded)
- output format of each entry:
  - same as `aggregate_each.json`
  - if a Wikipedia entry with image exists, the image URL is added to
    the `imgs` entry, and `wiki` is added to the `srcs` list/set.  
    Note that this doesn't actually download the image, just determine its URL.

### Converging with existing `pols.json` (`converge_each.py`)

- agree with `pols.json` on all data, and spell out every addition/deletion
- input: `wikify_each.json` (hard-coded) *and* the currently used `/backend/pols.json`
- output: `converge_each.json` (hard-coded)
- output format of each entry:
  - same order and same fields as `pols.json`, except:
  - `images` gets replaced by `imgs` (see "Aggregation")
  - `twitterId` may be left unassigned

### Checkout images, generate pols.json: `checkout_hot_poli.py`

- checkout preview/for-use images, and link to them "properly"
- input: `twitter_each.json` (hard-coded)
- output: `pols.json` (hard-coded; note: in this directory, not in `/backend/`)
- output format: see `/backend/README.md`
- SIDE-EFFECTS: all images will be put into the `preview` directory,
  which must not already exist.

## Bird images

The public-facing website needed new images, as we're not sure enough
about the license situation of the old images.

### Crawl image information: `fetch_birds.py`

- reliably locate exactly one image (including license infos) for each bird
- input: `birds.json` (hard-coded)
- output: `fetch_birds.json` (hard-coded)
- output format: list of JSON objects:
  - all fields of birds.json are preserved
    (can and shall be used as drop-in replacement for `birds.json`)
  - `img`: JSON object, image meta-information, just like an entry in the politician
    crawler (`url`, `license`, and optionally `copyright`)

### Checkout images: `checkout_birds.py`

- checkout for-use images, and link to them "properly"
- input: `fetch_birds.json` (hard-coded)
- output: `checkout_pubweb_birds.json` (hard-coded)
- output format: list of JSON objects, sorted by German name:
  - `filename`: string, location inside the `preview` directory, currently just bid plus `.jpg`, e.g. `"gartenbaumlaeufer.jpg"`
  - `bid`: string, internal bird-ID, probably not needed, e.g. `"gartenbaumlaeufer"`
  - `de_name`, `en_name`: string, German and English name respectively,
    that will be recognized both by humans and the backend, e.g. `"Gartenbaumläufer"`  
    Note: not HTML escaped!
  - `license`: string, e.g. `"CC-BY-SA-3.0"`
  - `copyright` (optional): string, e.g. `"Andreas Trepte"`
- SIDE-EFFECTS: all images for use in pubweb will be put into the `preview` directory,
  which must not already exist.
- SIDE-EFFECTS: all images for use in HoT will be put into the `preview_hb` directory,
  which must not already exist.

## About the cache

All web requests go through `nice.py`, which uses some kind of "cache", namely the subfolder `./cache/`.
In `cache_index_TEMPLATE.json` you can see how to initialize the cache by yourself.
Just drop it into the `cache` folder, drop the `_TEMPLATE` part, and you're good to go.

But again, that's a horrible idea.  Please re-use the files I already have cached, at least for the
heavy stuff like image data.

### Checks

There's `check_cache.py` to assert that every file mentioned in the index is actually there.
However, it doesn't check any of these things:
- whether the file is actually valid (which is a pretty difficult thing)
- whether the file is what we *indended* (impossible)
- whether the file is still up-to-date (impossible, without contacting the server again)
- whether identical files could be re-used
- whether every file in the filesystem is referenced by the index

So please don't expect too much of it.
