# Issue tracker (formerly: https://piratenpad.de/p/SNIP)

This is a copy of our internal issue tracker. Thanks to piratenpad.de
and Etherpad for their wonderful work!

## Open Questions

[Next Meeting]
> - [Max] citizen bird selection: image clickable
  -> Really? Selecting is an irreversible action and should thus always be 
     on purpose. When allowing to click the image, the selection *and* submission
     might come unexpected for the user.
  Implemented as feature toggle.

[Volker]
- French?
- Paper? - Paper!
- Poke Volker: Picture<Schweizer> from twitter? Looks not all too serious. Description?
- Poke Volker: How does the hall look.
- Make a decision about the "Feetless Akoya"
    * currently it's pretty bad: the "air holes" are irregular and look improvised – which they are.
    * getting the real "Standfuß" seems impossible
    * not desperate enough to ask the devil

[Max]
- Imprint "button" placement
- Prepare removing "drawing" feature
- Bird list -> allow to show drawings???

[Both]
- Keyboard situation
- Retweet information/details
- Wording
- Curse Word Replacements
- About page on public facing site.
- TeamViewer?

## Windows setup:

- [Any] Disable zoom - Chrome?
- [Any] Disable F Keys - Registry?

## Last steps before Production:

- [Any] All the "response" strings in `backend/responseBuilder.py`.
    This will be the most public part of the project, even more so than the text on the monitors.
- [Max] Activate ambient sounds
- [Ben] Activate replies
- [Any] Copy over concept text to public facing site
- [Any] Check language -> British English

## Backend:

- [Ben] Re-run all crawlers to get up-to-date information
- [Ben] Maybe force-sort politicians? (Front-End thinks they are sorted by pid, but new politicians are inserted sequentially)
- [Ben] Enable forwarding of retweet data (2 lines in twitter.py, plus adapting the tests)
- [Ben] Properly handle removal of the two politicians
- [Ben] Adapt data structure for citizen user feedback queue, see README.
      Provide *short* messages. French message encouraged, not mandatory.

## Frontend:

- [HIGH PRIORITY] INCLUDE REFERENCE TO BIRD PERSON!!!

- [Ben] Crop images to your liking
- [Max] switches on center page: Icons clickable
- [Max] Fix screensaver
- [Max] auto focus input field
- [Max] bird on tweet more prominent
- [Max] disallow opening profile before lists are displayed  
- [Max] rename deputy -> poli
- [Max] impressum/impress -> imprint
- [Max] Re-check whether switch-icons are correctly aligned with the switch-text (e.g. "stimmen von")
- [Max] "Add Citizen User" should not play sound of already displayed tweets
- [Max] Add Citizen User page: After scrolling: Arrows have different opacity -> take the one after scrolling.
- [Max] Remove "Foto"/"Zeichnung" from bird profile
- [Max] Reset filtered bird/poli list after leaving voiceslists page.
- [Max] keep switch and image consistent when leaving bird profile page
- [Max] Adapt data structure for citizen user feedback queue, see README

## Model

- [Ben] Stephan Schweitzer hinzufügen:
    Twitter-Handle: @sc_ontour
- [Ben] Update crawler to properly handle removal of the two politicians

## Publicity (public-facing page)

- [Max] Make preview-video's dimensions dynamic (responsive)

## Publicity

- [Max] Polish group green Twitter account for public display, rename.
- [Max] Give Volker access to account after polishing.
- [Any] Prepare How-To for exhib.

## Trivia / Good to know:

Search current session for errors, and keep listening:

    find backend/log/ | sort -n | tail -n1 \
      | xargs tail -F -n+1 | grep -Prn '(^|[^Tt])error' -
