#!/bin/bash

echo "+-------------------------------+"
echo "| Waiting for MySQL to start... |"
echo "+-------------------------------+"
./wait-for-it.sh db:3306

echo "+-----------------------+"
echo "| Migrating database... |"
echo "+-----------------------+"
python manage.py migrate

echo "+--------------------+"
echo "| Starting server... |"
echo "+--------------------+"
python manage.py runserver 0.0.0.0:8000
