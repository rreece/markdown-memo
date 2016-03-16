
# pandoc Makefile
#
# author:  Ryan Reece  <ryan.reece@cern.ch>
# created: 2014-07-28
#
###############################################################################


##-----------------------------------------------------------------------------
## user config
##-----------------------------------------------------------------------------

export TEXINPUTS := .//:./style//:./tex//:${TEXINPUTS}

OUTNAME := doc
OPS_FULLPDF:=templates/refs_tex.md templates/backmatter.md
OPS_FULLHTML:=templates/refs.md templates/backmatter.md
OPS_SECTION:=templates/refs_subsection.md templates/backmatter.md


##-----------------------------------------------------------------------------
## helpers
##-----------------------------------------------------------------------------

PRINT = @echo '==>  '

DATE     := $(shell date +"%a %b %d, %Y")
#MD_FILES := $(filter-out .//README.md, $(shell find ./ -name '*.md'))
MD_FILES := $(filter-out README.md, $(wildcard *.md))
HTML_FILES := $(MD_FILES:%.md=%.html)
MD_FILES := $(filter-out index.md, $(MD_FILES))
PDF_FILES := $(MD_FILES:%.md=%.pdf)
MD_FILES_WITH_REFS := $(shell egrep -l '@' *.md)


## MD_FILES   =            chap1.md   chap2.md   ...
## HTML_FILES = index.html chap1.html chap2.html ...
## PDF_FILES  =            chap1.pdf  chap2.pdf  ...


##-----------------------------------------------------------------------------
## targets
##-----------------------------------------------------------------------------

default: html

all: html pdf

html: $(HTML_FILES)
	$(PRINT) "html done."

pdf: $(OUTNAME).pdf

index.html: index.md meta.yaml
	pandoc \
		-t html \
		--ascii \
		--standalone \
		--smart \
		--variable=date-meta:"$(DATE)" \
		--variable=css:templates/markdown-memo.css \
		--template=./templates/index_template.html \
		-o $@ $< meta.yaml

$(OUTNAME).html: $(MD_FILES) mybib.bib meta.yaml
	pandoc \
		-t html \
		--ascii \
		--standalone \
		--smart \
		--variable=date-meta:"$(DATE)" \
		--variable=css:templates/markdown-memo.css \
		--template=./templates/index_template.html \
		--mathjax \
		--bibliography=mybib.bib \
		--filter pandoc-crossref \
		--filter pandoc-citeproc \
		-o $@ $(MD_FILES) $(OPS_FULLHTML) meta.yaml
	$(PRINT) "make $@ done."

## create html
%.html: %.md mybib.bib meta.yaml
	pandoc \
		-t html \
		--ascii \
		--standalone \
		--smart \
		--template=./templates/outline_template.html \
		-o $@.tmp $< meta.yaml
	rm -f meta.yaml.tmp
	grep -E '(^\.\.\.)' -v meta.yaml | grep -v -e '^$$' >> meta.yaml.tmp
	echo "# ---------------------------------------------------" >> meta.yaml.tmp
	echo `cat $@.tmp | grep -E "<title.*>(.*?)</title>" | sed 's/<title.*>\(.*\)<\/title>/doc_title: "\1"/'` >> meta.yaml.tmp
	echo `cat $@.tmp | grep -E "<h1.*>(.*?)</h1>" | head -n1 | sed 's/<h1.*>\(.*\)<\/h1>/page_title: "\1"/'` >> meta.yaml.tmp
	echo '...\n' >> meta.yaml.tmp
	pandoc \
		-t html \
		--ascii \
		--standalone \
		--smart \
		--variable=date-meta:"$(DATE)" \
		--variable=css:templates/markdown-memo.css \
		--template=./templates/outline_template.html \
		--mathjax \
		--bibliography=mybib.bib \
		--filter pandoc-crossref \
		--filter pandoc-citeproc \
		-o $@ $< $(OPS_SECTION) meta.yaml.tmp
	rm -f meta.yaml.tmp $@.tmp
	$(PRINT) "make $@ done."

## create the full pdf 
$(OUTNAME).pdf: $(MD_FILES) mybib.bib meta.yaml
	pandoc \
		--standalone \
		--smart \
		--variable=date-meta:"$(DATE)" \
		--template=templates/default_template.tex \
		--toc \
		--filter pandoc-crossref \
		--filter pandoc-eqnos \
		--bibliography=mybib.bib \
		--filter pandoc-citeproc \
		-o $(OUTNAME).pdf $(MD_FILES) $(OPS_FULLPDF) meta.yaml
	$(PRINT) "make $@ done."

## create the full pdf via pandoc to tex then pdflatex
#$(OUTNAME).pdf: $(OUTNAME).tex
#	pdflatex -interaction=nonstopmode $< &> latex.log
#	pdflatex -interaction=nonstopmode $< &> latex.log
#	$(PRINT) "make $@ done."

## create the pdf for a section
%.pdf: %.md mybib.bib meta.yaml
	pandoc \
		--standalone \
		--smart \
		--variable=date-meta:"$(DATE)" \
		--template=templates/default_template.tex \
		--toc \
		--filter pandoc-crossref \
		--filter pandoc-eqnos \
		--bibliography=mybib.bib \
		--filter pandoc-citeproc \
		-o $@ $< $(OPS_SECTION) meta.yaml
	$(PRINT) "make $@ done."

## create md with references replaced and bibliography created
$(OUTNAME).mds: $(MD_FILES) mybib.bib meta.yaml
	pandoc \
		-t markdown_github \
		--standalone \
		--smart \
		--toc \
		--bibliography=mybib.bib \
		--filter pandoc-citeproc \
		-o $@.tmp $(MD_FILES) $(OPS_FULLHTML) meta.yaml
	cat $@.tmp | sed -E 's/\[([0-9][0-9]?[0-9]?)\]/\[\^\1\]/g' | sed -E 's/^\[\^([0-9][0-9]?[0-9]?)\]\ /\[\^\1\]:\ /' > $@
	rm -f $@.tmp
	$(PRINT) "make $@ done."

%.mds: %.md mybib.bib meta.yaml
	pandoc \
		-t markdown_github \
		--standalone \
		--smart \
		--toc \
		--bibliography=mybib.bib \
		--filter pandoc-citeproc \
		-o $@.tmp $< $(OPS_SECTION) meta.yaml
	cat $@.tmp | sed -E 's/\[([0-9][0-9]?[0-9]?)\]/\[\^\1\]/g' | sed -E 's/^\[\^([0-9][0-9]?[0-9]?)\]\ /\[\^\1\]:\ /' > $@
	rm -f $@.tmp
	$(PRINT) "make $@ done."

## create html from mds
%.htmls: %.mds
	pandoc \
		-t html \
		--ascii \
		--standalone \
		--smart \
		--variable=date-meta:"$(DATE)" \
		--variable=css:templates/markdown-memo.css \
		--template=./templates/outline_template.html \
		-o $@ $< meta.yaml
	$(PRINT) "make $@ done."

## create tex with references replaced and bibliography created
$(OUTNAME).tex: $(MD_FILES) mybib.bib meta.yaml
	pandoc \
		-t latex \
		--ascii \
		--standalone \
		--smart \
		--template=templates/default_template.tex \
		--toc \
		--filter pandoc-crossref \
		--bibliography=mybib.bib \
		--filter pandoc-citeproc \
		-o $@ $(MD_FILES) $(OPS_FULLPDF) meta.yaml
	$(PRINT) "make $@ done."

%.tex: %.md mybib.bib meta.yaml
	pandoc \
		-t latex \
		--ascii \
		--standalone \
		--smart \
		--template=templates/default_template.tex \
		--toc \
		--filter pandoc-crossref \
		--bibliography=mybib.bib \
		--filter pandoc-citeproc \
		-o $@ $< $(OPS_SECTION) meta.yaml
	$(PRINT) "make $@ done."

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

