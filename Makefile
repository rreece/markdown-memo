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

OUTPUT := $(shell cat meta.yaml | grep output | awk '{split($$0,a,":"); print a[2]}' | xargs)
DOREFS := $(filter $(shell cat meta.yaml | grep ^dorefs | awk '{split($$0,a,":"); print a[2]}' | xargs),true)

OPS_FULLPDF := $(if $(DOREFS),templates/refs_tex.md templates/backmatter.md,templates/backmatter.md)
OPS_FULLHTML := $(if $(DOREFS),templates/refs.md templates/backmatter.md,templates/backmatter.md)
OPS_SECTION := $(if $(DOREFS),templates/refs_subsection.md templates/backmatter.md,templates/backmatter.md)


##-----------------------------------------------------------------------------
## helpers
##-----------------------------------------------------------------------------

PRINT = @echo '==>  '

DATE     := $(shell date +"%a %b %d, %Y")
MD_FILES := $(filter-out README.md, $(wildcard *.md))
MD_FILES := $(filter-out index.md, $(MD_FILES))
HTML_FILES := $(MD_FILES:%.md=%.html)
PDF_FILES := $(MD_FILES:%.md=%.pdf)
MD_FILES_WITH_REFS := $(shell egrep -l '@' *.md)
BIB_TXT_FILES := $(wildcard bibs/*.txt)


## MD_FILES   =  chap1.md   chap2.md   ...
## HTML_FILES =  chap1.html chap2.html ...
## PDF_FILES  =  chap1.pdf  chap2.pdf  ...


##-----------------------------------------------------------------------------
## targets
##-----------------------------------------------------------------------------

default: pdf

all: html pdf

html: $(HTML_FILES) index.html wordcount/wc.csv
	$(PRINT) "html done."

pdf: $(OUTPUT).pdf wordcount/wc.csv

index.md: $(MD_FILES)
	@if [ -f index.txt ]; \
	then \
		cp index.txt $@ ; \
	else \
		python templates/make_md_index.py --out=$@ $(MD_FILES) ; \
	fi
	$(PRINT) "make $@ done."

index.html: index.md meta.yaml
	@pandoc \
		-t html \
		--ascii \
		--standalone \
		--smart \
		--variable=date-meta:"$(DATE)" \
		--variable=css:templates/markdown-memo.css \
		--template=./templates/index_template.html \
		-o $@ $< meta.yaml
	$(PRINT) "make $@ done."

$(OUTPUT).html: $(MD_FILES) bibs/mybib.bib meta.yaml
	@pandoc \
		-t html \
		--ascii \
		--number-sections \
		--standalone \
		--smart \
		--variable=date-meta:"$(DATE)" \
		--variable=css:templates/markdown-memo.css \
		--template=./templates/index_template.html \
		--mathjax \
		--bibliography=bibs/mybib.bib \
		--filter pandoc-crossref \
		--filter pandoc-citeproc \
		-o $@ $(MD_FILES) $(OPS_FULLHTML) meta.yaml
	$(PRINT) "make $@ done."

## create html
%.html: %.md bibs/mybib.bib meta.yaml
	@pandoc \
		-t html \
		--ascii \
		--standalone \
		--smart \
		--template=./templates/outline_template.html \
		-o $@.tmp $< meta.yaml
	@rm -f meta.yaml.tmp
	@grep -E '(^\.\.\.)' -v meta.yaml | grep -v -e '^$$' >> meta.yaml.tmp
	@echo "# ---------------------------------------------------" >> meta.yaml.tmp
	@echo `cat $@.tmp | grep -E "<title.*>(.*?)</title>" | sed 's/<title.*>\(.*\)<\/title>/doc_title: "\1"/'` >> meta.yaml.tmp
	@echo `cat $@.tmp | grep -E "<h1.*>(.*?)</h1>" | head -n1 | sed 's/<h1.*>\(.*\)<\/h1>/page_title: "\1"/'` >> meta.yaml.tmp
	@echo '...\n' >> meta.yaml.tmp
	@pandoc \
		-t html \
		--ascii \
		--standalone \
		--smart \
		--variable=date-meta:"$(DATE)" \
		--variable=css:templates/markdown-memo.css \
		--template=./templates/outline_template.html \
		--mathjax \
		--bibliography=bibs/mybib.bib \
		--filter pandoc-crossref \
		--filter pandoc-citeproc \
		-o $@ $< $(OPS_SECTION) meta.yaml.tmp
	@rm -f meta.yaml.tmp $@.tmp
	$(PRINT) "make $@ done."

## create the full pdf 
#$(OUTPUT).pdf: $(MD_FILES) bibs/mybib.bib meta.yaml
#	pandoc \
#		--standalone \
#		--smart \
#		--variable=date-meta:"$(DATE)" \
#		--template=templates/default_template.tex \
#		--filter pandoc-crossref \
#		--filter pandoc-eqnos \
#		--bibliography=bibs/mybib.bib \
#		--filter pandoc-citeproc \
#		-o $(OUTPUT).pdf $(MD_FILES) $(OPS_FULLPDF) meta.yaml
#	$(PRINT) "make $@ done."

# create the full pdf via pandoc to tex then pdflatex
$(OUTPUT).pdf: $(OUTPUT).tex
	@pdflatex -interaction=nonstopmode $< &> latex.log
	@pdflatex -interaction=nonstopmode $< &> latex.log
	$(PRINT) "make $@ done."

## create the pdf for a section
%.pdf: %.md bibs/mybib.bib meta.yaml
	@pandoc \
		--standalone \
		--smart \
		--variable=date-meta:"$(DATE)" \
		--template=templates/default_template.tex \
		--filter pandoc-crossref \
		--filter pandoc-eqnos \
		--bibliography=bibs/mybib.bib \
		--filter pandoc-citeproc \
		-o $@ $< $(OPS_SECTION) meta.yaml
	$(PRINT) "make $@ done."

## create tex with references replaced and bibliography created
$(OUTPUT).tex: $(MD_FILES) bibs/mybib.bib meta.yaml
	@pandoc \
		-t latex \
		--ascii \
		--standalone \
		--smart \
		--template=templates/default_template.tex \
		--filter pandoc-crossref \
		--bibliography=bibs/mybib.bib \
		--filter pandoc-citeproc \
		-o $@ $(MD_FILES) $(OPS_FULLPDF) meta.yaml
	@python templates/transform_tex.py $@
	$(PRINT) "make $@ done."

%.tex: %.md bibs/mybib.bib meta.yaml
	@pandoc \
		-t latex \
		--ascii \
		--standalone \
		--smart \
		--template=templates/default_template.tex \
		--filter pandoc-crossref \
		--bibliography=bibs/mybib.bib \
		--filter pandoc-citeproc \
		-o $@ $< $(OPS_SECTION) meta.yaml
	@python templates/transform_tex.py $@
	$(PRINT) "make $@ done."

bibs/mybib.bib: $(BIB_TXT_FILES)
	@python templates/markdown2bib.py --out=bibs/mybib.bib $(BIB_TXT_FILES)
	$(PRINT) "make $@ done."

wordcount/wc.csv: $(MD_FILES) $(OUTPUT).pdf
	@if [ ! -f $@ ]; \
	then \
		printf "%s,%s,%s\n" "Date" "Words" "Pages" >> $@ ; \
	fi
	@printf "%16s, %8i, %5i\n" `date +"%Y-%m-%d-%Hh%M"` `cat $(MD_FILES) | wc | awk '{split($$0,a," "); print a[1]}'` `pdfinfo $(OUTPUT).pdf | grep Pages | tr -d "Pages: "` >> $@
	@cd wordcount/ ; python ../templates/wordcount.py wc.csv ; cd ..
	$(PRINT) "make $@ done."


##-----------------------------------------------------------------------------
## create md with references replaced and bibliography created
$(OUTPUT).mds: $(MD_FILES) bibs/mybib.bib meta.yaml
	@pandoc \
		-t markdown_github \
		--standalone \
		--smart \
		--bibliography=bibs/mybib.bib \
		--filter pandoc-citeproc \
		-o $@.tmp $(MD_FILES) $(OPS_FULLHTML) meta.yaml
	@cat $@.tmp | sed -E 's/\[([0-9][0-9]?[0-9]?)\]/\[\^\1\]/g' | sed -E 's/^\[\^([0-9][0-9]?[0-9]?)\]\ /\[\^\1\]:\ /' > $@
	@rm -f $@.tmp
	$(PRINT) "make $@ done."

%.mds: %.md bibs/mybib.bib meta.yaml
	@pandoc \
		-t markdown_github \
		--standalone \
		--smart \
		--bibliography=bibs/mybib.bib \
		--filter pandoc-citeproc \
		-o $@.tmp $< $(OPS_SECTION) meta.yaml
	@cat $@.tmp | sed -E 's/\[([0-9][0-9]?[0-9]?)\]/\[\^\1\]/g' | sed -E 's/^\[\^([0-9][0-9]?[0-9]?)\]\ /\[\^\1\]:\ /' > $@
	@rm -f $@.tmp
	$(PRINT) "make $@ done."

## create html from mds
%.htmls: %.mds
	@pandoc \
		-t html \
		--ascii \
		--standalone \
		--smart \
		--variable=date-meta:"$(DATE)" \
		--variable=css:templates/markdown-memo.css \
		--template=./templates/outline_template.html \
		-o $@ $< meta.yaml
	$(PRINT) "make $@ done."


##-----------------------------------------------------------------------------
# JUNK = *.aux *.log *.bbl *.blg *.brf *.cb *.ind *.idx *.ilg *.inx *.dvi *.toc *.out *~ ~* spellTmp *.lot *.lof *.ps *.d
JUNK = *.mds *.htmls *.tex *.aux *.dvi *.fdb_latexmk *.fls *.log *.out *.toc *.tmp *-tmp.html index.md
OUTS = *.html *.pdf bibs/*.bib

clean:
	@rm -f $(JUNK)
	$(PRINT) "make $@ done."

realclean: clean
	@rm -f $(OUTS)
	$(PRINT) "make $@ done."

over: realclean default


