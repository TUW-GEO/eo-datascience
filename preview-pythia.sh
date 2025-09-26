#! /bin/bash

mkdir ./${1}
pythia_convert --out ./${1}

./copy-pythia.sh ./${1}
./download-pythia.sh ./${1}

ENV_PATH=./${1}/notebooks/courses/environmental-remote-sensing/unit_01/.env

if [ ! -e "$ENV_PATH" ]; then
    echo "File not found: $ENV_PATH"
    echo "Executing command: $*"
    touch $ENV_PATH
    echo USER_HSAF = $USER_HSAF >> $ENV_PATH
    echo PASS_HSAF = $PASS_HSAF >> $ENV_PATH
    echo USER_WEKEO = $USER_WEKEO>> $ENV_PATH
    echo PASS_WEKEO = $PASS_WEKEO >> $ENV_PATH
else
    echo "File already exists: $ENV_PATH"
    echo "Command skipped"
    exit 0
fi
