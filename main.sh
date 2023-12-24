#!/bin/bash

. ./shell/func.sh

remove_not_need_data
remove_update_data

./shell/data_init.sh
./shell/name_prepare.sh

remove_not_need_data

#python src/main.py
