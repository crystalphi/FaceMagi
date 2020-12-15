#!/bin/bash

#HOSTNAME="db.facemagi.com"
HOSTNAME="backend_py_mysql_1"
PORT="3306"
USERNAME="root"
PASSWORD="Jdd107_MSL_DCKR"
DBNAME="FaceMagi"

#create_db_sql="drop database ${DBNAME}"
create_db_sql="create database IF NOT EXISTS ${DBNAME}"
mysql -h${HOSTNAME} -P${PORT} -u${USERNAME} -p${PASSWORD} -e "${create_db_sql}"

