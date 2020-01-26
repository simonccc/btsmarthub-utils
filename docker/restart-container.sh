docker-compose stop smarthub
docker-compose rm smarthub
docker-compose up -d smarthub
docker-compose start smarthub
docker logs smarthub -f
