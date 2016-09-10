FRONTEND_DEP:=ext/node_modules/stompjs ext/node_modules/browserify ext/node_modules/coffeescript-concat ext/node_modules/less

BROWSERIFY?=ext/node_modules/.bin/browserify
COFFEESCRIPT_CONCAT?=ext/node_modules/.bin/coffeescript-concat
LESSC?=ext/node_modules/.bin/lessc

OUT=out
TEMP=out/temp
LESS=less
COFFEE=coffee
MODEL=${COFFEE}/model
HTML=html
DIRS=${OUT} ${TEMP}
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

${OUT}/main.js: ${OUT}/bundled.js | ${DIRS}
	${BROWSERIFY} $< > $@

${OUT}/bundled.js: ${TEMP}/bundled.coffee | ${DIRS}
	coffee --output ${OUT} --compile $^

${TEMP}/bundled.coffee: ${COFFEE}/model.coffee $(wildcard ${COFFEE}/*.coffee) | ${DIRS}
	${COFFEESCRIPT_CONCAT} -I ${COFFEE} ${COFFEE}/main.coffee -o ${TEMP}/bundled.coffee

${COFFEE}/model.coffee: ${COFFEE}/model_empty.coffee ${MODELS} | ${DIRS}
	cat ${COFFEE}/model_empty.coffee ${MODELS} > $@

# BACKEND

.PHONY: backend
backend:
# Needs no building.

# DEPENDENCIES

.PHONY: install_dependencies
install_dependencies: ${FRONTEND_DEP}

${FRONTEND_DEP}: ext/node_modules/%:
	@mkdir -p ext/node_modules
	npm install --prefix ./ext/ $(patsubst ext/node_modules/%,%,$@)

# START

.PHONY: start
start: 
	@echo '# If this fails immediately due to "ConnectionError",'
	@echo '# check wheter RabbitMQ is up and running!  Try this:'
	@echo '# sudo rabbitmq-server -detached'
	( cd backend && ./startBackend.py )

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
	rm -rf ${OUT}

.PHONY: clean_temp
clean_temp: 
	rm -f ${COFFEE}/model.coffee
	rm -rf ${TEMP}
