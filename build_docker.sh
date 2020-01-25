docker stop smarthub
docker rm smarthub
docker image rm smarthub
docker build -t smarthub .
docker-compose up -d smarthub
docker-compose start smarthub
docker tail -f smarthub
