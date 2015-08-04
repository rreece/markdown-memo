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

AUTHOR   := Ryan Reece
HEADER   := Drafts for my blog: statisticalsignificance.net
# LICENSE  := Licensed for sharing under <a rel=\"license\" href=\"http://creativecommons.org/licenses/by/4.0/\">CC-BY-4.0</a>
LICENSE  := &copy; 2014-2015 Ryan Reece. All rights reserved.
# LICENSE  :=

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
		--variable=license:"$(LICENSE)" \
		--template=./templates/toc.html \
		-t html --ascii \
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
		--variable=license:"$(LICENSE)" \
		--template=./templates/outline.html \
		-t html --ascii \
		-o $@ $<

pdf: $(PDF_MD_FILES)
	$(PRINT) "pdf done."

%.pdf: %.md
	pandoc \
		--template=templates/default.latex \
		--variable=fontfamily:"mathpazo" \
		--toc \
		$< -o $@ 

%.pd: %.md
	pandoc \
		--variable=title:"$(@:%.pdf=$(HEADER) - %)" \
		--variable=author-meta:"$(AUTHOR)" \
		--variable=author:"$(AUTHOR)" \
		--variable=date-meta:"$(DATE)" \
		--variable=date:"$(DATE)" \
		--template=templates/default.latex \
		--variable=fontfamily:"mathpazo" \
		--toc \
		-o $@ $<

# JUNK = *.aux *.log *.bbl *.blg *.brf *.cb *.ind *.idx *.ilg *.inx *.dvi *.toc *.out *~ ~* spellTmp *.lot *.lof *.ps *.d
JUNK = *.html *.pdf

clean:
	rm -f $(JUNK)
	$(PRINT) "clean done."

over: clean default
all: over


