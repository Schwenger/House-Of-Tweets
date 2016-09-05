FRONTEND_DEP:=ext/node_modules/stompjs ext/node_modules/browserify ext/node_modules/coffeescript-concat
OUT=out
TEMP=out/temp
LESS=less
COFFEE=coffee
HTML=html
DIRS=${OUT} ${TEMP}

all: clean_temp frontend backend

# FRONTEND

.PHONY: frontend
frontend: css js html

.PHONY: css
css: ${OUT}/main.css

${OUT}/main.css: $(wildcard ${LESS}/*.less) | ${DIRS}
	lessc ${LESS}/main.less > $@

.PHONY: html
html: ${OUT}/main.html

${OUT}/main.html: ${HTML}/main.html
	cp $^ $@

.PHONY: js
js: ${OUT}/main.js | ${DIRS}

${OUT}/main.js: ${OUT}/bundled.js | ${DIRS}
	browserify $< > $@

${OUT}/bundled.js: ${TEMP}/bundled.coffee | ${DIRS}
	coffee --output ${OUT} --compile $^

${TEMP}/bundled.coffee: $(wildcard ${COFFEE}/*.coffee) | ${DIRS}
	coffeescript-concat -I ${COFFEE} ${COFFEE}/main.coffee -o ${TEMP}/bundled.coffee

# BACKEND

.PHONY: backend
backend: 


# DEPENDENCIES

.PHONY: dependencies
dependencies: ${FRONTEND_DEP} ${BACKEND_DEP}

${FRONTEND_DEP}: ext/node_modules/%: 
	npm install --prefix ./ext/ $(@:ext/node_modules/=)

# INSTALL

.PHONY: install all
install: install_dependencies all

.PHONY: install_dependencies
install_dependencies: ${DEPEN}

# CLEAN

${DIRS}: 
	mkdir -p $@

.PHONY: clean
clean: 
	rm -rf ${OUT}

.PHONY: clean_temp
clean_temp: 
	rm -rf ${TEMP}

