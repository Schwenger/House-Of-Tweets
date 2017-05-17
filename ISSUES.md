# Issue tracker (formerly: https://piratenpad.de/p/SNIP)

## Open Questions

[Volker]
- Paper? - Paper!

## Windows setup:

## Last steps before Production:

### Always

- [Any] Clean Downloads folder and History, just to make it less interesting to troll
- [Any] Make extra triple-sure that both have the newest version of backend (`backend/`),
        frontend (`out/` after `$ make frontend`) and images (`ext/images/politicians/`) if applicable
- [Any] Check citizen user page scrollbar

### Once

- [Max] Activate ambient sounds
- [Max] Re-check whether switch-icons are correctly aligned with the switch-text (e.g. "stimmen von")
- [Any] Check that "our" shortcut is marked as such
- [Any] Check CHECKLIST_WINDOWS.txt for missing entries
- [Any] Wir brauchen eine "Kostenübernahme von der Landesvertretung,
        damit wir die zwei beruflichen Nächte nicht selber zahlen müssen".

## Backend:

(ready)

## Frontend:

- [Max] Can Windows play more than one sound at the same time?
        On Linux, I just noticed, this fails silently. (Pun not intended.)
- [Max] After registering a CitizenUser, selection jumps to "false".
        That's the wrong way around.
        `TweetController.showAllTweets` and `_showAllTweets` (why is this implemented twice?) call this:
            `$('#citizen-tweets-switch').prop('checked', true);`
        Running that in the console, shows that the switch seems to
        implement this mapping: `true` for "aus" and `false` for "an".
        There's too many `not` in there, I'm not gonna touch it.

## Model

(ready)

## Publicity (public-facing page)

(ready)

## Publicity

- [Max] Rename group green Twitter account for public display, maybe adjust color.
- [Any] Prepare How-To for exhib.

## Trivia / Good to know:

Search current session for errors, and keep listening:

    find backend/log/ | sort -n | tail -n1 \
      | xargs tail -F -n+1 | grep -Prn '(^|[^Tt])error' -
