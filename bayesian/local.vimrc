let b:slime_config = {"socket_name": "default", "target_pane": ":"}

nmap <leader>m :call CompileStan()<CR>

set makeprg=./error.sh

function! CompileStan()
  write
  call system( "tmux send-keys C-l")
  SlimeSend1 stanc(file="./gp-simple.stan")
  silent make
endfunction
