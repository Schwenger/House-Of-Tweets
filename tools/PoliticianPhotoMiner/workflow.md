## Workflow

This file tries to document what each file is supposed to do.

Intermediate results (roughly 60 MiB) are stored in Ben's archives.

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
  - if from bundestag: `detect_party`, `name`
  - if from linke, spd or gruene: `full_name` (including any titles, proper hyphenization)
  - if cxu (= cdu/csu): `name` (deduced from url, wrong hyphenization, missing titles)

FIXME: spd still calls it `name`.
FIXME: cxu could have `full_name`.

### Second crawling: `crawl-each.py`

- crawls each politician-specific page, hosted on a party's website (where `bundestag.de` counts as a party)
- input: `parse-roots.json` (hard-coded)
- output: `crawl-each.json` (hard-coded)
- output format of each entry:
  - same as `parse-roots.json`
  - plus `page_file`, the relative path to the downloaded page

### Second parsing: `parse-each.py`

NOT IMPLEMENTED

- parse them, extract all interesting infos, aggregate by name
- input: `crawl-each.json` (hard-coded)
- output: `parse-each.json` (hard-coded)
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