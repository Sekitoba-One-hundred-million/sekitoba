dir='config'
write_file_name="$dir/name.py"
score_file="score_data_name.txt"
rank_score_file="rank_score_data.txt"
prod_dir="/Volumes/Gilgamesh/sekitoba-prod"
space="    "

rm -rf $write_file_name

echo 'import datetime\n' >> $write_file_name
echo 'class Name:' >> $write_file_name
echo '    def __init__( self ):' >> $write_file_name

self=$space$space'self.'
name_list=`cat $dir/$score_file`

for name in $name_list; do
    minus_name=${name}_minus
    echo "$self$name = \"$name\"" >> $write_file_name
    echo "$self$minus_name = \"$minus_name\"" >> $write_file_name
done

rank_name_list=`cat $dir/$rank_score_file`

for name in $rank_name_list; do
    if ! printf '%s\n' "${name_list[@]}" | grep -qx "$name"; then
        echo "$self$name = \"$name\"" >> $write_file_name
    fi
done

echo "${self}stock_name = self.stock_name_create()" >> $write_file_name

echo "" >> $write_file_name
stock_name_create=`cat $dir/stock_name_create`
echo "${stock_name_create}" >> $write_file_name
