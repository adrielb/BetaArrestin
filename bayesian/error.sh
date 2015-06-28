
tmux capture-pane -p|awk '/^ERROR/{print "model.stan:"$4": "}'|tac
