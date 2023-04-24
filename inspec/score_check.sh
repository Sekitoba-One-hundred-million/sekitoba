#!/bin/bash

ok=0

for name in `cat ../config/score_data_name.txt`; do
    check=0
    for file in `ls ../data_analyze/data_create/`; do
        check_name=${file%.*}
        
        if [ $name == $check_name ]; then
            check=1
            break
        fi
    done

    if [ $check -eq 0 ]; then
        ok=1
        echo not found $name
    fi
done

for name in `cat ../config/rank_score_data.txt`; do
    check=0
    for file in `ls ../data_analyze/data_create/`; do
        check_name=${file%.*}
        if [ $name == $check_name ]; then
            check=1
            break
        fi
    done

    if [ $check -eq 0 ]; then
        ok=1
        echo not found $name
    fi
done

for file in `ls ../data_analyze/data_create/`; do
    check=1
    check_name=${file%.*}
    
    log=`cat ../config/score_data_name.txt | grep "$check_name"`
    users_check=$?

    log=`cat ../config/rank_score_data.txt | grep "$check_name"`
    rank_check=$?

    if [ $rank_check -eq 0 ] || [ $users_check -eq 0 ]; then
        check=0
    fi
    
    if [ $check_name == "__init__" ]; then
        check=0
    fi

    if [ $check_name == "__pycache__" ]; then
        check=0
    fi

    if [ $check -eq 1 ]; then
        echo not need $file
    fi
done

exit $ok
