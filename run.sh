
docker rm vision-server-container
docker run -p 8000:8000 -d -v .:/home/ --name vision-server-container vision-server
