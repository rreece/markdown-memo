# markdown-memo Makefile
#
# author:  Ryan Reece  <ryan.reece@cern.ch>
# created: 2014-07-28
#
###############################################################################

SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c


##-----------------------------------------------------------------------------
## user config
##-----------------------------------------------------------------------------

export TEXINPUTS := .//:./templates//:./tex//:${TEXINPUTS}

doc_title := $(shell grep '^title:' meta.yaml | head -n1 | sed -e 's/title:\s*//' -e 's/^"//' -e 's/"$$//')
page_title = $(shell head -n10 $< | grep -v -e '^$$' | head -n1)
OUTPUT := $(shell grep '^output:' meta.yaml | head -n1 | awk '{ print $$2}')
DOREFS := $(filter $(shell cat meta.yaml | grep ^dorefs | awk '{split($$0,a,":"); print a[2]}' | xargs),true)

ifeq ($(DOREFS), true)
HTML_DEPS := bibs/mybib.bib
PDF_DEPS := bibs/mybib.bib
BACKMATTER_PDF := templates/refs_tex.md templates/backmatter.md
BACKMATTER_FULL_HTML := templates/refs.md templates/backmatter.md
BACKMATTER_HTML := templates/refs_subsection.md templates/backmatter.md
BIBLIO_OPTIONS := --bibliography=bibs/mybib.bib --citeproc
else
HTML_DEPS := 
PDF_DEPS := 
BACKMATTER_PDF := templates/backmatter.md
BACKMATTER_FULL_HTML := templates/backmatter.md
BACKMATTER_HTML := templates/backmatter.md
BIBLIO_OPTIONS :=
endif


##-----------------------------------------------------------------------------
## helpers
##-----------------------------------------------------------------------------

PRINT = @echo '==>  '

DATE := $(shell date +"%a %b %d, %Y")
MD_FILES := $(filter-out index.md README.md VERSIONS.md, $(wildcard *.md))
HTML_FILES := $(MD_FILES:%.md=%.html)
PDF_FILES := $(MD_FILES:%.md=%.pdf)
BIB_TXT_FILES := $(wildcard bibs/*.txt)
#MD_FILES_WITH_REFS := 
MD_FILES_ORDERED = $(shell if [ -f order.txt ]; then cat order.txt | tr '\n' ' '; fi)
MDP_FILES := $(MD_FILES:%.md=%.mdp)
MDP_FILES_ORDERED := $(MD_FILES_ORDERED:%.md=%.mdp)

## MD_FILES   =  chap1.md   chap2.md   ...
## HTML_FILES =  chap1.html chap2.html ...
## PDF_FILES  =  chap1.pdf  chap2.pdf  ...


##-----------------------------------------------------------------------------
## main targets
##-----------------------------------------------------------------------------

.PHONY: all default html ohtml pdf wordcount install install_for_linux install_for_mac check check_pdf clean realclean over cleanwc destroy destroygit destroywc newdoc

default: html # clean

all: html pdf

html: $(HTML_FILES) index.html
	$(PRINT) "html done."

ohtml: $(OUTPUT).html
	$(PRINT) "ohtml (document as one html file: $(OUTPUT).html) done."

pdf: $(OUTPUT).pdf wordcount

wordcount: wordcount/words.png


##-----------------------------------------------------------------------------
## install
## See: https://askubuntu.com/questions/1335772/using-pandoc-crossref-on-ubuntu-20-04
##-----------------------------------------------------------------------------

install: install_for_linux
	$(PRINT) "make $@ done."

install_for_linux:
	@echo "Installing for linux..." ; \
    sudo apt-get -y update ; \
	echo "Installing texlive-latex-extra..." ; \
    sudo apt-get -y install texlive-latex-extra ; \
	echo "Installing pandoc..." ; \
	wget https://github.com/jgm/pandoc/releases/download/2.13/pandoc-2.13-1-amd64.deb ; \
	sudo dpkg -i pandoc-2.13-1-amd64.deb ; \
	pandoc --version ; \
	echo `which pandoc` ; \
	if [ ! -f /usr/local/bin/pandoc-crossref ]; then \
		echo "Installing pandoc-crossref..." ; \
    	wget -c https://github.com/lierdakil/pandoc-crossref/releases/download/v0.3.10.0a/pandoc-crossref-Linux.tar.xz ; \
    	tar -xf pandoc-crossref-Linux.tar.xz ; \
    	sudo mv pandoc-crossref /usr/local/bin/ ; \
    	sudo chmod a+x /usr/local/bin/pandoc-crossref ; \
    	sudo mkdir -p /usr/local/man/man1 ; \
    	sudo mv pandoc-crossref.1  /usr/local/man/man1 ; \
	fi ; \
	echo "Installing other dependencies..." ; \
    sudo apt-get -y install python3-pandas ;
	$(PRINT) "make $@ done."

install_for_mac:
	@echo "Installing for mac..." ; \
	true ;
	$(PRINT) "make $@ done."

check:
	@if [ ! -f index.html ]; then \
		echo "Error: index.html does not exist." ; \
		exit 1 ; \
	fi
	$(PRINT) "make $@ done."

check_pdf:
	@if [ ! -f $(OUTPUT).pdf ]; then \
		echo "Error: $(OUTPUT).pdf does not exist." ; \
		exit 1 ; \
	fi
	$(PRINT) "make $@ done."


##-----------------------------------------------------------------------------
## file targets
##-----------------------------------------------------------------------------

## transform md to mdp (apply hacks with transform_md.py)
%.mdp: %.md
	@python scripts/transform_md.py $<
	$(PRINT) "make $@ done."

## if it exists, copy index.txt to index.md, otherwise make index.md
index.md: $(MD_FILES_ORDERED)
	@if [ -f index.txt ]; \
	then \
		cp index.txt $@ ; \
	else \
		python scripts/make_index_md.py -c --out=$@ $(MD_FILES_ORDERED) ; \
	fi
	$(PRINT) "make $@ done."

## create index.html
index.html: index.mdp meta.yaml
	@pandoc \
		-f markdown+smart \
		-t html \
		--ascii \
		--standalone \
		--variable=date_meta:"$(DATE)" \
		--template=./templates/index_template.html \
		--mathjax \
		-o $@ $< meta.yaml > /dev/null 2>&1
	@python scripts/transform_html.py $@
	$(PRINT) "make $@ done."

## create the output html in one combined file
$(OUTPUT).html: order.txt $(MDP_FILES) $(HTML_DEPS) meta.yaml
	@pandoc \
		-f markdown+smart \
		-t html \
		--ascii \
		--number-sections \
		--standalone \
		--variable=date_meta:"$(DATE)" \
		--template=./templates/index_template.html \
		--mathjax \
		--citeproc \
		--bibliography=bibs/mybib.bib \
		--filter pandoc-crossref \
		-o $@ $(MDP_FILES_ORDERED) $(BACKMATTER_FULL_HTML) meta.yaml > pandoc.log 2>&1
	@python scripts/transform_html.py $@
	$(PRINT) "make $@ done."

## create html
%.html: %.mdp order.txt $(HTML_DEPS) meta.yaml
	@pandoc \
		-f markdown+smart \
		-t html \
		--ascii \
		--standalone \
		--variable=date_meta:"$(DATE)" \
		--variable=page_title:"$(page_title)" \
		--variable=doc_title:"$(doc_title)" \
		--template=./templates/outline_template.html \
		--mathjax \
		--filter pandoc-crossref \
		$(BIBLIO_OPTIONS) \
		-o $@ $< $(BACKMATTER_HTML) meta.yaml > pandoc.log 2>&1
	@python scripts/transform_html.py $@
	$(PRINT) "make $@ done."

## create the pdf from tex
%.pdf: %.tex
	@pdflatex -interaction=nonstopmode $< > latex.log 2>&1
	@pdflatex -interaction=nonstopmode $< > latex.log 2>&1
	@pdflatex -interaction=nonstopmode $< > latex.log 2>&1
	$(PRINT) "make $@ done."

## create tex with references replaced and bibliography created
$(OUTPUT).tex: order.txt $(MDP_FILES) $(PDF_DEPS) meta.yaml
	@pandoc \
		-f markdown+smart \
		-t latex \
		--ascii \
		--standalone \
		--template=templates/default_template.tex \
		--filter pandoc-crossref \
		$(BIBLIO_OPTIONS) \
		-o $@ $(MDP_FILES_ORDERED) $(BACKMATTER_PDF) meta.yaml
	@python scripts/transform_tex.py $@
	$(PRINT) "make $@ done."

## create the tex for a section
%.tex: %.md $(PDF_DEPS) meta.yaml
	@pandoc \
		-f markdown+smart \
		-t latex \
		--ascii \
		--standalone \
		--template=templates/default_template.tex \
		--filter pandoc-crossref \
		$(BIBLIO_OPTIONS) \
		-o $@ $< $(BACKMATTER_HTML) meta.yaml ; \
	@python scripts/transform_tex.py $@
	$(PRINT) "make $@ done."

## create bibs/mybib.bib from bibs/*.txt
bibs/mybib.bib: $(BIB_TXT_FILES)
	@if [ -z "$(BIB_TXT_FILES)" ] ; \
	then \
		echo "==>   ERROR: No bibliography files found in bibs/. Set dorefs=false in meta.yaml." ; \
		exit 1 ; \
	else \
		python scripts/markdown2bib.py --out=bibs/mybib.bib $(BIB_TXT_FILES) ; \
	fi
	$(PRINT) "make $@ done."

## create bib_index from bibs/mybib.bib
bib_index.md: bibs/mybib.bib
	@python scripts/make_bib_index_md.py --out=$@ $<
	$(PRINT) "make $@ done."

## create default order of md files
order.txt:
	@ls -1 $(MD_FILES) > $@
	$(PRINT) "make $@ done."

## update wordcount/wc.csv
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

## create wordcount figures
wordcount/words.png: wordcount/wc.csv
	@echo ''
	@cd wordcount/ ; python ../scripts/wordcount.py wc.csv ; cd ..
	@echo ''


##-----------------------------------------------------------------------------
# JUNK = *.aux *.log *.bbl *.blg *.brf *.cb *.ind *.idx *.ilg *.inx *.dvi *.toc *.out *~ ~* spellTmp *.lot *.lof *.ps *.d
JUNK = *.mdp *.htmls *.tex *.aux *.dvi *.fdb_latexmk *.fls *.log *.out *.toc *.tmp *-tmp.html index.md bib_index.md
OUTS = *.html *.pdf bibs/*.bib

## clean up (do this)
clean:
	@rm -f $(JUNK)
	$(PRINT) "make $@ done."

## clean up everything including the output
realclean: clean
	@rm -f $(OUTS)
	$(PRINT) "make $@ done."

## make realclean and make default again
over: realclean default

## cleanwc (clean wordcount)
cleanwc:
	@rm -rf wordcount
	@git checkout -- wordcount
	$(PRINT) "make $@ done."


##-----------------------------------------------------------------------------
## Be careful using these destructive targets

destroy: realclean
	@rm -f *.md *.html *.txt
	$(PRINT) "make $@ done."

destroygit: 
	@rm -rf .git
	@rm -rf */.git
	$(PRINT) "make $@ done."

destroywc: 
	@rm -f wordcount/wc.csv
	$(PRINT) "make $@ done."

newdoc: destroy destroygit destroywc
	@echo "Introduction" > 01-introduction.md 
	@echo "===============================================================================" >> 01-introduction.md 
	@echo "" >> 01-introduction.md 
	@echo "First subsection" >> 01-introduction.md 
	@echo "-------------------------------------------------------------------------------" >> 01-introduction.md 
	@echo "" >> 01-introduction.md 
	@echo "Start writing..." >> 01-introduction.md 
	@echo "" >> 01-introduction.md 
	@echo "" >> 01-introduction.md 
	@echo "Conclusion" >> 01-introduction.md 
	@echo "===============================================================================" >> 01-introduction.md 
	@echo "" >> 01-introduction.md 
	@echo "Ain't it something?" >> 01-introduction.md 
	@echo "" >> 01-introduction.md 
	@echo "" >> 01-introduction.md 
	@echo "Acknowledgements {.unnumbered}" >> 01-introduction.md 
	@echo "===============================================================================" >> 01-introduction.md 
	@echo "" >> 01-introduction.md 
	@echo "Thanks to everyone who helped with this manuscript." >> 01-introduction.md 
	@echo "" >> 01-introduction.md 
	@echo "" >> 01-introduction.md 
	$(PRINT) "make $@ done."

