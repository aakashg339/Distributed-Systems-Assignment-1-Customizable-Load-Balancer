import hashlib
import os


def returnSmallestId(n, ids):
    for i in range(1, n+1):
        print(i, end = ".")

returnSmallestId(5,[1,2])


def hash_function(value):
    return int(hashlib.md5(value.encode()).hexdigest(), 16) % (2**32)



def createServer(id):
    return os.popen(f'docker run --name {id} --network net1 --network-alias {id} -e SERVER_ID={id} -d mainimage:latest').read()