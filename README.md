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


NOTE :: 
docker-compose has not yet set been set up 



Jan 21 19:27 PM 

Load Balancer now in working condition. 

Added the things below 
- Added the health check for the servers that makes sure that a minimum of N(3 initially) servers are running every time 
- Make adjustments to handle concurrent requests and deletion/maintainance of servers
- Handled some edge cases for all the /add, /rem and /<path> methods 


How to use ? 
Go inside Server folder 
then RUN : 
1. docker build -t serverimage .
2. cd .. 
<!-- 3. docker rm -f  $(docker ps -aq) (Repeat this in between the next call) --> // Not needed now, I have called this from within the load-balancer. 
3. python3 load_balancer.py

then opem the address : http://127.0.0.1:5000/home 
this should result in different servers getting called. 



IMP : 
docker run -v /var/run/docker.sock:/var/run/docker.sock -it your_image_name

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Changes Jan 23 2024

1. simlified the Consistent Hashing function 
2. introduced quadratic hashing 
3. made requests id as a 6 digit random number 
4. Now the loadbalancer is successfully running inside a container and spawning the servers ..

NEW ISSUE : 
helper.get_container_ip() is not returning anything .. If that is fixed, this will be almost complete. 


RUNNING : 
1. go to Server/  => then run :          docker build -t serverimage . 
2. go to loadBalancer/ =>  then run :    docker build -t loadbalancer 
3. run the command : docker run -p 5000:5000 --privileged=true -v /var/run/docker.sock:/var/run/docker.sock -it loadbalancer