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

DATE     := $(shell date +"%a %b %d, %Y")

AUTHOR   := Ryan Reece
HEADER   := My Collection of Memos
FOOTER   := <p><i>Ryan Reece</i> <br/> <img src=\"img/my_email.png\" alt=\"my email address\"/> <br/> $(DATE)</p>

CSS      := templates/markdown-memo.css
TEMPLATE := templates/outline.html

export TEXINPUTS := .//:./style//:./tex//:${TEXINPUTS}


#------------------------------------------------------------------------------
# helpers
#------------------------------------------------------------------------------

PRINT = @echo '==>  '
MD_FILES := $(filter-out .//README.md, $(shell find ./ -name '*.md'))
HTML_MD_FILES := $(MD_FILES:%.md=%.html)
PDF_MD_FILES := $(MD_FILES:%.md=%.pdf)


#------------------------------------------------------------------------------
# targets
#------------------------------------------------------------------------------

default: html

html: $(HTML_MD_FILES)
	$(PRINT) "html done."

index.html: index.md
	pandoc --variable=siteheader:"$(HEADER)" --variable=sitefooter:"$(FOOTER)" --variable=title:"$(@:%.html=$(HEADER) - %)" --variable=author-meta:"$(AUTHOR)" --variable=date-meta:"$(DATE)" --variable=css:"$(CSS)" --ascii -t html --template=$(TEMPLATE) -o $@ $<

%.html: %.md
	pandoc --variable=siteheader:"$(HEADER)" --variable=sitefooter:"$(FOOTER)" --variable=title:"$(@:%.html=$(HEADER) - %)" --variable=author-meta:"$(AUTHOR)" --variable=date-meta:"$(DATE)" --variable=css:"$(CSS)" --ascii -t html -B ./templates/back-to-toc.html -A ./templates/back-to-toc.html --template=$(TEMPLATE) -o $@ $<

pdf: $(PDF_MD_FILES)
	$(PRINT) "pdf done."

%.pdf: %.md
	pandoc --variable=title:"$(@:%.pdf=$(HEADER) - %)" --variable=author-meta:"$(AUTHOR)" --variable=date-meta:"$(DATE)" --variable=author:"$(AUTHOR)" --variable=date:"$(DATE)" --template=templates/default.latex -o $@ $<

# JUNK = *.aux *.log *.bbl *.blg *.brf *.cb *.ind *.idx *.ilg *.inx *.dvi *.toc *.out *~ ~* spellTmp *.lot *.lof *.ps *.d
JUNK = *.html *.pdf

clean:
	rm -f $(JUNK)
	$(PRINT) "clean done."

over: clean default
all: over


