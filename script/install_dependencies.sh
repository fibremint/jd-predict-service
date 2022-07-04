#!/bin/bash

# ref: https://stackoverflow.com/questions/59895/how-can-i-get-the-source-directory-of-a-bash-script-from-within-the-script-itsel
SCRIPT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
SERVICE_PATH=$SCRIPT_PATH/../

pip install $SERVICE_PATH/jd
pip install -r $SERVICE_PATH/backend/requirements.txt
