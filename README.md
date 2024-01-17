To Run the docker image
- docker build -t < any name of the image > . (either this if you are in the directory where docker file resides or instead of . specify the path)
- docker images (to view the docker images)
- sudo docker run -p < any valid port >:5000 -e "SERVER_ID=< any number >" < any name of the image >
- sudo docker ps : To see ll the running images
- sudo docker stop < container id >