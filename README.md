House of Tweets
===============

<!-- Do not change the first three lines; it is used by provide.sh to verify
     stuff.  Also, HTML comments need to stand alone. -->

House of Tweets is an art/computer science project that took place at the Saarland University.

We do not want to bother anyone with unnecessarily many words, so feel free to play around with our project and leave feedback if you like. Make sure, your sound is turned on!

![main_page_overview](https://github.com/Schwenger/House-Of-Tweets/blob/master/preview.png)


Install instructions:
=====================

For the tersest but also most platform-specific instructions, read the `.travis.yml` script.


### Get all secrets

To be able to establish a connection to twitter, you need to provide information about your twitter account in the `backend/credentials.py` files. This is a short Python "module" that defines a map `CREDENTIALS`.

Refer to `backend/credentials_TEMPLATE.py` for an example and follow the format.

You can obtain the necessary values by creating a [twitter app](https://apps.twitter.com/).


### Get heavy

Large binary files are stored in a separate repository. To download the files run `git submodule update --init .heavy`. 

This repository includes all sounds and images which have appropriate licensing such that they can be made public.


### OS-dependent packages

In general, you'll need:
- some form of libav for pydub (see below)
- npm
- rabbitmq
- coffeescript
- less
- Python 3
- pip (sometimes "pip3", should be running on Python 3)
- script (as in "typescript", appeared in BSD 3.0)

##### Linux
- Ubuntu: `sudo apt-get install -qq libav-tools npm rabbitmq-server coffeescript` (python, pip, and bsdutils?)
- Debian: `sudo apt-get install -qq libav-tools npm rabbitmq-server coffeescript python3-dev python3-pip bsdutils`

Some systems (Ubuntu and Debian, at least) install the `node` binary in
a way that is incompatible with npm.  To resolve this, do this on
Debian and Ubuntu:
```
sudo ln -s /usr/bin/nodejs /usr/bin/node
```

##### Mac OS X
In case you have not installed homebrew yet, run 
```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
to install homebrew and `brew install rabbitmq node python3 libav bsdutils` to install the dependencies.

Afterwards add the following to your `.bashrc`
```
export NODE_PATH=/usr/local/lib/node_modules
```
Then, run `npm install -g coffee-script`.

##### Windows
It wouldn't be Windows if there would not be a graphical installer for most of the needed programs. 
- [Erlang](http://www.erlang.org/downloads) for rabbitmq
- [RabbitMQ](https://www.rabbitmq.com/install-windows.html)
- [Python](https://www.python.org/downloads/windows/)
- [ffmpeg](https://ffmpeg.org/download.html) This is the only program without a graphical installer. Download and extract the program. Afterwards add the path to the `ffmpeg/bin` directory to your PATH variable ([instructions](http://stackoverflow.com/questions/23400030/windows-7-add-path)).

As it is windows, you most certainly have to restart your system, potentially several times during the installations.

### OS-independent packages

FrontEnd-dependencies will be installed automatically by running
`make install_dependencies`.

This will install `stompjs, browserify, coffeescript-concat, less, pip3, install, pika, pydub, tweepy, typing` using `npm` and `pip`.

Note 1: In Ubuntu the `pip3` package is simply called `pip`.
Check with `--version` which Python version it is addressing and make sure it is Python 3.

Note 2: Under Debian, you may need to install the pip packages as sudo.

Note 3: Under Windows you need to install the dependencies manually. Use the GUI for `npm`, and the command line for `pip`. Both are shipped with the before-mentioned installers. For the latter, you need to run the command line as an administrator.

Normal workflow:
================

Get RabbitMQ running:
- preconditions: none
- if not already started: `sudo rabbitmq-server -detached` (the `-detached` part starts it "into the background")
- wait a second (RabbitMQ doesn't like being rushed at this point)
- load plugin: `sudo rabbitmq-plugins enable --online rabbitmq_web_stomp rabbitmq_management`  
  Explanation:
    * `--online` means: fail if rabbitmq isn't running
    * `rabbitmq_web_stomp` enables communication with the frontend
    * `rabbitmq_management` is optional, and provides [a web interface](http://localhost:15672)
  In Windows use the rabbit-mq console shipped with the installer or the GUI.
- useful for: running the project, running tests
  
Build the frontend:
- preconditions: none
- execute: `make frontend` or just `make`
- useful for: running the project

Run the backend:
- preconditions: RabbitMQ is running
- start: `( cd backend && ./startBackend.py ${SOME_KEY})` with `SOME_KEY` being a key defined in `credentials.py`.
- useful for: running the project

Run the tests:
- preconditions: RabbitMQ is running (unless you changed `MANUAL_TESTS` in `tests.py`)
- start: `( cd backend && ./tests.py ${SOME_KEY})`

Run the project / presentation:
- preconditions: backend and RabbitMQ are running
- start: point your browser at `out/main.html`


Authors:
========

The application is developed and maintained by
* Maximilian Schwenger (schwenger@stud.uni-saarland.de)
* Ben Wiederhake (s9bewied@stud.uni-saarland.de, Ben.Wiederhake@gmail.com)

Sounds are extracted from [xeno-canto](http://www.xeno-canto.org/about/terms), thank you very much!
Images can be extracted from wikipedia, for legal reasons, they are not included online.

The first version was additionally developed by 
* Michaela Klauck (s9miklau@stud.uni-saarland.de)
* Christopher Schommer (s9crscho@stud.uni-saarland.de)
* s9saster@stud.uni-saarland.de

Troubleshooting:
================
In case there are any troubles developing on windows, we do not intend to fix it. The workflow is designed for Unix systems.

A fully built project will run on Windows, as well as Unix systems. However, the FrontEnd is designed for and only fully tested on Chrome for Windows 7 and Mac OS 10.10 or later.
