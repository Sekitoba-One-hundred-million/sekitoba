#!/bin/bash

source ./shell/func.sh

function checkProxy {
  sleep 10
  domain_file="/Volumes/Gilgamesh/proxy/domain"
  while true; do
    if [ -f "${domain_file}" ]; then
      domain=`cat "${domain_file}"`
      status="$(curl -m 3 http://${domain}/ -H 'Host: race.netkeiba.com' -o /dev/null -w '%{http_code}\n' -s)"
      echo $status $domain
      if [ "${status}" == '200' ]; then
        break
      fi
    fi

    sleep 10
  done
}

startSekitobaProxy
#sleep 300
checkProxy

echo "start remove_not_need_data"
remove_not_need_data

echo "start remove_update_data"
remove_update_data

echo "start data_init.sh"
./shell/data_init.sh

echo "start name_prepare.sh"
./shell/name_prepare.sh

echo "start remove_not_need_data"
remove_not_need_data

python src/main.py

stopServer
