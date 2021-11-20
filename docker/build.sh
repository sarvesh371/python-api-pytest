image=$(cat Dockerfile | grep "IMAGE_NAME" | cut -d "=" -f2 | sed s/\'//g)
docker build --tag $image --no-cache .
