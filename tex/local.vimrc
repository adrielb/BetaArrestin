"set makeprg=make\ all
"set makeprg=./equsubs.sed\ <\ dmath.tex\ >\ dmath.sed.tex
"let g:LatexBox_custom_indent=0
let b:main_tex_file="barrestin.tex"

set autochdir
set smartindent

augroup TexAutoWrite
  autocmd FileType tex :autocmd! TexAutoWrite InsertLeave <buffer> :update
augroup END

set spellfile=en.utf-8.add
set spellsuggest=best,10

set formatoptions+=t " Auto-wrap text using textwidth
set formatoptions+=c " Auto-wrap comments using textwidth
set formatoptions+=q " Allow formatting of comments with gq
"set formatoptions+=a " Automatic formatting of paragraphs
set formatoptions+=n " When formatting text, recognize numbered lists
set formatoptions+=1 " Don't break a line after a one-letter word
set formatoptions+=j " remove a comment leader when joining lines

"let &l:formatlistpat = '^\s*\\\(end\|item\)\>' 
"set formatoptions= 
"set formatlistpat=


set textwidth=78

let g:LatexBox_latexmk_preview_continuously=1
let g:LatexBox_quickfix=2

set wildignore+=*.nav,*.out,*.snm,*.fdb_latexmk,*.log

imap <buffer> [[     \begin{
imap <buffer> ]]     <Plug>LatexCloseCurEnv
imap <buffer> ((     \eqref{
nmap <buffer> cr     <Plug>LatexChangeEnv
vmap <buffer> <F7>   <Plug>LatexWrapSelection
vmap <buffer> <S-F7> <Plug>LatexEnvWrapSelection



