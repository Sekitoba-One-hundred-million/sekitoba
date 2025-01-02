#!/bin/bash

ATHENA_HOST='Athena'
predictServerName='predict-server'
proxyServerName='proxy-server'

function startPredictServer {
  ssh -t "${ATHENA_HOST}" << EOC
  source ~/.zshrc
  cd /home/athena/ghq/github.com/Sekitoba-One-hundred-million/predict-server
  tmux new-session -d -s "${predictServerName}" 'python main.py'
EOC
}

function stopPredictServer {
  ssh -t "${ATHENA_HOST}" << EOC
  source ~/.zshrc
  pgrep -f "${predictServerName}" | xargs kill
EOC
}

function startSekitobaProxy {
  ssh -t "${ATHENA_HOST}" << EOC
  source ~/.zshrc
  cd /home/athena/ghq/github.com/Sekitoba-One-hundred-million/proxy-manage
  go build
  tmux new-session -d -s "${proxyServerName}" './sekitoba-proxy-manage'
EOC
}

function stopServer {
  ssh -t "${ATHENA_HOST}" << EOC
  source ~/.zshrc
  pgrep sekitoba-proxy | xargs kill
  sleep 20
  pgrep -f "${predictServerName}" | xargs kill
EOC
  echo "Stop Server"
}

startPredictServer
startSekitobaProxy

trap stopServer 2

sleep 1200

stopServer
