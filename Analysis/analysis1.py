import requests
import matplotlib.pyplot as plt
import threading
import time

# Function to send asynchronous requests to the load balancer
x = 0
def send_requests(url, count, result_dict):
    for _ in range(count):
        try:
            response = requests.get(url)
            ser = ""
            cond = False
            for i in response.text : 
                if i == '[' : 
                    cond = True
                    continue
                elif i == ']':
                    break
                if cond : 
                    ser+=i  
            if len(ser) != 0 : 
                server = ser
                result_dict[server] = result_dict.get(server, 0) + 1
        except requests.RequestException as e:
            print(f"Request failed: {e}")

# Function to plot the bar chart for load distribution analysis
def plot_load_distribution(result_dict):
    dixt = dict(result_dict) 
    for k, v in dixt.items(): 
        if v == 0 : 
            del result_dict[k]
    # print(result_dict.keys())
    plt.bar(result_dict.keys(), result_dict.values())
    plt.xlabel('Server ID')
    plt.ylabel('Number of Requests')
    plt.title('Load Distribution among Servers')
    plt.show()

# Main function to perform the load distribution analysis
def load_distribution_analysis(url, total_requests):
    result_dict = {}
    threads = [threading.Thread(target=send_requests, args=(url, total_requests//10, result_dict)) for _ in range(10)]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    plot_load_distribution(result_dict)

# usage
load_balancer_url = "http://127.0.0.1:5000/home"  # Replace with your load balancer URL
total_requests = 10000




def runner():
    load_distribution_analysis(load_balancer_url, total_requests)

runner()