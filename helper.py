import hashlib
import os

def hash_function(value):
    return int(hashlib.md5(value.encode()).hexdigest(), 16) % (2**32)



# id is a numeric value 
def createServer(id):
    container_name = f'server{id}'  # Adjust the naming convention as needed
    return os.popen(f'docker run --name {container_name} --network net1 --network-alias {container_name} -e SERVER_ID={id} -d serverimage').read()