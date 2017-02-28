# Issue tracker (formerly: https://piratenpad.de/p/SNIP)

This is a copy of our internal issue tracker. Thanks to piratenpad.de
and Etherpad for their wonderful work!

## Open Questions

[Next Meeting]
> - [Both] About page on public facing site.
  -> Ehh, an unstylized `<ul>` gotta do the job.

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
- Bird list -> allow to show drawings???

[Both]
- Keyboard situation
- Retweet information/details
- Wording
- Curse Word Replacements
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
- [Max] Re-check whether switch-icons are correctly aligned with the switch-text (e.g. "stimmen von")

## Backend:

- [Ben] Adapt data structure for citizen user feedback queue, see README.
      Provide *short* messages. French message encouraged, not mandatory.

## Frontend:

- [HIGH PRIORITY] INCLUDE REFERENCE TO BIRD PERSON!!!

- [Max] Fix screensaver
- [Max] Imprint "button" placement
- [Max] Prepare removing "drawing" feature
- [Max] auto focus input field
- [Max] bird on tweet more prominent
- [Max] "Add Citizen User" should not play sound of already displayed tweets
- [Max] Add Citizen User page: After scrolling: Arrows have different opacity -> take the one after scrolling.
- [Max] Adapt data structure for citizen user feedback queue, see README

## Model

- [Ben] Stephan Schweitzer hinzufügen:
    Twitter-Handle: @sc_ontour
- [Ben] Check how long the cv entries are, and enrich short ones.

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
