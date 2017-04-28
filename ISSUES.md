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

- [Any] All the "response" strings in `backend/responseBuilder.py`.
    This will be the most public part of the project, even more so than the text on the monitors.
- [Ben] Also, strings in `backend/messages.json`
- [Max] Activate ambient sounds
- [Max] Re-check whether switch-icons are correctly aligned with the switch-text (e.g. "stimmen von")
- [Any] Check that "our" shortcut is marked as such
- [Any] Check CHECKLIST_WINDOWS.txt for missing entries

## Backend:

## Frontend:

- [HIGH PRIORITY] INCLUDE REFERENCE TO BIRD PERSON!!!

- [Max] The `@` (CitizenUser) is always broken.

## Model

- [Ben] Download ambient sounds.

## Publicity (public-facing page)

## Publicity

- [Max] Polish group green Twitter account for public display, rename.
- [Any] Prepare How-To for exhib.

## Trivia / Good to know:

Search current session for errors, and keep listening:

    find backend/log/ | sort -n | tail -n1 \
      | xargs tail -F -n+1 | grep -Prn '(^|[^Tt])error' -
