# users scoreを作成するためのファイルがあるか確認する
sh users_score_check.sh

if [ $? -eq 1 ]; then
    echo error users score!
    exit 1
fi
