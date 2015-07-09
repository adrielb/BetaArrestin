sleep 0.333

tmux capture-pane -p|awk '
/^Error in stanc/ {sub("^[^\"]*\"",""); 
                   sub("\".*$","");
                   f=$0}
/MESSAGE/         {getline m};
/^ERROR/          {print f":"$4": "m}
'|tac
