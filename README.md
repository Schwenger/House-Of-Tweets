House of Tweets
===============

House of Tweets is an art/computer science project that took place at the Saarland University.

We do not want to bother anyone with unnecessarily many words, so feel free to play around with our project and leave feedback if you like. Make sure, your sound is turned on!

![main_page_overview](https://github.com/Schwenger/House-Of-Tweets/preview.png)

Prerequesites:
==============

UPDATE: You need to have to install ffmpeg or libav. I suggest libav. Run:

`apt-get install libav-tools`

You need to get coffee and lessc up and running. For this please have a look at [the coffeescript website](https://www.coffeescript.org) 
and [the less website](https://www.lesscss.org).
Additionally, you will need [rabbitmq](https://www.rabbitmq.com) for tweet passing and browserify for resolving node.js dependencies.
To install rabbitmq on Mac use

`brew install rabbitmq`

To install rabbitmq on Debian/Ubuntu you have to add the repo as well as the key to avoid unwanted warnings. 
Afterwards you need to update your repos and install rabbitmq as usual.

`echo "deb http://www.rabbitmq.com/debian/ testing main"  | sudo tee  /etc/apt/sources.list.d/rabbitmq.list > /dev/null`

`wget https://www.rabbitmq.com/rabbitmq-signing-key-public.asc`

`sudo apt-key add rabbitmq-signing-key-public.asc`

`sudo apt-get update`

`sudo apt-get install rabbitmq-server -y`

As expected windows needs some special treatment and provides a graphical install wizard.
First download erlang from [here](http://www.erlang.org/download.html) and install it (this might take a while).
Afterwards download the rabbitmq installer from [here](https://www.rabbitmq.com/install-windows.html) and run it.

Browserify is a node.js modules. To install it you first need node.js as well as the package manager npm.
Mac:

`brew install nodejs`

`brew install npm`

Now run:

`cd $HOUSEOFTWEETSREPO/ext`

`npm install browserify -g`

`npm install amqplib`

Ubuntu:

Try:

`sudo apt-get update`

`sudo apt-get install nodejs`

`sudo apt-get install npm`

`sudo ln -s /usr/bin/nodejs /usr/bin/node`

else:

`curl -sL https://deb.nodesource.com/setup | sudo bash -`

`sudo apt-get install nodejs`

`sudo apt-get install build-essential`

`sudo ln -s /usr/bin/nodejs /usr/bin/node`

Here, the nodejs packages already contains npm.

Now run:

`cd $HOUSEOFTWEETSREPO/ext`

`npm install browserify -g`

`npm install amqplib`

Windows:

Against all odds, for Windows there is an installer you con download from [here](https://nodejs.org/en/download/). 
After installation restart your computer. npm is already contained in the installation.

Now run:

`cd $HOUSEOFTWEETSREPO/ext`

`npm install browserify -g`

`npm install amqplib`

Install Instructions:
=====================

Simply run the compile script (`./compile`) to compile and start/manage everything automatically. It's as simple as that.
Troubleshooting: Make sure this file has execute rights (`chmod +x compile.sh`).
Afterwards open the html/main.html file in your browser and start the backend using 

`cd backend; python3 startbackend.py`

Make sure the queue is up:
`rabbitmq-server start -detached`

Working Process:
================

When introducing a new coffee script file make sure to add the compile instruction into compile.sh so that everything works fine out of the box.
When editing the README have a look at this [markdown-cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet).

Authors:
========

* Michaela Klauck (s9miklau@stud.uni-saarland.de)
* Christopher Schommer (s9crscho@stud.uni-saarland.de)
* Maximilian Schwenger (schwenger@stud.uni-saarland.de)
* s9saster@stud.uni-saarland.de

Sounds are extracted from [xeno-canto](http://www.xeno-canto.org/about/terms), thank you very much!
Images can be extracted from wikipedia, for legal reasons, they are not included online.

Troubleshooting:
================
In case there are any troubles running the application on windows, we are aware of this but we do not intend to fix it. The application is designed for unix systems.
