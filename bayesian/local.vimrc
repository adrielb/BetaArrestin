
nmap <leader>m :call CompileStan()<CR>

set makeprg=./error.sh

function! CompileStan()
  write
  call system( "tmux send-keys C-l")
  SlimeSend1 stanc(file="./steady-state-model.stan")
  silent make
endfunction
