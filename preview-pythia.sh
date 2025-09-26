#! /bin/bash

mkdir ./${1}
pythia_convert --out ./${1}

./copy-pythia.sh ./${1}
./download-pythia.sh ./${1}

read -p "User name for HSAF: " USER_HSAF
read -p "Password for HSAF user $USER_HSAF: " PASS_HSAF
read -p "User name for WEkEO: " USER_WEKEO
read -p "Password for WEkEO user $USER_WEKEO: " PASS_WEKEO

ENV_PATH=./${1}/notebooks/courses/environmental-remote-sensing/unit_01/.env
touch $ENV_PATH
echo USER_HSAF = $USER_HSAF >> $ENV_PATH
echo PASS_HSAF = $PASS_HSAF >> $ENV_PATH
echo USER_WEKEO = $USER_WEKEO>> $ENV_PATH
echo PASS_WEKEO = $PASS_WEKEO >> $ENV_PATH
