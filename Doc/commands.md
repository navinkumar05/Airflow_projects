# commands

```bash
docker ps
docker images

system prune -a
docker system prune --volumes
```

AWS config file

```bash
docker exec -it <container_name_or_id> /bin/bash

# sudo user
docker exec -it -u root <container_name_or_id> /bin/bash
```

```bash
apt apt update
apt install -y awscli

aws configure       --> aws credential
aws configure list  --> to get the all details
```
