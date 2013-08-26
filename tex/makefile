all: beamer.pdf

%.pdf: %.tex
	pdflatex -interaction=nonstopmode $<

main: 
	./equsubs.sed < dmath.tex > dmath.sed.tex
	./equsubs.sed < params.tex > params.sed.tex
	pdflatex -interaction=nonstopmode main.tex

view:
	evince beamer.pdf

clean:
	rm -rf *.log *.aux *.nav *.out *.toc *.snm *.fls *.fdb_latexmk


