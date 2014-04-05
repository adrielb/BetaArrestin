set autochdir

nnoremap <buffer> <leader>r :wall \| SlimeSend1 %run -i BetaArrestin.py<CR>
nnoremap <leader>m  :make\|redraw!<CR>

let g:slime_default_config = {"socket_name": "default", "target_pane": "1.0"}
"let g:slime_default_config = {"socket_name": "default", "target_pane": "1.1"}
"let g:slime_default_config = {"socket_name": "default", "target_pane": "ipython:1.1"}

"wmctrl -Fa 'Figure 1'
augroup pythonREPL
  autocmd!
  autocmd FileType python nmap <buffer> <CR>         <Plug>SlimeLineSend
  autocmd FileType python nmap <buffer> <leader><CR> <Plug>SlimeParagraphSend
  autocmd FileType python xmap <buffer> <CR>         <Plug>SlimeRegionSend
augroup END
