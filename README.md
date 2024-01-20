To Run the docker image
- docker build -t < any name of the image > . (either this if you are in the directory where docker file resides or instead of . specify the path)
- docker images (to view the docker images)
- sudo docker run -p < any valid port >:5000 -e "SERVER_ID=< any number >" < any name of the image >
- sudo docker ps : To see ll the running images
- sudo docker stop < container id >

TEST 21/01/2024 - 00:22AM 
Server distribution now working.

Running :
go inside Server folder 
then RUN : 
1. docker build -t serverimage .
2. cd .. 
3. docker rm -f  $(docker ps -aq) (Repeat this in between the next call)
4. python3 load_balancer.py 

then opem the address : http://127.0.0.1:5000/home 
this should result in different servers getting called. 

Day Successfully wasted :) :) 
