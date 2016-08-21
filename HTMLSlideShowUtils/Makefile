# FORMAT types: slidy, dzslides, slideous, reveal.js, s5
FORMAT=slidy

UTILSDIR=../HTMLSlideShowUtils

USER=$(shell $(UTILSDIR)/scripts/get-config-param.py push/user)
HOST=$(shell $(UTILSDIR)/scripts/get-config-param.py push/host)
ROOT=$(shell $(UTILSDIR)/scripts/get-config-param.py push/root)
DEST=$(shell $(UTILSDIR)/scripts/get-config-param.py push/dest)

NETLOC=$(USER)@$(HOST)

PUSHURL="$(NETLOC):$(ROOT)/$(DEST)"


slides:
	# this target should create a directory named html containing the presentation
	# all pre and post processing should be done here
	#
	# we are using pandoc to do the conversion from markdown to html here.
	$(UTILSDIR)/scripts/preprocess.py slides.md slides-processed.md
	$(UTILSDIR)/scripts/make-images.py slides-processed.md
	mkdir -p html
	# note: --self-contained does not work with mathjax
	# --standalone creates a file with header and footer
	# --mathjax uses mathjax javascript to render latex equation. requires an internet connection
	# --to is the format that will be written to
	# --css is a css file to use
	pandoc slides-processed.md -o html/00-slides.html --standalone --mathjax --to $(FORMAT) --css css/$(FORMAT).css
	for file in $$($(UTILSDIR)/scripts/print-image-filenames.py slides-processed.md); do cp $$file html; done
	cp -r $(UTILSDIR)/data/* html

push:
	if [ -n "$(DEST)" ] ; then ssh $(NETLOC) "mkdir -p $(ROOT)/$(DEST)"; rsync -avzP --delete html/ $(PUSHURL); fi

all: slides push

update: all

test:
	@echo "utils dir: $(UTILSDIR)"
	@echo "push/user: $(USER)"
	@echo "push/host: $(HOST)"
	@echo "push/root: $(ROOT)"
	@echo "push/dest: $(DEST)"
	@echo "   netloc: $(NETLOC)"
	@echo " push url: $(PUSHURL)"

pngslides:
	ls Slide*.PNG | sort -V | sed 's/^/# _\n![](/; s/$$/)\n/'

clean:
	rm -rf html
	if [ -n "$(DEST)" ]; then ssh $(NETLOC) "rm -rf $(ROOT)/$(DEST)"; fi
