sleep 0.333

tmux capture-pane -p|awk '
/Exception thrown at line/ {l=$NF;getline m;print "'$1':"l m}
'|tac

