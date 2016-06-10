#!/bin/bash
if [ ! -d out ]; then
  mkdir out
fi

echo "Installing web stomping plugin..."
rabbitmq-plugins enable rabbitmq_web_stomp &> /dev/null

echo "Installing node.js modules..."
#npm install --prefix ./ext/ stompjs &> /dev/null
#npm install --prefix ./ext/ browserify &> /dev/null

echo "Compiling less..."
lessc less/main.less > out/main.css

echo "Bundling coffee files..."
echo > out/tmp.coffee
cat coffee/global.coffee >> out/tmp.coffee
echo >> out/tmp.coffee
cat coffee/model.coffee >> out/tmp.coffee
for f in coffee/*.coffee; do
  if [ $f != "coffee/main.coffee" -a $f != "coffee/global.coffee" -a $f != "coffee/model.coffee" ]; then
    cat $f >> out/tmp.coffee
    echo >> out/tmp.coffee
  fi
done
cat coffee/main.coffee >> out/tmp.coffee

echo "Compiling coffee..."
coffee -c out/tmp.coffee 
#rm out/tmp.coffee
echo "Resolving node.js dependencies..."
browserify out/tmp.js > out/main.js

echo "Starting rabbitmq server"
rabbitmq-server -detached &> /dev/null

echo "Starting python background..."

echo "Nothing to do yet."

echo "Compilation finished."
