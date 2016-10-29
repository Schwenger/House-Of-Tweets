# Issue tracker (formerly: https://piratenpad.de/p/SNIP)

This is a copy of our internal issue tracker. Thanks to piratenpad.de
and Etherpad for their wonderful work!

## Debian / Windows setup:

- [Any] Install and set up TeamViewer on Windows for remote access (Ben knows how)
- [Max] On-Screen Keyboard konfigurieren
- [Max] Disable zoom
- [Max] disable F Keys
- [Any] sanity check all the "response" strings in `backend/responseBuilder.py`.
    This will be the most public part of the project, even more so than the text on the monitors.

## Backend:

- [Ben] If far in the future (= long after November 2016):
    - re-run all crawlers to get up-to-date information
    - maybe force-sort politicians? (Frontend thinks they are sorted by pid, but new politicians are inserted sequentially)
- [Ben] Enable forwarding of retweet data (2 lines in twitter.py, plus adapting the tests)
- [Ben] Gaaanz zum Schluss: Wirklich die replies aktivieren

Both: Come up with a "protocol" to sanely display to a user when the tweeting can start.
Suggestion:
- if something is wrong, send `{"user":"foo","bird":"bar","state":"error"}`
- if data entry succeeded, send `{"user":"foo","bird":"bar","state":"connecting"}`
- *when* (not if) the user can start tweeting, send
  `{"user":"foo","bird":"bar","state":"ready"}`

I just have to think about how to implement that sanely and safely.
Note that I can't* send you notifications when the user is removed.  
*: well, of course I can, but it's unnecessarily complicated.
(Not implemented in this way.  This would replace the "userFeedbackQueue".)

Both: Come up with a "protocol" to transfer "retweet" information.
Suggestion:
`retweet` is no longer a boolean but an optional field,
containing a JSON object about the retweet information.
Absence indicates "not a retweet".  Fields:
- `content`, `username`, `userscreen`, `tweet_id`, `profile_img`:
   Just like in the `tweet` messages themselves.
   (Might be named slightly differently in the `tweets` queue.)
- `uid`, `hashtags`: could be made available easily, but I don't think it's needed anyway.
- `time`: might be difficult, but I could do it.

## Frontend:

- [Max] "Special thanks to: Universität des Saarlandes"
     -> "Saarland University".
     Die anderen haben keinen offiziellen englischen Namen bzw. Wikipedia *ist* schon der englische Name.
- [Max] Display of error/success (adding a CitizenUser) is mixed up
     You probably have fixed that locally, but current git master is still faulty.
- [Max] remove French-handling in model_messages.coffee:
    when "french",  "fr" then @_fr[msg_id]
- [Max] Gaaanz zum Schluss: "ambient sounds" wieder an machen.
- M rename Vogelstimmen, stimmen von
- M citizen bird selection: image clickable
- M re-evaluate curse word replacements (suggested by Julia: "*****" instead of "#Gänseblümchen")
- M switches on center page: Icons clickable
- M auto focus input field
- M bird on tweet more prominent
- M disallow opening profile before lists are displayed  
    (e.g., if a user "double clicks" on something, make sure the second click doesn't activate anything.)
- M rename deputy -> poli
- M sort english birds
- M impressum/impress? (British English)
- M impressum: "idea of bird" in concept. WTF?
- M translate saarland university
- M Re-check whether switch-icons are correctly aligned with the switch-text (e.g. "stimmen von")
- M RT: Display author somehow    
  Note: I'll only provide you with the "directly previous" author.  If @A tweets "msgA", @B retweets
  that, and @C retweets *from @B*, then I can only tell you "@B" as previous author, because fuck recursion.
  See "retweet protocol" discussion in Backend.

## Model

Stephan Schweitzer hinzufügen:
- Twitter-Handle: @sc_ontour
- Bild: Ich warte noch auf das Bild.
- Beschreibungstext: Ich warte noch auf das Beschreibungstext.

## Publicity (public-facing page)

- [Any] Some nicer display of "sponsors" and "team".  
    Optional.  I made a `<ul>`-based, plain-text version, without the logos.
- [Any] Impressum: Copy text from coffee files?    
    BLOCKED by impressum changes.  Also, come up with an automation.  
    Y'know, "Automate ALL the things!"
- [Any] Check frontend and public-facing site for proper *British* English.  
    We can't use the British flag and then write American English.  
    Last run: 03.10.2016
- [Max] Make preview-video's dimensions dynamic (responsive)

## Publicity

- [Max] Polish group green Twitter account for public display, rename
- [Any] update our description in backend/pols.json:
    - [max] write text: englisches Template allgemein
    - [max] write text: deutscher, englischer Text für HoT
    - [ben] push text into pols.json and that coffee model file
- [Max] Give Volker access to account after polishing.
- [Any] Aufstellung vor Ort.  Es gibt nur ein Twitter, und da beide Monitore
        dasselbe zeigen, sollten sie nicht nebeneinander stehen.
- [Both] how-to on exhibition?  
    What do you mean?  
    Die Frage, ob wir bei der Ausstellung einen Text neben den Rechner hängen
      sollen, der erklärt, was man machen kann und wie.

## Trivia / Good to know:

Search current session for errors, and keep listening:

    find backend/log/ | sort -n | tail -n1 \
      | xargs tail -F -n+1 | grep -Prn '(^|[^Tt])error' -
