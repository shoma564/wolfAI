#!/bin/bash
rm -r mysql/*

docker-compose down
docker-compose down --rmi all --volumes --remove-orphans

rm -r mysql/*


docker build ./flask -t shomaigu/pro-flask-slack:latest
#docker push shomaigu/pro-flask-slack:latest

#docker build ./db -t shomaigu/pro-mysql:latest
#docker push shomaigu/pro-mysql:latest


docker-compose up
