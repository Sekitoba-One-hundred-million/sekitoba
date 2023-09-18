#!/bin/bash

. ./shell/func.sh

git_clone ${version_manage} ${version}
IFS=$'\n'

# 必要なpickleデータをprodに移す
for data_info in `cat ${pickle_info}`; do
    IFS=${OLDIFS}
    array_data=( ${data_info} )
    data=${array_data[0]}
    file_name=${array_data[1]}
    data_path=''

    if [[ ${file_name} == 'None' ]]; then
        data_path="${sekitoba_data}/${version}/${data}"

        if [ ! -e ${data_path} ]; then
            data_path="${sekitoba_data}/${data}"
        fi
    else
        data_path="${sekitoba_data}/${data}"
    fi

    prod_data_hash=''
    prod_data_path="${sekitoba_prod}/${data}"

    if [ -e ${prod_data_path} ]; then
        prod_data_hash=`md5sum ${prod_data_path} | awk -F ' ' '{ print $1 }'`
    fi

    data_hash=`md5sum ${data_path} | awk -F ' ' '{ print $1 }'`

    if [ -z ${prod_data_hash} ]  || [ ${data_hash} != ${prod_data_hash} ]; then
        cp ${data_path} ${prod_data_path}
    fi
done

for pickle in `cat ${add_pickle_data}`; do
    prod_data_hash=''
    prod_data_path="${sekitoba_prod}/${pickle}"

    if [ -e ${prod_data_path} ]; then
        prod_data_hash=`md5sum ${prod_data_path} | awk -F ' ' '{ print $1 }'`
    fi

    data_path="${sekitoba_data}/${pickle}"
    data_hash=`md5sum ${data_path} | awk -F ' ' '{ print $1 }'`

    if [ -z ${prod_data_hash} ]  || [ ${data_hash} != ${prod_data_hash} ]; then
        cp ${data_path} ${prod_data_path}
    fi
done

#バージョンに合わせたcommit-idを取得
recovery_commit=`commit_get ${recovery_analyze}`
rank_commit=`commit_get ${rank_learn}`
race_pace_simulation_commit=`commit_get ${race_pace_simulation}`
train_score_commit=`commit_get ${train_score}`
first_passing_rank_commit=`commit_get ${first_passing_rank}`
last_passing_rank_commit=`commit_get ${last_passing_rank}`
up3_commit=`commit_get ${up3}`

#必要なデータ取得のためにレポジトリをクローン
git_clone ${recovery_analyze} ${recovery_commit}
git_clone ${rank_learn} ${rank_commit}
git_clone ${race_pace_simulation} ${race_pace_simulation_commit}
git_clone ${train_score} ${train_score_commit}
git_clone ${first_passing_rank} ${first_passing_rank_commit}
git_clone ${last_passing_rank} ${last_passing_rank_commit}
git_clone ${up3} ${up3_commit}

# 必要なデータをコピー
cp ${sekitoba_home}/${recovery_analyze}/plus_score.json ${plus_score_json}
cp ${sekitoba_home}/${recovery_analyze}/minus_score.json ${minus_score_json}
cp ${sekitoba_home}/${recovery_analyze}/score_data_name.txt ${recovery_score_data_name}
cp ${sekitoba_home}/${rank_learn}/${score_data} ${rank_score_data}
cp ${sekitoba_home}/${race_pace_simulation}/${score_data} ${race_pace_simulation_score_data}
cp ${sekitoba_home}/${train_score}/${score_data} ${train_score_data}
cp ${sekitoba_home}/${first_passing_rank}/${score_data} ${first_passing_rank_score_data}
cp ${sekitoba_home}/${last_passing_rank}/${score_data} ${last_passing_rank_score_data}
cp ${sekitoba_home}/${up3}/${score_data} ${up3_score_data}
