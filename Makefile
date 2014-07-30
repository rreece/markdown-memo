#
# pandoc Makefile
#
# author:  Ryan Reece  <ryan.reece@cern.ch>
# created: 2014-07-28
#
###############################################################################


#------------------------------------------------------------------------------
# user config
#------------------------------------------------------------------------------

AUTHOR   := John Doe
HEADER   := My Collection of Memos

DATE     := $(shell date +"%a %b %d, %Y")
CSS      := templates/markdown-memo.css

export TEXINPUTS := .//:./style//:./tex//:${TEXINPUTS}


#------------------------------------------------------------------------------
# helpers
#------------------------------------------------------------------------------

PRINT = @echo '==>  '
MD_FILES := $(filter-out .//README.md, $(shell find ./ -name '*.md'))
HTML_MD_FILES := $(MD_FILES:%.md=%.html)
PDF_MD_FILES := $(filter-out .//index.pdf, $(MD_FILES:%.md=%.pdf))


#------------------------------------------------------------------------------
# targets
#------------------------------------------------------------------------------

default: html

html: $(HTML_MD_FILES)
	$(PRINT) "html done."

index.html: index.md
	pandoc \
		--variable=siteheader:"$(HEADER)" \
		--variable=title:"$(HEADER)" \
		--variable=author-meta:"$(AUTHOR)" \
		--variable=author:"$(AUTHOR)" \
		--variable=date-meta:"$(DATE)" \
		--variable=date:"$(DATE)" \
		--variable=css:"$(CSS)" \
		--template=./templates/toc.html \
		-t html \
		-o $@ $<

%.html: %.md
	pandoc \
		--variable=siteheader:"$(HEADER)" \
		--variable=title:"$(@:%.html=$(HEADER) - %)" \
		--variable=author-meta:"$(AUTHOR)" \
		--variable=author:"$(AUTHOR)" \
		--variable=date-meta:"$(DATE)" \
		--variable=date:"$(DATE)" \
		--variable=css:"$(CSS)" \
		--template=./templates/outline.html \
		-t html \
		-o $@ $<

pdf: $(PDF_MD_FILES)
	$(PRINT) "pdf done."

%.pdf: %.md
	pandoc \
		--variable=title:"$(@:%.pdf=$(HEADER) - %)" \
		--variable=author-meta:"$(AUTHOR)" \
		--variable=author:"$(AUTHOR)" \
		--variable=date-meta:"$(DATE)" \
		--variable=date:"$(DATE)" \
		--template=templates/default.latex \
		-o $@ $<

# JUNK = *.aux *.log *.bbl *.blg *.brf *.cb *.ind *.idx *.ilg *.inx *.dvi *.toc *.out *~ ~* spellTmp *.lot *.lof *.ps *.d
JUNK = *.html *.pdf

clean:
	rm -f $(JUNK)
	$(PRINT) "clean done."

over: clean default
all: over


