NPM_DEP:=ext/node_modules/stompjs ext/node_modules/browserify ext/node_modules/coffeescript-concat ext/node_modules/less ext/node_modules/jquery-on-infinite-scroll ext/node_modules/coffee-script
PIP_DEP:=bs4 pika pydub requests tweepy typing

BROWSERIFY?=ext/node_modules/.bin/browserify
COFFEESCRIPT_CONCAT?=ext/node_modules/.bin/coffeescript-concat
LESSC?=ext/node_modules/.bin/lessc
COFFEE_BIN?=ext/node_modules/.bin/coffee

OUT=out
TEMP=temp
LESS=less
COFFEE_DIR=coffee
MODEL=${COFFEE_DIR}/model
HTML=html
DIRS=${OUT} ${TEMP} out_pubweb/imgs out_pubweb/css out_pubweb/js
MODELS:=$(wildcard ${MODEL}/*.coffee)

# Max: /Volumes/TF
# Ben: /media/eispin/BW2-NTFS
WINDOWSSHARE?=/Volumes/TF
EXPORTDIR=ext out backend tools/tweepy_monkeypatch

all: frontend backend

# WINDOWS

.PHONY: windows
windows: all
	sed -i -e "s/citizenUserLoadingTime = 1000;/citizenUserLoadingTime = 3000/;" ${OUT}/main.js
	echo Copying files to ${WINDOWSSHARE}.
	mkdir -p $(WINDOWSSHARE)/HoT
	# "Processing... This might take a while."
	rsync --stats -a --copy-links --exclude node_modules --delete-excluded ${EXPORTDIR} ${WINDOWSSHARE}/HoT
	# Note that tweepy_monkeypatch is now at the top-level.

# FRONTEND

.PHONY: frontend
frontend: css js html

.PHONY: css
css: ${OUT}/main.css

${OUT}/main.css: $(wildcard ${LESS}/*.less) | ${DIRS}
	${LESSC} ${LESS}/main.less > $@

.PHONY: html
html: ${OUT}/main.html

${OUT}/main.html: ${HTML}/main.html
	cp $^ $@

.PHONY: js
js: ${OUT}/main.js | ${DIRS}

${OUT}/main.js: ${TEMP}/bundled.js | ${DIRS}
	${BROWSERIFY} $< > $@

${TEMP}/bundled.js: ${TEMP}/bundled.coffee | ${DIRS}
	${COFFEE_BIN} --output ${TEMP} --compile $<

${TEMP}/bundled.coffee: ${COFFEE_DIR}/model.coffee $(wildcard ${COFFEE_DIR}/*.coffee) | ${DIRS}
	${COFFEESCRIPT_CONCAT} -I ${COFFEE_DIR} coffee/main.coffee -o $@

${COFFEE_DIR}/model.coffee: ${COFFEE_DIR}/model_empty.coffee ${MODELS} | ${DIRS}
	cat ${COFFEE_DIR}/model_empty.coffee ${MODELS} > $@

# BACKEND

.PHONY: backend
backend:
# Needs no building.

# PUBWEB
# TODO: Dependencies?

# Yes, this feels a lot like "Please put me into my own namespace".
# No, due to the shared npm accesses it just so doesn't make sense to
# create a different Makefile for that.
PUBWEB_HTML_NAMES:=index index_en birds birds_en about about_en
PUBWEB_HTML_SRC:=${patsubst %,pubweb/autogen/%.html,${PUBWEB_HTML_NAMES}}
PUBWEB_HTML_DST:=${patsubst %,out_pubweb/%.html,${PUBWEB_HTML_NAMES}}
PUBWEB_STATIC_SRC:=$(wildcard pubweb/static/*.*) $(wildcard pubweb/static/*/*.*)
# PUBWEB_STATIC_DST should also include the images, but:
# FIXME: Come up with a clever way to "regenerate"/cache the chosen bird images
#        (WITHOUT pulling from hot_crawler_cache)
PUBWEB_STATIC_DST:=${patsubst pubweb/static/%,out_pubweb/%,${PUBWEB_STATIC_SRC}}
PUBWEB_DYNAMIC_DST:=out_pubweb/js/main.js ${PUBWEB_HTML_DST}

PUBWEB_JSON_DYN:=$(patsubst %,pubweb/birds_%_dyn.coffee,de en)
PUBWEB_JSON_INIT:=$(patsubst %,pubweb/birds_%_init.json,de en)

.PHONY: pubweb
pubweb: pubweb_dyn pubweb_static ${PUBWEB_SPOOF}

# Goal: overwrite old "proper file" index.html if existing.
# Problem: no way to tell make that "check outdated-ness by filetype".
# Observation: make follows symlinks to determine a timestamp.
# Solution: bind it to the faked destination
${PUBWEB_SPOOF}: out_pubweb/index%.html: out_pubweb/birds%.html
	ln -sf $(notdir $<) $@  # Relative path!

.PHONY: pubweb_dyn
pubweb_dyn: ${PUBWEB_DYNAMIC_DST}

${PUBWEB_HTML_DST}: out_pubweb/%: pubweb/autogen/% | ${DIRS}
	cp $< $@

# Slightly overzealous, but whatever
# (If about.html.in changes, then technically birds.html doesn't need to
#  be regenerated, but mk_html.py is too coarse for that anyway.)
${PUBWEB_HTML_SRC}: %: pubweb/index.html.in pubweb/about.html.in pubweb/birds.html.in pubweb/mk_html.py ${PUBWEB_JSON_INIT}
	( cd pubweb && ./mk_html.py )

out_pubweb/js/main.js: ${TEMP}/pubweb_bundled.js | ${DIRS}
# FIXME: Minify?
	${BROWSERIFY} $< > $@

${TEMP}/pubweb_bundled.js: ${TEMP}/pubweb_bundled.coffee | ${DIRS}
	${COFFEE_BIN} --output ${TEMP} --compile $<

${TEMP}/pubweb_bundled.coffee: pubweb/main.coffee pubweb/template.coffee ${PUBWEB_JSON_DYN} | ${DIRS}
	${COFFEESCRIPT_CONCAT} -I pubweb/ $< -o $@

pubweb/template.coffee: pubweb/template.coffee.gen pubweb/mk_html.py
	( cd pubweb && ./template.coffee.gen )

${PUBWEB_JSON_INIT} ${PUBWEB_JSON_DYN}: %: pubweb/mk_json.py tools/PhotoMiner/checkout_pubweb_birds.json
	( cd pubweb && ./mk_json.py )

.PHONY: pubweb_static
pubweb_static: ${PUBWEB_STATIC_DST}

${PUBWEB_STATIC_DST}: out_pubweb/%: pubweb/static/% | ${DIRS}
	cp $< $@

# DEPENDENCIES

.PHONY: install_dependencies
install_dependencies: ${NPM_DEP}
	@if command -v pip3 &> /dev/null ; \
	then \
		echo pip3 install ${PIP_DEP} ; \
		pip3 install ${PIP_DEP} ; \
	elif command -v pip &> /dev/null ; \
	then \
		echo pip install ${PIP_DEP} ; \
		pip install ${PIP_DEP} ; \
	else \
		echo "# Can't find pip or pip3.  Is it installed?" ; \
		false ; \
	fi

${NPM_DEP}: ext/node_modules/%:
	@mkdir -p ext/node_modules
	npm install --prefix ./ext/ $(patsubst ext/node_modules/%,%,$@)

# START

.PHONY: start
start:
	@echo '# Can't start backend: I need your key!  Do it like this:'
	@echo '#     ./startLoggedBackend.sh test_max'
	@echo '# I'll fail now so you can see this message.'
	@false

# CHECK

.PHONY: check
check:
	@echo '# If this fails immediately due to "ConnectionError",'
	@echo '# check wheter RabbitMQ is up and running!  Try this:'
	@echo '# sudo rabbitmq-server -detached'
	( cd backend && ./tests.py )

.PHONY: monkeypatch
monkeypatch:
	./tools/tweepy_monkeypatch/tell.sh

# CLEAN

${DIRS}:
	mkdir -p $@

.PHONY: clean
clean:
# Don't remove or "clean" out_pubweb!  It might be the official repo itself,
# and errors there would be bad.
	rm -rf ${OUT}

.PHONY: clean_temp
clean_temp:
	rm -f ${COFFEE_DIR}/model.coffee
	rm -rf ${TEMP}
