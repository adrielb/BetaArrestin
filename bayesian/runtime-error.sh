sleep 0.333

tmux capture-pane -p|awk '
/^Exception thrown at line/ {l=$5;getline m;print "'$1':"l m}
'|tac

# in vim cmd line:
# set makeprg=./runtime-error.sh\ gp-deriv-both.stan
