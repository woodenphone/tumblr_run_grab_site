#!/bin/bash

echo 'Starting gs-server'

# Start grab-site but return terminal to user
# https://superuser.com/questions/178587/how-do-i-detach-a-process-from-terminal-entirely#178592
grab-site </dev/null &>/dev/null &

echo 'Started gs-server'
