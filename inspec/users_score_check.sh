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

exit $ok
