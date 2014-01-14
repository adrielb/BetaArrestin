PYTHON=export DISPLAY=:0.2;python -W ignore::DeprecationWarning

FIGS=StotVsMAPKpp.pdf SmemVsp3.pdf fig-p4func.pdf InputVsMAPKpp.pdf InputVsMI.pdf \
		 ScaffoldVsMAPKppMI.pdf GradientVsMI.pdf rab11dn.pdf p3effects-params.pdf \
		 p3effects.pdf

all: p3effects.pdf p3effects-params.pdf

#${FIGS:pdf=py}: 

allfigs: ${FIGS}

#%.pdf : %.py BetaArrestin.py FigDisplay.py
	#${PYTHON} $<

%.csv : %-sim.py BetaArrestin.py
	${PYTHON} $<
	
%.pdf : %.csv %.py FigDisplay.py
	${PYTHON} ${<:csv=py}

opt:
	${PYTHON} opt.py

clean:
	rm *.pyc

cleanfigs:
	rm ${FIGS}

p3effects.csv: p3effects-params.csv


.PHONY: all allfigs clean cleanfigs
.PRECIOUS: %.csv
