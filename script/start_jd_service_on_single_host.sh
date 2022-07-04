#!/bin/bash

SCRIPT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
SERVICE_PATH=$SCRIPT_PATH/../

python $SERVICE_PATH/backend/launch_api_service.py &
python $SERVICE_PATH/backend/launch_serve_tf.py &