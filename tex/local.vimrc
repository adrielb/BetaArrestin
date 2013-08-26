"set makeprg=make\ all
"set makeprg=./equsubs.sed\ <\ dmath.tex\ >\ dmath.sed.tex
set nowrap
set autoread
set autowriteall
"set hidden
augroup TexAutoWrite
  autocmd FileType tex :autocmd! TexAutoWrite InsertLeave <buffer> :update
augroup END

set spellfile=en.utf-8.add
set spellsuggest=best,10
set cursorline
"set wrap linebreak nolist
set formatoptions=nt1
set textwidth=78
set relativenumber

