#!/bin/sed -f
#s/\\text{\([[:alnum:]]*\)}/\1/g
s/\\text{\([adkpfnC][[:digit:]]\)}/\1/g
s/\\text{S\(cyto\|mem\|ves\)}/S_{\\text{\1}}/g
s/\([adkpC]\)\([[:digit:]]\)/\1_\2/g
s/\\text{\(on\|of\)\([[:digit:]]\)}/\\text{\1}_\2/g
s/\[\([01]\)\]\[t\]/\(\1,t)/g
s/(\([01]\))'(t)/'(\1,t)/g
s/(\([01]\))(t)/(\1,t)/g

