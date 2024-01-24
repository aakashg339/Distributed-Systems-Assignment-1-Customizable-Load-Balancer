build_lb:
	docker-compose build load_balancer

run_lb:
	docker-compose up load_balancer

build_server:
	docker build -t serverimage ./path/to/Server

run_server:
	docker run --name Load_Balancer --network my_network -it serverimage

start: 
	docker build -t serverimage ./Server ; docker-compose build load_balancer ; docker-compose up load_balancer

clean:
	docker-compose down
