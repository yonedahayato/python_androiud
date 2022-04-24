IMAGE_NAME=kivy-gpu:dev.0.1
# IMAGE_NAME=uphy/ubuntu-desktop-jp:20.04

# docker build -t ${IMAGE_NAME} --no-cache .
docker run -it --rm -p 8081:8080 -v $PWD:/home/work ${IMAGE_NAME} /bin/bash