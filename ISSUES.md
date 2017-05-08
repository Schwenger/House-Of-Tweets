# Issue tracker (formerly: https://piratenpad.de/p/SNIP)

## Open Questions

[Next Meeting]
- Check for remaining issues

[Volker]
- Paper? - Paper!

[Both]
- Curse Word Replacements

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

## Backend:

(ready)

## Frontend:

- [Max] The `@` (CitizenUser) is always broken.

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
