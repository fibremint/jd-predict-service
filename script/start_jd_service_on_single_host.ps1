$RootPath = Split-Path $PSScriptRoot

Start-Process -NoNewWindow python $RootPath/backend/launch_api_service.py
Start-Process -NoNewWindow python $RootPath/backend/launch_serve_tf.py