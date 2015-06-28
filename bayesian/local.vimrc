
nmap <leader>m :call CompileStan()<CR>

set makeprg=./error.sh

function! CompileStan()
  write
  SlimeSend1 dso <- stan_model( stanc_ret=stanc(file="./model.stan") )
  make
endfunction
