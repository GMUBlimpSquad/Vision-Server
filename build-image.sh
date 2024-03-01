#!/usr/bin/env sh

docker rmi -f vision-server
docker buildx build -t vision-server .
