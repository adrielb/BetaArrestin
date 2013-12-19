nnoremap <buffer> <leader>r :wall \| SlimeSend1 %run -i BetaArrestin.py<CR>

let g:slime_default_config = {"socket_name": "default", "target_pane": "2.0"}
"let g:slime_default_config = {"socket_name": "default", "target_pane": "1.1"}
"let g:slime_default_config = {"socket_name": "default", "target_pane": "ipython:1.1"}

"wmctrl -Fa 'Figure 1'
