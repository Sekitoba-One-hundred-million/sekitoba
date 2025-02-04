#!/bin/bash

source ./shell/func.sh

startSekitobaProxy
sleep 300
#echo "start remove_not_need_data"
#remove_not_need_data

#echo "start remove_update_data"
#remove_update_data

#echo "start data_init.sh"
#./shell/data_init.sh

#echo "start name_prepare.sh"
#./shell/name_prepare.sh

#echo "start remove_not_need_data"
#remove_not_need_data

python src/main.py

#stopServer
