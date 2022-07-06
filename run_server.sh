#!/bin/sh

docker start server 2>/dev/null || docker run -u 0 --rm --name server -itdv $PWD/server:/home/secure-xgboost -p 5000:5000 -w /home/secure-xgboost/ sec-xgb:server
docker exec -itd server service ssh restart # Starts the ssh for data transfer through scp
# docker attach server
docker inspect server | grep '"IPAddress"' | awk 'NR==1{print(substr($2, 2, length($2)-3)":22")}' > server/hosts.config # Saving server IP address
cp server/hosts.config client1/config/hosts.config
cp server/hosts.config client2/config/hosts.config
docker exec -it server bash -c "python3 start_server.py"
docker stop server
