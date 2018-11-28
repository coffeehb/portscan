
#! /bin/bash
source /etc/profile;
# https://www.jianshu.com/p/2d60e6513fdd
# -----------------------------
#
tempfifo=$$.fifo
target_ip=$1
start_port=$2
end_port=$3
number_tasks=100

if [ $# -eq 3 ] 
then
    if [ "$start_port" \> "$end_port" ]
    then
        echo "Error! $start_port is greater than $end_port"
        exit 1;
    fi
else
    echo "Error! Not enough params."
    echo "Sample: sh bash_scanports.sh 23.232.72.205 1 10000"
    exit 2;
fi

trap "exec 1000>&-;exec 1000<&-;exit 0" 2 # Ctrl + C
mkfifo $tempfifo
exec 1000<>$tempfifo
rm -rf $tempfifo

for ((i=1; i<$number_tasks; i++))
do
    echo >&1000
done

while [ $start_port != $end_port ]
do
    read -u1000
    {
        nc -z -w 1 $target_ip $start_port | grep succeeded
        echo >&1000
    } &

    let start_port=start_port+1
done

wait
echo "done!!!!!!!!!!"
