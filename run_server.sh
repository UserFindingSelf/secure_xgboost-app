#!/bin/sh

docker start server 2>/dev/null || docker run -u 0 --rm --name server -itdv $PWD/server:/home/secure-xgboost -p 8080:80 -w /home/secure-xgboost/ sec-xgb:server
docker exec -itd server service ssh restart # Starts the ssh for data transfer through scp
docker inspect server | grep '"IPAddress"' | awk 'NR==1{print(substr($2, 2, length($2)-3)":22")}' > server/hosts.config # Saving server IP address
docker exec -it server bash -c "export LANG=C.UTF-8 && streamlit run server_app.py"
docker stop server
# docker attach server
