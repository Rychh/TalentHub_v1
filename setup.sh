#!/bin/bash

cp talenthub/settings/base.py talenthub/settings/local.py
python3 manage.py makemigrations talenthub
python3 manage.py migrate
echo "import examples" | python3 manage.py shell
