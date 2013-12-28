FIGS=StotVsMAPKpp.pdf SmemVsp3.pdf fig-p4func.pdf InputVsMAPKpp.pdf InputVsMI.pdf \
		 ScaffoldVsMAPKppMI.pdf GradientVsMI.pdf rab11dn.pdf

all: allfigs

#${FIGS:pdf=py}: 

allfigs: ${FIGS}

%.pdf : %.py BetaArrestin.py
	${PYTHON} $<

opt:
	${PYTHON} opt.py

clean:
	rm *.pyc

cleanfigs:
	rm ${FIGS}

PYTHON=python -W ignore::DeprecationWarning

.PHONY: all allfigs
