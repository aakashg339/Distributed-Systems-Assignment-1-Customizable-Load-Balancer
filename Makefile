run:
	sudo docker build -t serverimage ./Server
	sudo docker build -t loadbalancer ./loadBalancer
	if ! sudo docker network inspect my_network &> /dev/null; then     sudo docker network create my_network; fi
	sudo docker run -p 5000:5000 --privileged=true -v /var/run/docker.sock:/var/run/docker.sock --name my_loadbalancer_app --network my_network -it loadbalancer