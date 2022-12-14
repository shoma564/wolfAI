#!/bin/bash
rm -r mysql/*

docker-compose down
docker-compose down --rmi all --volumes --remove-orphans

rm -r mysql/*

docker-compose up
