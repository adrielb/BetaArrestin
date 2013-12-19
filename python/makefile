all: fig-p4func.pdf

run:
	python BetaArrestin.py

opt:
	${PYTHON} opt.py

${FIGS}: BetaArrestin.py

allfigs: ${FIGS}

FIGS=StotVsMAPKpp.pdf SmemVsp3.pdf fig-p4func.pdf InputVsMAPKpp.pdf InputVsMI.pdf \
		 ScaffoldVsMAPKppMI.pdf GradientVsMI.pdf rab11dn.pdf

.SUFFIXES: .pdf .py
.py.pdf:
	${PYTHON} $<

	
clean:
	rm *.pyc

cleanfigs:
	rm ${FIGS}

PYTHON=python -W ignore::DeprecationWarning
