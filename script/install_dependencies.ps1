# ref: https://stackoverflow.com/questions/9725521/how-to-get-the-parents-parent-directory-in-powershell
# $RootPath = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$RootPath = Split-Path $PSScriptRoot

pip install $RootPath/jd
pip install -r $RootPath/backend/requirements.txt