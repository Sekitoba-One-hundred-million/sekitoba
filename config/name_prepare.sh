dir='config'
write_file_name="$dir/name.py"
score_file="score_data_name.txt"
prod_dir="/Volumes/Gilgamesh/sekitoba-prod"
space="    "

cp $prod_dir/$score_file $dir/$score_file
rm -rf $write_file_name

echo 'import datetime\n' >> $write_file_name
echo 'class Name:' >> $write_file_name
echo '    def __init__( self ):' >> $write_file_name

self=$space$space'self.'
name_list=`cat $dir/$score_file`

for name in $name_list; do
    minus_name=${name}_minus
    echo "$self$name = \"$name\"" >> $write_file_name
    #echo "$self$minus_name = \"$file_name\"" >> $write_file_name
done

echo "${self}stock_name = self.stock_name_create()" >> $write_file_name

echo "" >> $write_file_name
stock_name_create=`cat $dir/stock_name_create`
echo "${stock_name_create}" >> $write_file_name