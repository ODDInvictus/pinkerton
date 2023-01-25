#! /bin/bash

pipenv shell
uwsgi --ini /apps/ibs/uwsgi.ini 