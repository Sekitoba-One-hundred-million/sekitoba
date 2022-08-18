commit_id="fb1059ddde52e41d73f8bc5a3ad2e6250e69e4b6"
volume="/Volumes/Gilgamesh"

git clone git@github.com:Sekitoba-One-hundred-million/recovery_analyze.git
cd recovery_analyze
git checkout $commit_id

echo
echo copy score_data_name.txt
cp score_data_name.txt ../config/

score_func="score_func.py"

# score_funcの用意 sekitobaに合う様に作り替える
echo copy $score_func
cp users_score/score.py ../

cd ..
touch $score_func
count=0
line_number=13

echo 'from config import name as data_name\n' >> $score_func
while IFS='' read -r score_file; do
    count=$((count+1))
    if [ $count -ge $line_number ]; then
        echo "$score_file" >> $score_func
    fi
done < score.py

mv $score_func predict_and_buy/$score_func
rm score.py
rm -rf recovery_analyze

# users_score_rate.pickleを対象のcommitから取ってくる
users_rate="users_score_rate.pickle"
echo copy ${users_rate}.${commit_id}
cp ${volume}/sekitoba-data/${users_rate}.${commit_id} ${volume}/sekitoba-prod/${users_rate}
