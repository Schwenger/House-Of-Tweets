FRONTEND_DEP:=ext/node_modules/stompjs ext/node_modules/browserify ext/node_modules/coffeescript-concat ext/node_modules/less
PUBWEB_DEP:=ext/node_modules/browserify ext/node_modules/coffeescript-concat ext/node_modules/jquery-on-infinite-scroll
# FIXME: install and use pubweb dependencies
BACKEND_DEP:=bs4 pika pydub requests tweepy typing

BROWSERIFY?=ext/node_modules/.bin/browserify
COFFEESCRIPT_CONCAT?=ext/node_modules/.bin/coffeescript-concat
LESSC?=ext/node_modules/.bin/lessc

OUT=out
TEMP=temp
LESS=less
COFFEE=coffee
MODEL=${COFFEE}/model
HTML=html
DIRS=${OUT} ${TEMP} out_pubweb/imgs out_pubweb/css out_pubweb/js
MODELS:=$(wildcard ${MODEL}/*.coffee)


all: frontend backend

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
	coffee --output ${TEMP} --compile $<

${TEMP}/bundled.coffee: ${COFFEE}/model.coffee $(wildcard ${COFFEE}/*.coffee) | ${DIRS}
	${COFFEESCRIPT_CONCAT} -I ${COFFEE} $< -o $@

${COFFEE}/model.coffee: ${COFFEE}/model_empty.coffee ${MODELS} | ${DIRS}
	cat ${COFFEE}/model_empty.coffee ${MODELS} > $@

# BACKEND

.PHONY: backend
backend:
# Needs no building.

# PUBWEB
# TODO: Dependencies?

# Yes, this feels a lot like "Please put me into my own namespace".
# No, due to the shared npm accesses it just so doesn't make sense to
# create a different Makefile for that.
PUBWEB_HTML_NAMES:=index index_en about about_en
PUBWEB_HTML_SRC:=${patsubst %,tools/WebsiteGen/autogen/%.html,${PUBWEB_HTML_NAMES}}
PUBWEB_HTML_DST:=${patsubst %,out_pubweb/%.html,${PUBWEB_HTML_NAMES}}
PUBWEB_STATIC_SRC:=$(wildcard pubweb/static/*.*) $(wildcard pubweb/static/*/*.*)
# PUBWEB_STATIC_DST should also include the images, but:
# FIXME: Come up with a clever way to "regenerate"/cache the chosen bird images
#        (WITHOUT pulling from hot_crawler_cache)
PUBWEB_STATIC_DST:=${patsubst pubweb/static/%,out_pubweb/%,${PUBWEB_STATIC_SRC}}
PUBWEB_DYNAMIC_DST:=out_pubweb/js/main.js ${PUBWEB_HTML_DST}

.PHONY: pubweb
pubweb: ${PUBWEB_DYNAMIC_DST} ${PUBWEB_STATIC_DST}

.PHONY: pubweb_dyn
pubweb_dyn: ${PUBWEB_DYNAMIC_DST}

${PUBWEB_HTML_DST}: out_pubweb/%: tools/WebsiteGen/autogen/% | ${DIRS}
	cp $< $@

# Slightly overzealous, but whatever
${PUBWEB_HTML_SRC}: %: tools/WebsiteGen/about.html.in tools/WebsiteGen/index.html.in tools/WebsiteGen/mk_html.py
	( cd tools/WebsiteGen && ./mk_html.py )

out_pubweb/js/main.js: ${TEMP}/pubweb_bundled.js | ${DIRS}
# FIXME: Minify?
	${BROWSERIFY} $< > $@

${TEMP}/pubweb_bundled.js: ${TEMP}/pubweb_bundled.coffee | ${DIRS}
	coffee --output ${TEMP} --compile $<

${TEMP}/pubweb_bundled.coffee: pubweb/main.coffee tools/WebsiteGen/birds.coffee | ${DIRS}
	${COFFEESCRIPT_CONCAT} -I tools/WebsiteGen/ $< -o $@

tools/WebsiteGen/birds.coffee: tools/WebsiteGen/mk_json.py tools/PhotoMiner/checkout_birds.json
	( cd tools/WebsiteGen && ./mk_json.py )

${PUBWEB_STATIC_DST}: out_pubweb/%: pubweb/static/% | ${DIRS}
	cp $< $@

# DEPENDENCIES

.PHONY: install_dependencies
install_dependencies: ${FRONTEND_DEP}
	@if command -v pip3 &> /dev/null ; \
	then \
		echo pip3 install ${BACKEND_DEP} ; \
		pip3 install ${BACKEND_DEP} ; \
	elif command -v pip &> /dev/null ; \
	then \
		echo pip install ${BACKEND_DEP} ; \
		pip install ${BACKEND_DEP} ; \
	else \
		echo "# Can't find pip or pip3.  Is it installed?" ; \
		false ; \
	fi

${FRONTEND_DEP}: ext/node_modules/%:
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
	rm -f ${COFFEE}/model.coffee
	rm -rf ${TEMP}
