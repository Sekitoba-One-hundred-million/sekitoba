#!/bin/bash

ATHENA_HOST='Athena'
predictServerName='predict-server'
proxyServerName='proxy-server'

function startPredictServer {
  echo "start PredictServer"
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
  echo "start SekitobaProxy"
  ssh -t "${ATHENA_HOST}" << EOC
  source ~/.zshrc
  cd /home/athena/ghq/github.com/Sekitoba-One-hundred-million/proxy-manage
  go build
  tmux new-session -d -s "${proxyServerName}" './sekitoba-proxy-manage'
EOC
}

function stopServer {
  echo "stop SekitobaProxy"
  ssh -t "${ATHENA_HOST}" << EOC
  source ~/.zshrc
  pgrep sekitoba-proxy | xargs kill
  sleep 20
EOC
  echo "Stop Server"
}

function checkProxy {
  sleep 10
  domain_file="/Volumes/Gilgamesh/proxy/domain"
  while true; do
    if [ -f "${domain_file}" ]; then
      domain=`cat "${domain_file}"`
      status="$(curl -m 3 http://${domain}/ -H 'Host: race.netkeiba.com' -o /dev/null -w '%{http_code}\n' -s)"

      if [ "${status}" == '200' ]; then
        break
      fi
    fi

    sleep 10
  done
}
#startPredictServer
startSekitobaProxy

trap stopServer 2

#sleep 300
checkProxy

python test/main.py

stopServer
