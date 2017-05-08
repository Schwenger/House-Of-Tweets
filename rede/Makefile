TEX			=pdflatex
# If you change this, please don't commit such a change!
VIEWER		=evince

SOURCE		=document.tex
SOURCE_BARE:=$(patsubst %.tex,%,$(SOURCE))


all: view

$(SOURCE_BARE).pdf: $(SOURCE)
	$(TEX) -halt-on-error $<

.PHONY: clean
clean:
	rm -f $(addprefix ${SOURCE_BARE}., aux bbl blg lof log mw out pdf tdo toc)

.PHONY: spellcheck
spellcheck-en:
	aspell --lang=en_US check ${SOURCE}; done

.PHONY: view
view: ${SOURCE_BARE}.pdf
	@command -v ${VIEWER} > /dev/null || { \
		echo "Bad $$VIEWER: ${VIEWER}" ; \
		echo "If you change this, please don't commit such a change!" ; \
		exit 1 ; \
	}
	$(VIEWER) $^ &
