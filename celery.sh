#!/bin/sh

while [ 1 ]
do
	celery -A _ worker -l info
done
