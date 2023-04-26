#!/bin/bash -x

recovery_commit_id="564e1335d01f1fb1343e5073032425fec4e37131"
rank_commit_id="d59f500987c121c30675f11d388ff097aa1402e3"
score_func="predict_and_buy/score_func.py"
volume="/Volumes/Gilgamesh"

git clone -q git@github.com:Sekitoba-One-hundred-million/recovery_analyze.git > /dev/null

if [ ! $? -eq 0 ]; then
    echo fail git clone recovery_analyze
    exit 1
fi

cd recovery_analyze
git checkout -q $recovery_commit_id > /dev/null

if [ ! $? -eq 0 ]; then
    echo fail git checkout recovery_analyze
    echo commitid $recovery_commit_id
    echo $git_log
    exit 1
fi

cp score_data_name.txt ../config/score_data_name.txt

rm ../$score_func
touch ../$score_func
echo 'from config import name as data_name\n' >> ../$score_func
sed '1,3d' users_score/score.py >> ../$score_func

cd ..
rm -rf recovery_analyze

git clone -q git@github.com:Sekitoba-One-hundred-million/rank_learn.git

if [ ! $? -eq 0 ]; then
    echo fail git clone rank_learn
    exit 1
fi

cd rank_learn
git checkout -q $rank_commit_id

if [ ! $? -eq 0 ]; then
    echo fail git checkout rank_learn
    echo commitid $rank_commit_id
    echo $git_log
    exit 1
fi

cp common/rank_score_data.txt ../config/rank_score_data.txt

cp $volume/sekitoba-data/rank_model.pickle.$rank_commit_id $volume/sekitoba-prod/rank_model.pickle

cd ..
rm -rf rank_learn

./config/name_prepare.sh
