cd ./inspec

# users scoreを作成するためのファイルがあるか確認する
./score_check.sh

if [ $? -eq 1 ]; then
    echo error users score!
    exit 1
fi
