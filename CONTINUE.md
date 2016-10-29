# How-to revive this project

- Gather the two all-in-one touchscreens from Max and Ben
- Re-install Windows on them, as documented in `/install/CHECKLIST_WINDOWS.txt`  
  Let's hope that the drivers are still available.
- Pout at Max for not documenting every single step.  Also, you may want to
  skip the Virtualbox entirely, as we currently operate by just building on
  a different machine and copy all files over, and that works rather well.
- Re-evaluate the tweepy-monkeypatch, and check whether tweepy still exists.
  Maybe migrate to twython?
  See [issue #10](https://github.com/Schwenger/House-Of-Tweets/issues/10) for potential discussion.
- Run the crawler.  You *can* use the `/tools/PhotoMiner/cache` submodule, but it's a bad idea,
  so just start from scratch.  Read `/tools/PhotoMiner/README.md` for details.
- Drink a smoothie while waiting on the crawler.  Do I still like smoothies?  I hope so!
- Fetch all submodules.
  - `.heavy` is the largest and easiest one, since it's hosted on GitHub
    and mirrored by us (well, by Ben, at least).
  - `.secrets` takes a bit more effort.
    The repo is currently "only" hosted on our
    private computers, so here's how to rebuild that repository:
    - Create `/.secrets/credentials.py` as documented in `/backend/credentiels_TEMPLATE.py`
    - `/.secrets/tweets/` is an archive of received tweets.  Not important,
      as you can re-collect fresh data easily.
    - `/.secrets/images/logos/` and `/.secrets/images/profile/` have unclear copyright situation,
      and won't be made public.  They only contain the sponsors' logos and our pictures anyway:
      ```
$ ls logos profile
logos:
dfki.jpg  hbk-o.png  ministerium.png  saartoto.pdf  spielbanken.pdf  unieule.png
dfki.png  hbk.png    saarland.jpg     saartoto.png  spielbanken.png

profile:
ben-o.png  ben.png  max.jpg  volker.jpg
```
    - `/.secrets/images/birds_secret/` contain all "private" drawings
      (currently only `kiwi-drawing.jpg`), including the `unsorted` subfolder.
  - `/tools/PhotoMiner/cache` should be ignored, since it's probably totally out-of-date
    when you read this.  For the worst case scenario, Ben has a backup.
    (Because it's *huge*, Max doesn't have a backup.)
- Try to get `/backend/tests.py test_${NAME}` to run.  See `/README.md` for instructions.
- Try to `make install_dependencies`.  Note that you'll have to install some `pip`
  stuff differently on Debian (but not Ubuntu), and I still haven't figured out why.
- Set up Travis automation again, in case it isn't.
- Try to `make frontend` and display the result.  Since the frontend is highly non-portable,
  watch out for off-by-pixel errors due to Chrome updates.
- Login to twitter (both Ben and Max have the password to the @HouseOfTweetsSB account)
  and adapt if necessary.
- Check whether the links in `/backend/responseBuilder.py` are still valid,
  and replace them if necessary.

This should be it.
