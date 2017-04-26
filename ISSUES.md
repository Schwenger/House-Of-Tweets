# Issue tracker (formerly: https://piratenpad.de/p/SNIP)

## Open Questions

[Next Meeting]
- Check for remaining issues
- Why does "Ben" ask the Landesvertretung to link to us?

[Volker]
- Paper? - Paper!
- Poke Volker: How does the hall look.
- Make a decision about the "Feetless Akoya"
    * currently it's pretty bad: the "air holes" are irregular and look improvised – which they are.
    * getting the real "Standfuß" seems impossible
    * not desperate enough to ask the devil

[Both]
- Retweet information/details
- Wording
- Curse Word Replacements

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
- [Any] Clean Downloads folder and Hinstory, just to make it less interesting to troll
- [Any] Make extra triple-sure that both have the newest version of backend (`backend/`),
        frontend (`out/` after `$ make frontend`) and images (`ext/images/politicians/`) if appliccable
- [Any] Check that "our" shortcut is marked as such
- [Any] Check CHECKLIST_WINDOWS.txt for missing entries

## Backend:

Nothing to do currently

## Frontend:

- [Urgent] Adding new user will remove tweets by polis.
- [HIGH PRIORITY] INCLUDE REFERENCE TO BIRD PERSON!!!

- [Max] Fix screensaver - DONE
- [Max] Imprint "button" placement - DONE
- [Max] Left sidebar control and flags overlap invisibly. - DONE
- [Max] Prepare removing "drawing" feature - DONE
- [Max] auto focus input field - DONE
- [Max] bird on tweet more prominent - Done?
- [Max] "Add Citizen User" should not play sound of already displayed tweets
- [Max] Add Citizen User page: After scrolling: Arrows have different opacity -> take the one after scrolling. - DONE
- [Max] Replace double-spaces in politician's CV by `<br />` or something. - DONE
- [Max] Adapt data structure for citizen user feedback queue, see README - DONE

- [Max] Move "Imprint" button a bit up: Barely reachable (by physical finger) on Tweetian2
- [Max] The bird selection scroll thing (CitizenUser) is sometimes broken.
- [Max] The `@` (CitizenUser) is always broken.
- [Max] Apparently, there's a 4x2 grid.

## Model

Nuthin'.  Watchin' da game, havin' a bud …

## Publicity (public-facing page)

- [Ben] Landesvertretung fragen, auf unsere Seite zu verlinken.

## Publicity

- [Max] Polish group green Twitter account for public display, rename.
- [Max] Give Volker access to account after polishing.
- [Any] Prepare How-To for exhib.

## Trivia / Good to know:

Search current session for errors, and keep listening:

    find backend/log/ | sort -n | tail -n1 \
      | xargs tail -F -n+1 | grep -Prn '(^|[^Tt])error' -
