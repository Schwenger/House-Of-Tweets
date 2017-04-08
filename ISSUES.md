# Issue tracker (formerly: https://piratenpad.de/p/SNIP)

## Open Questions

[Next Meeting]
- [Both] About page on public facing site.
  -> Ehh, an unstylized `<ul>` gotta do the job.
- Soll "HoT" wirklich ein Politiker sein?  Vielleicht im Frontend "verstecken"?
		-> Wahrscheinlich eine gute Idee, habe es mal eingefügt.

[Volker]
- Paper? - Paper!
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
- [Ben] Also, strings in `backend/messages.json`
- [Max] Activate ambient sounds
- [Ben] Activate replies
- [Any] Copy over concept text to public facing site
- [Any] Check language -> British English
- [Max] Re-check whether switch-icons are correctly aligned with the switch-text (e.g. "stimmen von")

## Backend:

Nothing to do currently

## Frontend:

- [HIGH PRIORITY] INCLUDE REFERENCE TO BIRD PERSON!!!

- [Max] Fix screensaver
- [Max] Imprint "button" placement
- [Max] Prepare removing "drawing" feature
- [Max] auto focus input field
- [Max] bird on tweet more prominent
- [Max] "Add Citizen User" should not play sound of already displayed tweets
- [Max] Add Citizen User page: After scrolling: Arrows have different opacity -> take the one after scrolling.
- [Max] Replace double-spaces in politician's CV by `<br />` or something.
- [Max] Adapt data structure for citizen user feedback queue, see README

## Model

Nuthin'.  Watchin' da game, havin' a bud …

## Publicity (public-facing page)

- [Max] Make preview-video's dimensions dynamic (responsive)
- [Ben] Add date, time, place
    18.5.
- [Ben] Landesvertretung fragen, auf unsere Seite zu verlinken.

## Publicity

- [Max] Polish group green Twitter account for public display, rename.
- [Max] Give Volker access to account after polishing.
- [Any] Prepare How-To for exhib.

## Trivia / Good to know:

Search current session for errors, and keep listening:

    find backend/log/ | sort -n | tail -n1 \
      | xargs tail -F -n+1 | grep -Prn '(^|[^Tt])error' -
