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
- [None] Upload correct pictures for Max/V7 to T1

## Backend:

- [None] backend/vomit.py sometimes leads to strange behavior in frontend  (sorry, future programmer)
- [None] Find out what happened to the API keys, why T2 burned them, and whether they are usable again

## Frontend:

- [None] Alignment, still
- [None] Need a way to load pols.json from Backend, NOT built-in
         (changes to coffee/model/model_polis.json are lost upon restart)

## Model

(ready)

## Publicity (public-facing page)

(ready)

- [Any] After 23rd May 2017: Add note that HoT is over, at least in LV Saarland.

## Publicity

- [None] Rename group green Twitter account for public display, maybe adjust color.

## Trivia / Good to know:

Search current session for errors, and keep listening:

    find backend/log/ | sort -n | tail -n1 \
      | xargs tail -F -n+1 | grep -Prn '(^|[^Tt])error' -
