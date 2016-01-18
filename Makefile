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

export TEXINPUTS := .//:./style//:./tex//:${TEXINPUTS}

OUTNAME := doc


#------------------------------------------------------------------------------
# helpers
#------------------------------------------------------------------------------

PRINT = @echo '==>  '

DATE     := $(shell date +"%a %b %d, %Y")
#MD_FILES := $(filter-out .//README.md, $(shell find ./ -name '*.md'))
MD_FILES := $(filter-out README.md, $(wildcard *.md))
HTML_FILES := $(MD_FILES:%.md=%.html)
MD_FILES := $(filter-out index.md, $(MD_FILES))
PDF_FILES := $(MD_FILES:%.md=%.pdf)

# MD_FILES   =            chap1.md   chap2.md   ...
# HTML_FILES = index.html chap1.html chap2.html ...
# PDF_FILES  =            chap1.pdf  chap2.pdf  ...


#------------------------------------------------------------------------------
# targets
#------------------------------------------------------------------------------

default: html

html: $(HTML_FILES)
	$(PRINT) "html done."

index.html: index.md meta.yaml
	pandoc \
		-t html \
		--ascii \
		--standalone \
		--smart \
		--variable=date-meta:"$(DATE)" \
		--variable=css:templates/markdown-memo.css \
		--template=./templates/toc.html \
		-o $@ $< meta.yaml

# create html
%.html: %.md mybib.bib meta.yaml
	pandoc \
		-t html \
		--ascii \
		--standalone \
		--smart \
		--variable=date-meta:"$(DATE)" \
		--variable=css:templates/markdown-memo.css \
		--template=./templates/outline.html \
		--mathjax \
		--bibliography=mybib.bib \
		--filter pandoc-citeproc \
		-o $@ $< meta.yaml

$(OUTNAME).html: $(MD_FILES) mybib.bib meta.yaml
	pandoc \
		-t html \
		--ascii \
		--standalone \
		--smart \
		--variable=date-meta:"$(DATE)" \
		--variable=css:templates/markdown-memo.css \
		--template=./templates/outline.html \
		--mathjax \
		--bibliography=mybib.bib \
		--filter pandoc-citeproc \
		-o $@ $(MD_FILES) meta.yaml

# create pdf with metadata included in the md in yaml
%.pdf: %.md mybib.bib meta.yaml
	pandoc \
		--standalone \
		--smart \
		--variable=date-meta:"$(DATE)" \
		--template=templates/default.latex \
		--toc \
		--filter pandoc-eqnos \
		--bibliography=mybib.bib \
		--filter pandoc-citeproc \
		-o $@ $< meta.yaml

$(OUTNAME).pdf: $(MD_FILES) mybib.bib meta.yaml
	pandoc \
		--standalone \
		--smart \
		--variable=date-meta:"$(DATE)" \
		--template=templates/default.latex \
		--toc \
		--filter pandoc-eqnos \
		--bibliography=mybib.bib \
		--filter pandoc-citeproc \
		-o doc.pdf $(MD_FILES) meta.yaml
	$(PRINT) "pdf done."


# output md with references replaced and bibliography created
%.mds: %.md mybib.bib meta.yaml
	pandoc \
		-t markdown_github \
		--standalone \
		--smart \
		--toc \
		--bibliography=mybib.bib \
		--filter pandoc-citeproc \
		-o $@.tmp $< meta.yaml
	cat $@.tmp | sed -E 's/\[([0-9][0-9]?[0-9]?)\]/\[\^\1\]/g' | sed -E 's/^\[\^([0-9][0-9]?[0-9]?)\]\ /\[\^\1\]:\ /' > $@
	rm -f $@.tmp

$(OUTNAME).mds: $(MD_FILES) mybib.bib meta.yaml
	pandoc \
		-t markdown_github \
		--standalone \
		--smart \
		--toc \
		--bibliography=mybib.bib \
		--filter pandoc-citeproc \
		-o $@.tmp $(MD_FILES) meta.yaml
	cat $@.tmp | sed -E 's/\[([0-9][0-9]?[0-9]?)\]/\[\^\1\]/g' | sed -E 's/^\[\^([0-9][0-9]?[0-9]?)\]\ /\[\^\1\]:\ /' > $@
	rm -f $@.tmp


# create html from mds
%.htmls: %.mds
	pandoc \
		-t html \
		--ascii \
		--standalone \
		--smart \
		--variable=date-meta:"$(DATE)" \
		--variable=css:templates/markdown-memo.css \
		--template=./templates/outline.html \
		-o $@ $< meta.yaml

# create tex with references replaced and bibliography created
%.tex: %.md mybib.bib meta.yaml
	pandoc \
		-t latex \
		--ascii \
		--standalone \
		--smart \
		--template=templates/default.latex \
		--toc \
		--bibliography=mybib.bib \
		--filter pandoc-citeproc \
		-o $@ $< meta.yaml
	pdflatex $@

$(OUTNAME).tex: $(MD_FILES) mybib.bib meta.yaml
	pandoc \
		-t latex \
		--ascii \
		--standalone \
		--smart \
		--template=templates/default.latex \
		--toc \
		--bibliography=mybib.bib \
		--filter pandoc-citeproc \
		-o $@ $(MD_FILES) meta.yaml
	pdflatex $@

mybib.bib: $(MD_FILES)
	cat bibs/*.bib > mybib.bib
	$(PRINT) "mybib.bib done."

# JUNK = *.aux *.log *.bbl *.blg *.brf *.cb *.ind *.idx *.ilg *.inx *.dvi *.toc *.out *~ ~* spellTmp *.lot *.lof *.ps *.d
JUNK = *.mds *.htmls *.tex *.aux *.dvi *.fdb_latexmk *.fls *.log *.out *.toc *.bib *.tmp
OUTS = *.html *.pdf

clean:
	rm -f $(JUNK)
	$(PRINT) "clean done."

realclean: clean
	rm -f $(OUTS)
	$(PRINT) "realclean done."

over: realclean default
all: over

