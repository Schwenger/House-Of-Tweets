## Workflow

This file tries to document what each file is supposed to do.

Intermediate results (roughly 60 MiB) are stored in Ben's archives.
So instead of running `crawl-*.py`, please contact me,
to go easy on their websites.

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
  - `page`: URL from which this information was gathered
  - `possible_parties`: "list" (semantically a set) of reasonable
    party-associations (usually only a single party, or rarely `['cdu', 'csu']`)
  - `ejected` (optional): whether they are "ausgeschieden"
  - `src`: owning party of the website (`bundestag.de` is `bundestag`)
  - `twitter_handle` (optional): twitter account, probably without leading `@`.
  - `img`: JSON object, or `null` (in case of bundestag and sometimes cxu;
    these photos are too small to be usable)  
    FIXME: should be optional, not null

Where the format for `img`
  - `url`: url from the source's website
  - `license`: one of `cc-by-sa-3.0`, `unknown-bundestag`,
    `unknown-linke`, `unknown-gruene`, `custom-spd`
  - `copyright` (optional): what it says
  - `is_compressed`: presence indicates that the download is a compressed file which
    has to be uncompressed to get an image file.

### Aggregation: `aggregate-each.py`

NOT IMPLEMENTED

- aggregate by name, make sure everything matches
- input: `parse-each.json` (hard-coded)
- output: `aggregate-each.json` (hard-coded)
- output format of each entry:
  - `full_name`: verified and consistent (else it throws)
  - `party`: verified and consistent (else it throws)
  - `imgs`: object
  
The format of `imgs` is:
- key: owning party of the website (`bundestag.de` is `bundestag`)
- value: JSON object
  - `url`: url from the source's website
  - `license`: one of `CC-BY-SA`, `unknown-linke`, `unknown-gruene`
  - `photographer`: what it says

### Patching

In case this is necessary: some `jsonpatch`

NOT EVEN THOUGHT ABOUT