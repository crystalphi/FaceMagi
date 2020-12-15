#!/bin/bash

read -r -p "确定要更新数据库结构吗? [y/n] " input

case $input in
    [yY][eE][sS]|[yY])
		echo "Yes"
        
        python3 ./manage.py db migrate -m "initial migrate"
        python3 ./manage.py db upgrade
        
		;;

    [nN][oO]|[nN])
		echo "No"
       		;;

    *)
	echo "Invalid input..."
	exit 1
	;;
esac
