docker network prune -f
docker volume prune -f
docker container prune -f
docker image prune -af
docker system prune -af
docker rmi -f $(docker images -q)

docker-compose down --volumes --rmi all
