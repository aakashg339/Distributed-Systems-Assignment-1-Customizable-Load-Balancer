import os 

## For Testing Purpose : 
def dropServer(container_name): 
    os.popen(f"sudo docker stop {container_name}")
    os.popen(f"sudo docker rm {container_name}")