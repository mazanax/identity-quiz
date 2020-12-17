# How to deploy

### Local machine
```
#!/usr/bin/env bash

echo "Building PRODUCTION image"
PARAM_SITE_HOST="protocol://site_host_without_trailing_slash"
PARAM_DB_NAME="dbname"
PARAM_DB_USER="dbuser"
PARAM_DB_PASS="dbpassword"
PARAM_DB_HOST="dbhost"

TAG=$(git rev-parse HEAD)
docker build -f .docker/Dockerfile -t quiz:$TAG -t quiz:latest \
  --build-arg APP_SITE_HOST=$PARAM_SITE_HOST \
  --build-arg POSTGRES_DB_NAME=$PARAM_DB_NAME \
  --build-arg POSTGRES_DB_USER=$PARAM_DB_USER \
  --build-arg POSTGRES_DB_PASS="$PARAM_DB_PASS" \
  --build-arg POSTGRES_DB_HOST=$PARAM_DB_HOST \
  --build-arg VK_CLIENT_ID="vk_client_id_for_oauth" \
  --build-arg VK_CLIENT_SECRET="vk_client_secret_for_oauth" \
  --build-arg FB_CLIENT_ID="fb_client_id_for_oauth" \
  --build-arg FB_CLIENT_SECRET="fb_client_secret_for_oauth" \
  --build-arg GOOGLE_CLIENT_ID="google_client_id_for_oauth" \
  --build-arg GOOGLE_CLIENT_SECRET="google_client_secret_for_oauth" \
  .

docker push quiz:$TAG
docker push quiz:latest
```

### Server
```
# docker-compose.yml for example :)

version: "3.3"
services:
  backend-1:
    image: "quiz:latest"
    ports:
      - "8888:80"
```

```
# update.sh for example :)

#!/usr/bin/env bash

docker pull quiz:latest && \
  docker-compose down && \
  docker-compose up -d && \
  docker image prune -f
```
