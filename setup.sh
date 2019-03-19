#!/bin/bash

python3 manage.py makemigrations talenthub
python3 manage.py migrate
echo "import examples" | python3 manage.py shell
