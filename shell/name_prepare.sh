#!/bin/bash

. ./shell/func.sh

touch ${score_file}
touch ${instance_file}

cat ${rank_score_data} >> ${instance_file}
cat ${race_pace_simulation_score_data} >> ${instance_file}
cat ${train_score_data} >> ${instance_file}
cat ${first_passing_rank_score_data} >> ${instance_file}
cat ${last_passing_rank_score_data} >> ${instance_file}
cat ${up3_score_data} >> ${instance_file}
cat ${recovery_score_data_name} >> ${instance_file}
cat ${rough_race_score_data} >> ${instance_file}

sort ${instance_file} | uniq >> ${score_file}

space="    "

echo 'class DataName:' >> ${data_name_py}
echo '    def __init__( self ):' >> ${data_name_py}

self=$space$space'self.'

for name in `cat ${score_file}`; do
    echo "${self}${name} = \"${name}\"" >> ${data_name_py}
done

for name in `cat ${add_score_file}`; do
    echo "${self}${name} = \"${name}\"" >> ${data_name_py}
done

echo 'class PickleName:' >> ${pickle_name_py}
echo '    def __init__( self ):' >> ${pickle_name_py}

IFS=$'\n'
for data in `cat ${pickle_info}`; do
    pickle_name=`echo ${data} | awk -F '.' '{ print $1 }'`

    if [[ "${pickle_name}" =~ "instance" ]]; then
        continue
    fi
    
    echo "${self}${pickle_name} = \"${pickle_name}.pickle\"" >> ${pickle_name_py}
done

for data in `cat ${add_pickle_data}`; do
    pickle_name=`echo ${data} | awk -F '.' '{ print $1 }'`
    echo "${self}${pickle_name} = \"${pickle_name}.pickle\"" >> ${pickle_name_py}
done

IFS=${OLDIFS}

rm ${instance_file}
