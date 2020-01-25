docker stop smarthub
docker rm smarthub
docker image rm smarthub
docker build -t smarthub .
docker run -d --name smarthub smarthub
docker start smarthub
docker exec -it smarthub sh
