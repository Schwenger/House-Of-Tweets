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
$ find -type f -print0 | sort -z | xargs -0 sha512sum  # Ignoring certain irrelevant files
9c4dc6ef1940de3d0e4c1655d58e96dc5b60514bd3d569ed77b356cbd27999470ef6b3d635b73145cb124d6c002de76be4122593c175ea0425a893c8ef683cd4  ./credentials.py
a1c3ead750d6e96c5187bfdaa4d1ba15dc059f2438c9b48fd7fabbfb2bbe68421dcf9ef54f0270faa14ec5740fb89cbe9af46459a055b900064ad08a4ae0a029  ./images/birds_secret/kiwi-drawing.jpg
80bb927e50e02c15136a534d30248a7d18dbca86b9876eadaedcf0ad6001e73be3b42b7b894dc8a9176eeda1fcebb34e00b15a4e06d68d05220a9b608f414167  ./images/birds_secret/unsorted/anna-tattoo-birdie.jpg
e2a5e12709832920cb8d05788c184b125900a548b096c68d24012a9ce4403d5dc2cd207d6cf21345bc9e40403eed7346f8ba9106b1e5fbb300b9ae3a4055cc16  ./images/birds_secret/unsorted/Gabriele_Langendorf_Twitter.jpg
dab6570ad85125c887aea99521d2a75a629a305b2bb3380ea0ece464874d5ff311e6b57d4b3cd754d41de0e2649df680ac72bcdbf1d6550922c77948579c555a  ./images/birds_secret/unsorted/graffity-birdie-freundmaria-sb.jpg
eacf8f31f0c924805dcc222667d5420b5ddc62fd3342f25e907bb268472b7670cc94098b3a2e9432b626d983b5cbe436f9040bc5ade2f1315ca25e3147af03d8  ./images/birds_secret/unsorted/Michael Markwick.jpg
d43b276374c197218a452da397c245f0ae2ae4c325edc427970e296179404760b907904c1a6cc592e9467a576994e9bdde81a114f85a93b509efb393264784ed  ./images/birds_secret/unsorted/P1200466.jpg
564b2a3cb79c0f058c95990098ecdbf5ae1512951da0fd1839854d154244e3fa57e04c21fab7f39d4e3b46e9eee691f6c744c31cf3bc98f815fde6c83a2cc7de  ./images/birds_secret/unsorted/piepi2.jpg
9e1384fda1dee00a60bfd846db1944d2be14cf3d7d497d485d6f6f16e1980215412dc1170192a80e65c4ba0c05c53afb66d04d029a5b4a4d39d957bc3461ebf1  ./images/birds_secret/unsorted/steinadler.jpg
8258f9dc4ec78264b9e574a37816f6505f8eddf2bb21e352ea37395a4c9ff4beb10e5ffcdc660ca02cd0669c043d5e0d97d5a1491a022523af570862816dce1f  ./images/birds_secret/unsorted/wawa.jpg
723ac50b2959ad86390b46113096ba296859b72f1b2c7f056c6d782e65f2cbdfbbe92f9dec42a5dd0d63f27bc821c24fb66ccff0fa74d70ec41158057470583f  ./images/logos/dfki.jpg
bcf0e07da94a7d8c056ca56a56c1ab869201eeb1272ad6274de9e7781daff9e50ba9505fd8788b72b218c98e84ae47530da27cded27f228ff86c8ff456c7a9f6  ./images/logos/dfki.png
94be35ff5db248d0941e509c0d2ed30498da1a7a424e8f59e12311b679ca5744d7a760b583371c3d6f897f6c8ef9bfab750351519246899ff5326e3c3058f530  ./images/logos/hbk-o.png
b4bcaa691b4f97f1cc95b69ad0d932ecde81293d1ddcba14e9fd0ff442f2db28f479062f66f530322bdd5912129bd1dc13b9509afc56f4e4d4ecbf52f1f7755f  ./images/logos/hbk.png
ffd6c4d7e0bd4255331b617198a83f6232e3971d8a5aec3897994424c6ec2df82f71c2c85dd49c8212f23e17648682e58936908680805a63e4e93153f5411c22  ./images/logos/ministerium.png
18407b6726ee1ac2d27f4ffffbc7aa568d273dd5823d35de5fc29a6f1511dc2c86bce6255b66d46e82b50d39454f80c549e31bb3b742b80c82a73e062d3b1e21  ./images/logos/saarland.jpg
974972df697a1b1255e0140842dd65adb531b44fa48450072077013fb39068fb19f47149152983b3fd256ffec3f10a8c93e48a8edd68c5b26c86157daac0c108  ./images/logos/saartoto.pdf
14ef16101daa10d8aeb2f6835bb384341fa7a743da398fc87c0c41104b750289b57c93d3777fab909a5568b98e10fd41f6bb14cdc131a18d4d467308b9dc385e  ./images/logos/saartoto.png
ca5b97d1e22d9d92ecd9e8a44d2706a5a37c74ca9a6a4b9c6087710d3838b21436f3b119483f21b64203301e479dbfb21979e0c01c72323982dbdbade2adda23  ./images/logos/spielbanken.pdf
86decc2f8d1649731a0c3616a79a6102a5a0a3d8a313a62a3b50efdebd7a7f900ddcbe5c3128069f27ff491980bf6c458b4efe9063851c30fbcac4d3c52cac7d  ./images/logos/spielbanken.png
db023193df75c43cee4c38826bfc004736b19a709662c0f833491b1dc10fed35e1d540cab994f469e944688493d5c97254d30bd53be28b7631df2e85ae952222  ./images/logos/unieule.png
b794424653aa9676f0b3183fed926c911c2da3a61a78f8badd7e63ebe3469dc4679e04d25426711676c3b433a50863fa4771bb73af73f9d40904d48620444df7  ./images/profile/ben-o.png
56bf1c007fcd9e6abeee3339f92861ab80bd39037274c5e55c7ad5917dca4ec88f53decede333e909cf7c9d2e1082ea30d58a0fc4073db37d1d5de70ef481f95  ./images/profile/ben.png
4b2b076328b71c5aba14b63b21017e5215b3443afced45bb72e5ac17bad10cc1602b485e82b54ac65bb80f7c1b3b9f10dad66ea725eab09e7d6a608bb0215fd6  ./images/profile/max.jpg
1deb24af0032111dfcf1371373036d4809317388ec6f346d948e46a043446f1c4dd6bee0a7dc817338075f2312e4ca3e1a114d33aa4a8a24d040d12b2ee84294  ./images/profile/volker.jpg
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
