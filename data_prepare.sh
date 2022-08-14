file_name='./config/use_data.txt'
prod_dir='/Volumes/Gilgamesh/sekitoba-prod/'
local_dir='./storage/'

while read line
do
    ARR=(${line// / })
    name=${ARR[0]}
    version=${ARR[1]}
    next_name=$prod_dir$name'.'$version
    echo $name $version
    cp $next_name $local_dir$name
done < $file_name
