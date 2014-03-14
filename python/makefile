PYTHON=export DISPLAY=:0.2;python -W ignore::DeprecationWarning

FIGS=StotVsMAPKpp.pdf SmemVsp3.pdf fig-p4func.pdf InputVsMAPKpp.pdf InputVsMI.pdf \
		 ScaffoldVsMAPKppMI.pdf GradientVsMI.pdf rab11dn.pdf p3effects-params.pdf \
		 p3effects.pdf noco.pdf MIdensity.pdf

all: tags p4effects.pdf

allfigs: ${FIGS}

%.csv : %-sim.py BetaArrestin.py
	${PYTHON} $<
	
%.pdf : %.csv %.py FigDisplay.py matplotlibrc
	${PYTHON} $*.py

opt:
	${PYTHON} opt.py

clean:
	rm *.pyc

cleanfigs:
	rm ${FIGS}

tags: *.py
	ctags -R

p3effects.csv: p3effects-params.csv

noco.csv: InputVsMAPKpp.csv
rab11dn.csv: InputVsMAPKpp.csv


.PHONY: all allfigs clean cleanfigs tags
.PRECIOUS: %.csv


#%.pdf : %.py BetaArrestin.py FigDisplay.py
	#${PYTHON} $<

#${FIGS:pdf=py}: 

	#${PYTHON} ${<:csv=py}
