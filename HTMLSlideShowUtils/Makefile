# TO types: slidy, dzslides, slideous, revealjs
# Note: s5 not supported yet

# we are assuming that each presentation is in its own sub-directory
UTILSDIR=$(wildcard HTMLSlideShowUtils)
ifeq ($(strip $(UTILSDIR)),)
UTILSDIR=$(wildcard ../HTMLSlideShowUtils)
endif
ifeq ($(strip $(UTILSDIR)),)
UTILSDIR=COULD_NOT_FIND_UTILS_DIR
endif

TO?=slidy
ifneq ($(strip $(UTILSDIR)),COULD_NOT_FIND_UTILS_DIR)
TO=$(shell $(PYTHON3CMD) $(UTILSDIR)/scripts/get-config-param.py to --default slidy)

EXTRARSYNCOPTS?=$(shell $(PYTHON3CMD) $(UTILSDIR)/scripts/get-config-param.py extra-rsync-opts --default '')
PUSHCMD?=$(shell $(PYTHON3CMD) $(UTILSDIR)/scripts/get-config-param.py push/cmd --default 'rsync -avzP --delete $(EXTRARSYNCOPTS)')
PANDOCCMD?=$(shell $(PYTHON3CMD) $(UTILSDIR)/scripts/get-config-param.py pandoc/cmd --default 'pandoc')
PYTHON3CMD?=python3

USER=$(shell $(PYTHON3CMD) $(UTILSDIR)/scripts/get-config-param.py push/user)
HOST=$(shell $(PYTHON3CMD) $(UTILSDIR)/scripts/get-config-param.py push/host)
ROOT=$(shell $(PYTHON3CMD) $(UTILSDIR)/scripts/get-config-param.py push/root)
DEST=$(shell $(PYTHON3CMD) $(UTILSDIR)/scripts/get-config-param.py push/dest)
NETLOC=$(shell $(PYTHON3CMD) $(UTILSDIR)/scripts/get-config-param.py push/netloc)
endif

ifeq ($(NETLOC),None)
	NETLOC=$(USER)@$(HOST)
endif

PUSHURL="$(NETLOC):$(ROOT)/$(DEST)"


slides:
	@# this target should create a directory named html containing the presentation
	@# all pre and post processing should be done here
	rm -rf html
	cp slides.md slides-processed.md
	if [ -x ./preprocessor ]; then  ./preprocessor; fi
	$(PYTHON3CMD) $(UTILSDIR)/scripts/expand-macros.py slides-processed.md slides-processed.md
	mkdir -p html
	$(PYTHON3CMD) $(UTILSDIR)/scripts/build-slideshow.py slides-processed.md html/00-slides.html
	for file in $$($(PYTHON3CMD) $(UTILSDIR)/scripts/print-image-filenames.py slides-processed.md); do cp $$file html; done
	@if [ ! -d $(UTILSDIR)/data/$(TO) ]; then echo; echo; echo "ERROR: No data directory found for $(TO). Please run 'make update-data' and rerun."; echo; echo; fi
	cp -r $(UTILSDIR)/data/$(TO) html/data
	if [ -x ./postprocessor ]; then  ./postprocessor; fi


# support for building PDFs too.
document:
	cp document.md document-processed.md
	if [ -x ./preprocessor ]; then  ./preprocessor; fi
	$(PYTHON3CMD) $(UTILSDIR)/scripts/expand-macros.py slides-processed.md slides-processed.md
	$(PYTHON3CMD) $(UTILSDIR)/scripts/make-images.py -s slides-processed.md
	$(PANDOCCMD) document-processed.md -o document.pdf
	if [ -x ./postprocessor ]; then  ./postprocessor; fi

update-data:
	cd $(UTILSDIR)/data/; ./update.sh

push:
	if [ -n "$(DEST)" ] ; then ssh $(NETLOC) "mkdir -p $(ROOT)/$(DEST)"; $(PUSHCMD) html/ $(PUSHURL); fi

clean:
	rm -rf html
	if [ -n "$(DEST)" ]; then ssh $(NETLOC) "rm -rf $(ROOT)/$(DEST)"; fi

all: slides push

update: all

info:
	@echo "      utils dir: $(UTILSDIR)"
	@echo "             to: $(TO)"
	@echo " ext rsync opts: $(EXTRARSYNCOPTS)"
	@echo "     pandoc/cmd: $(PANDOCCMD)"
	@echo "       push/cmd: $(PUSHCMD)"
	@echo "      push/user: $(USER)"
	@echo "      push/host: $(HOST)"
	@echo "      push/root: $(ROOT)"
	@echo "      push/dest: $(DEST)"
	@echo "         netloc: $(NETLOC)"
	@echo "       push url: $(PUSHURL)"
	@echo "        preproc: $(shell if [ -x ./preprocessor  ]; then echo YES; else echo NO; fi)"
	@echo "       postproc: $(shell if [ -x ./postprocessor ]; then echo YES; else echo NO; fi)"

pngslides:
	@find ./ -maxdepth 1 -iname 'slide*.png' | sort -V | sed 's/^/# _\n![](/; s/$$/)\n/'

pdf2png:
	convert slides.pdf Slides.png

NAME?=NewPresentation
new-show:
	mkdir $(NAME)
	cd $(NAME); ln -s ../Makefile; ln -s ../config.yaml; cp ../demo/slides.md ./
