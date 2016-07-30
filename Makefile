OUTPUT_DIR:=out
TEMP_DIR:=temp
COFFEE_DIR:=coffee
DIRS:=${OUTPUT_DIR} ${TEMP_DIR}
JS_TEMP:=${OUTPUT_DIR}/temporarily_combined_code.js
FRONTEND_DEP:=ext/node_modules/stompjs ext/node_modules/browserify
COFFEE_ALL:=$(sort $(wildcard ${COFFEE_DIR}/*.coffee))

all: frontend backend

${DIRS}:
	mkdir -p $@

.PHONY: frontend
frontend: ${FRONTEND_DEP} clean_temp ${OUTPUT_DIR}/main.css ${OUTPUT_DIR}/main.js

${OUTPUT_DIR}/main.css: $(wildcard less/*.less) | ${DIRS}
	lessc less/main.less > $@

.PHONY: coffee
coffee: ${COFFEE_ALL} | ${DIRS}
	coffee --output ${TEMP_DIR}/ --compile ${COFFEE_DIR}/

${JS_TEMP}: coffee | ${DIRS}
	cat ${TEMP_DIR}/*.js > $@

${OUTPUT_DIR}/main.js: ${JS_TEMP} | ${DIRS} 
	browserify $< > $@

.PHONY: say 
say: 
	true ${COFFEE_ALL}

.PHONY: backend
backend:

.PHONY: start
start:
	$SCRIPTDIR/start_app.sh

.PHONY: dependencies
dependencies: ${FRONTEND_DEP}

${FRONTEND_DEP}: ext/node_modules/%: 
	npm install --prefix ./ext/ $(@:ext/node_modules/=)

.PHONY: clean
clean:
	rm -rf ${DIRS}

.PHONY: clean_temp
clean_temp:
	rm -rf ${TEMP_DIR}