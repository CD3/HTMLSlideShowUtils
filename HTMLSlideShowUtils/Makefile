# TO types: slidy, dzslides, slideous, revealjs
# Note: s5 not supported yet

# we are assuming that each presentation is in its own sub-directory
UTILSDIR=../HTMLSlideShowUtils

TO?=slidy
TO=$(shell $(UTILSDIR)/scripts/get-config-param.py to --default slidy)


EXTRAPANDOCOPTS?=$(shell $(UTILSDIR)/scripts/get-extra-pandoc-opts.py $(TO))

USER=$(shell $(UTILSDIR)/scripts/get-config-param.py push/user)
HOST=$(shell $(UTILSDIR)/scripts/get-config-param.py push/host)
ROOT=$(shell $(UTILSDIR)/scripts/get-config-param.py push/root)
DEST=$(shell $(UTILSDIR)/scripts/get-config-param.py push/dest)
NETLOC=$(shell $(UTILSDIR)/scripts/get-config-param.py push/netloc)

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
	$(UTILSDIR)/scripts/expand-macros.py slides-processed.md slides-processed.md
	$(UTILSDIR)/scripts/make-images.py slides-processed.md
	mkdir -p html
	@#
	@# we are using pandoc to do the conversion from markdown to html here.
	@# note: --self-contained does not work with mathjax
	@# --standalone creates a file with header and footer
	@# --mathjax uses mathjax javascript to render latex equation. requires an internet connection
	@# --to is the format that will be written to
	pandoc slides-processed.md -o html/00-slides.html --standalone --mathjax --to $(TO) $(EXTRAPANDOCOPTS)
	for file in $$($(UTILSDIR)/scripts/print-image-filenames.py slides-processed.md); do cp $$file html; done
	@if [ ! -d $(UTILSDIR)/data/$(TO) ]; then echo; echo; echo "ERROR: No data directory found for $(TO). Please run 'make update-data' and rerun."; echo; echo; fi
	cp -r $(UTILSDIR)/data/$(TO) html/data
	if [ -x ./postprocessor ]; then  ./postprocessor; fi

update-data:
	cd $(UTILSDIR)/data/; ./update.sh

push:
	if [ -n "$(DEST)" ] ; then ssh $(NETLOC) "mkdir -p $(ROOT)/$(DEST)"; rsync -avzP --delete html/ $(PUSHURL); fi

clean:
	rm -rf html
	if [ -n "$(DEST)" ]; then ssh $(NETLOC) "rm -rf $(ROOT)/$(DEST)"; fi

all: slides push

update: all

info:
	@echo "      utils dir: $(UTILSDIR)"
	@echo "             to: $(TO)"
	@echo "ext pandoc opts: $(EXTRAPANDOCOPTS)"
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
	cd $(NAME); ln -s ../Makefile
	@echo "---"                                                                          >  $(NAME)/slides.md
	@echo "push:"                                                                        >> $(NAME)/slides.md
	@echo "  netloc: fixme  # an rsync style remote url to push to"                      >> $(NAME)/slides.md
	@echo "  dest: fixme  # name of directory to put presentation into under the netloc" >> $(NAME)/slides.md
	@echo "title: fixme"                                                                 >> $(NAME)/slides.md
	@echo "subtitle: fixme"                                                              >> $(NAME)/slides.md
	@echo "author: fixme"                                                                >> $(NAME)/slides.md
	@echo "---"                                                                          >> $(NAME)/slides.md
	@echo "# Slide 1 Title"                                                              >> $(NAME)/slides.md
	@echo "This is (one of) Einstein's equation: $$E = mc^2$$"                           >> $(NAME)/slides.md
