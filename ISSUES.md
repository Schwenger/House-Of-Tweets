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

- [Any] Check CHECKLIST_WINDOWS.txt for missing entries

## Backend:

(ready)

## Frontend:

- [Max] Alignment, still

## Model

(ready)

## Publicity (public-facing page)

(ready)

## Publicity

- [Max] Rename group green Twitter account for public display, maybe adjust color.

## Trivia / Good to know:

Search current session for errors, and keep listening:

    find backend/log/ | sort -n | tail -n1 \
      | xargs tail -F -n+1 | grep -Prn '(^|[^Tt])error' -
