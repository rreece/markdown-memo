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

ifeq ($(DOREFS), true)
HTML_DEPS := bibs/mybib.bib
PDF_DEPS := bibs/mybib.bib
OPS_FULLPDF := templates/refs_tex.md templates/backmatter.md
OPS_FULLHTML := templates/refs.md templates/backmatter.md
OPS_SECTION := templates/refs_subsection.md templates/backmatter.md
else
HTML_DEPS := 
PDF_DEPS := 
OPS_FULLPDF := templates/backmatter.md
OPS_FULLHTML := templates/backmatter.md
OPS_SECTION := templates/backmatter.md
endif


##-----------------------------------------------------------------------------
## helpers
##-----------------------------------------------------------------------------

PRINT = @echo '==>  '

DATE     := $(shell date +"%a %b %d, %Y")
MD_FILES := $(filter-out index.md README.md VERSIONS.md, $(wildcard *.md))
HTML_FILES := $(MD_FILES:%.md=%.html)
PDF_FILES := $(MD_FILES:%.md=%.pdf)
BIB_TXT_FILES := $(wildcard bibs/*.txt)
#MD_FILES_WITH_REFS := 
MD_FILES_ORDERED = $(shell cat order.txt | tr '\n' ' ')


## MD_FILES   =  chap1.md   chap2.md   ...
## HTML_FILES =  chap1.html chap2.html ...
## PDF_FILES  =  chap1.pdf  chap2.pdf  ...


##-----------------------------------------------------------------------------
## targets
##-----------------------------------------------------------------------------

default: html

all: html pdf

html: $(HTML_FILES) index.html
	$(PRINT) "html done."

ohtml: $(OUTPUT).html
	$(PRINT) "ohtml (document as one html file: $(OUTPUT).html) done."

pdf: $(OUTPUT).pdf wordcount

wordcount: wordcount/words.png

index.md: $(MD_FILES)
	@if [ -f index.txt ]; \
	then \
		cp index.txt $@ ; \
	else \
		python scripts/make_index_md.py -c --out=$@ $(MD_FILES) ; \
	fi
	$(PRINT) "make $@ done."

index.html: index.md meta.yaml
	@pandoc \
		-t html \
		--ascii \
		--standalone \
		--smart \
		--variable=date-meta:"$(DATE)" \
		--template=./templates/index_template.html \
		-o $@ $< meta.yaml
	$(PRINT) "make $@ done."

$(OUTPUT).html: order.txt $(MD_FILES) $(HTML_DEPS) meta.yaml
	@pandoc \
		-t html \
		--ascii \
		--number-sections \
		--standalone \
		--smart \
		--variable=date-meta:"$(DATE)" \
		--template=./templates/index_template.html \
		--mathjax \
		--bibliography=bibs/mybib.bib \
		--filter pandoc-crossref \
		--filter pandoc-citeproc \
		-o $@ $(MD_FILES_ORDERED) $(OPS_FULLHTML) meta.yaml
	@python scripts/transform_html.py $@
	$(PRINT) "make $@ done."

## create html
%.html: %.md order.txt $(HTML_DEPS) meta.yaml
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
	@if [ "$(DOREFS)" = "true" ] && grep --quiet REFERENCES $< ; \
	then \
		pandoc \
			-t html \
			--ascii \
			--standalone \
			--smart \
			--variable=date-meta:"$(DATE)" \
			--template=./templates/outline_template.html \
			--mathjax \
			--bibliography=bibs/mybib.bib \
			--filter pandoc-crossref \
			--filter pandoc-citeproc \
			-o $@ $< $(OPS_SECTION) meta.yaml.tmp ; \
	else \
		pandoc \
			-t html \
			--ascii \
			--standalone \
			--smart \
			--variable=date-meta:"$(DATE)" \
			--template=./templates/outline_template.html \
			--mathjax \
			--filter pandoc-crossref \
			-o $@ $< templates/backmatter.md meta.yaml.tmp ; \
	fi
	@rm -f meta.yaml.tmp $@.tmp
	@python scripts/transform_html.py $@
	$(PRINT) "make $@ done."

## create the full pdf 
#$(OUTPUT).pdf: $(MD_FILES) $(PDF_DEPS) meta.yaml
#	@pandoc \
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

## create the full pdf via pandoc to tex then pdflatex
$(OUTPUT).pdf: $(OUTPUT).tex
	@pdflatex -interaction=nonstopmode $< &> latex.log
	@pdflatex -interaction=nonstopmode $< &> latex.log
	$(PRINT) "make $@ done."

## create the pdf for a section
#%.pdf: %.md $(PDF_DEPS) meta.yaml
#	@pandoc \
#		--standalone \
#		--smart \
#		--variable=date-meta:"$(DATE)" \
#		--template=templates/default_template.tex \
#		--filter pandoc-crossref \
#		--filter pandoc-eqnos \
#		--bibliography=bibs/mybib.bib \
#		--filter pandoc-citeproc \
#		-o $@ $< $(OPS_SECTION) meta.yaml
#	$(PRINT) "make $@ done."

## create tex with references replaced and bibliography created
$(OUTPUT).tex: order.txt $(MD_FILES) $(PDF_DEPS) meta.yaml
	@if [ "$(DOREFS)" = "true" ] ; \
	then \
		pandoc \
			-t latex \
			--ascii \
			--standalone \
			--smart \
			--template=templates/default_template.tex \
			--filter pandoc-crossref \
			--bibliography=bibs/mybib.bib \
			--filter pandoc-citeproc \
			-o $@ $(MD_FILES_ORDERED) $(OPS_FULLPDF) meta.yaml ; \
	else \
		pandoc \
			-t latex \
			--ascii \
			--standalone \
			--smart \
			--template=templates/default_template.tex \
			--filter pandoc-crossref \
			-o $@ $(MD_FILES_ORDERED) $(OPS_FULLPDF) meta.yaml ; \
	fi
	@python scripts/transform_tex.py $@
	$(PRINT) "make $@ done."

## create the tex for a section
#%.tex: %.md $(PDF_DEPS) meta.yaml
#	@pandoc \
#		-t latex \
#		--ascii \
#		--standalone \
#		--smart \
#		--template=templates/default_template.tex \
#		--filter pandoc-crossref \
#		--bibliography=bibs/mybib.bib \
#		--filter pandoc-citeproc \
#		-o $@ $< $(OPS_SECTION) meta.yaml
#	@python scripts/transform_tex.py $@
#	$(PRINT) "make $@ done."

bibs/mybib.bib: $(BIB_TXT_FILES)
	@if [[ -z "$(BIB_TXT_FILES)" ]] ; \
	then \
		echo "==>   ERROR: No bibliography files found in bibs/. Set dorefs=false in meta.yaml." ; \
		exit 1 ; \
	else \
		python scripts/markdown2bib.py --out=bibs/mybib.bib $(BIB_TXT_FILES) ; \
	fi
	$(PRINT) "make $@ done."

bib_index.md: bibs/mybib.bib
	@python scripts/make_bib_index_md.py --out=$@ $<
	$(PRINT) "make $@ done."

order.txt:
	@ls -1 $(MD_FILES) > $@
	$(PRINT) "make $@ done."

wordcount/wc.csv: $(MD_FILES) $(OUTPUT).pdf
	@if [ ! -d wordcount ]; \
	then \
		mkdir wordcount ; \
	fi
	@if [ ! -f $@ ]; \
	then \
		printf "%s,%s,%s\n" "Date" "Words" "Pages" >> $@ ; \
	fi
	@printf "%16s, %8i, %5i\n" `date +"%Y-%m-%d-%Hh%M"` `cat $(MD_FILES) | wc | awk '{split($$0,a," "); print a[2]}'` `pdfinfo $(OUTPUT).pdf | grep Pages | tr -d "Pages: "` >> $@
	$(PRINT) "make $@ done."

wordcount/words.png: wordcount/wc.csv
	@echo ''
	@cd wordcount/ ; python ../scripts/wordcount.py wc.csv ; cd ..


##-----------------------------------------------------------------------------
## create md with references replaced and bibliography created
#$(OUTPUT).mds: $(MD_FILES) $(HTML_DEPS) meta.yaml
#	@pandoc \
#		-t markdown_github \
#		--standalone \
#		--smart \
#		--bibliography=bibs/mybib.bib \
#		--filter pandoc-citeproc \
#		-o $@.tmp $(MD_FILES) $(OPS_FULLHTML) meta.yaml
#	@cat $@.tmp | sed -E 's/\[([0-9][0-9]?[0-9]?)\]/\[\^\1\]/g' | sed -E 's/^\[\^([0-9][0-9]?[0-9]?)\]\ /\[\^\1\]:\ /' > $@
#	@rm -f $@.tmp
#	$(PRINT) "make $@ done."
#
#%.mds: %.md $(HTML_DEPS) meta.yaml
#	@pandoc \
#		-t markdown_github \
#		--standalone \
#		--smart \
#		--bibliography=bibs/mybib.bib \
#		--filter pandoc-citeproc \
#		-o $@.tmp $< $(OPS_SECTION) meta.yaml
#	@cat $@.tmp | sed -E 's/\[([0-9][0-9]?[0-9]?)\]/\[\^\1\]/g' | sed -E 's/^\[\^([0-9][0-9]?[0-9]?)\]\ /\[\^\1\]:\ /' > $@
#	@rm -f $@.tmp
#	$(PRINT) "make $@ done."
#
### create html from mds
#%.htmls: %.mds
#	@pandoc \
#		-t html \
#		--ascii \
#		--standalone \
#		--smart \
#		--variable=date-meta:"$(DATE)" \
#		--template=./templates/outline_template.html \
#		-o $@ $< meta.yaml
#	$(PRINT) "make $@ done."


##-----------------------------------------------------------------------------
# JUNK = *.aux *.log *.bbl *.blg *.brf *.cb *.ind *.idx *.ilg *.inx *.dvi *.toc *.out *~ ~* spellTmp *.lot *.lof *.ps *.d
JUNK = *.mds *.htmls *.tex *.aux *.dvi *.fdb_latexmk *.fls *.log *.out *.toc *.tmp *-tmp.html index.md bib_index.md
OUTS = *.html *.pdf bibs/*.bib

clean:
	@rm -f $(JUNK)
	$(PRINT) "make $@ done."

realclean: clean
	@rm -f $(OUTS)
	$(PRINT) "make $@ done."

over: realclean default

destroy: realclean
	@rm -f *.md *.html *.txt
	$(PRINT) "make $@ done."


