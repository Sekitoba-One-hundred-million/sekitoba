#!/bin/bash

OLDIFS=$IFS
sekitoba_home=`pwd`
version=`cat ${sekitoba_home}/version`
volume='/Volumes/Gilgamesh'
sekitoba_data="${volume}/sekitoba-data"
sekitoba_prod="${volume}/sekitoba-prod"

config_dir="${sekitoba_home}/src/config"
data_dir="${sekitoba_home}/data"
data_name_py="${config_dir}/data_name.py"
pickle_name_py="${config_dir}/pickle_name.py"
score_file="${data_dir}/score_data_name.txt"
add_score_file="${data_dir}/add_score_data_name.txt"
instance_file="${score_file}.instance"

version_manage='version-manage'
sekitoba_library='sekitoba_library'
recovery_analyze='recovery_analyze'
rank_learn='rank_learn'
race_pace_simulation='race_pace_simulation'
rough_race='rough_race'
train_score='train_score'
first_passing_rank='first_passing_rank'
last_passing_rank='last_passing_rank'
up3='up3'

pickle_info="${sekitoba_home}/${version_manage}/data/pickle_info.txt"
add_pickle_data="${sekitoba_home}/data/add_pickle_data.txt"
score_data='common/rank_score_data.txt'
rank_score_data="${sekitoba_prod}/rank_score_data.txt"
race_pace_simulation_score_data="${sekitoba_prod}/race_pace_simulation_score_data.txt"
rough_race_score_data="${sekitoba_prod}/rough_race_score_data.txt"
train_score_data="${sekitoba_prod}/train_score_score_data.txt"
first_passing_rank_score_data="${sekitoba_prod}/first_passing_rank_score_data.txt"
last_passing_rank_score_data="${sekitoba_prod}/last_passing_rank_score_data.txt"
up3_score_data="${sekitoba_prod}/up3_score_data.txt"
plus_score_json="${sekitoba_prod}/plus_score.json"
minus_score_json="${sekitoba_prod}/minus_score.json"
use_score_json="${sekitoba_prod}/use_score_data.json"
recovery_score_data_name="${sekitoba_prod}/recovery_score_data_name.txt"

git_commit="${sekitoba_home}/${version_manage}/data/git-commit.txt"
version_manage_git="ssh://git@github.com/Sekitoba-One-hundred-million/${version_manage}.git"
recovery_analyze_git="ssh://git@github.com/Sekitoba-One-hundred-million/${recovery_analyze}.git"

function git_clone {
    repogitory=$1
    commit=$2
    git_url="ssh://git@github.com/Sekitoba-One-hundred-million/${repogitory}.git"
    git clone -q ${git_url}
    cd ${repogitory}; git checkout -q ${commit}; cd ..
}

function commit_get {
    repogitory=$1
    cat ${git_commit}| grep ${repogitory} | awk -F ' ' '{ print $2 }'
}

function remove_not_need_data {
    if [ -d ${version_manage} ]; then
        rm -rf ${version_manage}
    fi

    if [ -d ${recovery_analyze} ]; then
        rm -rf ${recovery_analyze}
    fi

    if [ -d ${rank_learn} ]; then
        rm -rf ${rank_learn}
    fi

    if [ -d ${race_pace_simulation} ]; then
        rm -rf ${race_pace_simulation}
    fi

    if [ -d ${train_score} ]; then
        rm -rf ${train_score}
    fi
    
    if [ -d ${first_passing_rank} ]; then
        rm -rf ${first_passing_rank}
    fi
    
    if [ -d ${last_passing_rank} ]; then
        rm -rf ${last_passing_rank}
    fi
    
    if [ -d ${up3} ]; then
        rm -rf ${up3}
    fi

    if [ -d ${rough_race} ]; then
        rm -rf ${rough_race}
    fi

    if [ -e ${instance_file} ]; then
        rm ${instance_file}
    fi
}

function remove_update_data {
    if [ -e ${score_file} ]; then
        rm ${score_file}
    fi

    if [ -e ${data_name_py} ]; then
        rm ${data_name_py}
    fi

    if [ -e ${pickle_name_py} ]; then
        rm ${pickle_name_py}
    fi
}
