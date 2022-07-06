import subprocess
import argparse
import time
import sys
import os
import securexgboost as xgb

running_processes = []

def start_server(clients):
    global running_processes

    if running_processes:
        for ps in running_processes:
            ps.kill()
        running_processes = []

    enclave = ["python3", "utils/launch_enclave.py", str(clients)]
    orchestrator = ["python3", "utils/start_orchestrator.py", str(clients)]

    process = subprocess.Popen(enclave, preexec_fn=os.setsid)
    running_processes.append(process)

    process2 = subprocess.Popen(orchestrator, preexec_fn=os.setsid)
    running_processes.append(process2)
    print("Started server for " + str(clients))

def stop_server():
    global running_processes

    if running_processes:
        for ps in running_processes:
            ps.kill()
        running_processes = []

prev_clients = ["user1", "user2"]
while True:
    # mode = input("\nTraining [T/t] or Inference [I/i] (Anything else leads to exit): ")
    # if mode == 'T' or mode == 't':
        # clients = input("Enter all client names separated by space: ")
        # clients = clients.strip().split()
    # elif mode == 'I' or mode == 'i':
        # clients = input("Enter client name: ")
        # clients = clients.strip().split()
        #clients = [clients.strip()]
    # else:
        # stop_server()
        # print("Exiting")
        # break
    # Using default client
    clients = input(f"\nEnter client names, separted by space. Just press enter to repeat previous clients {prev_clients}: ")
    if clients:
        clients = clients.strip().split()
        prev_clients = clients
    else:
        clients = prev_clients
    start_server(clients)
    time.sleep(2)
    cont = input("\nEnter Y/y if you want to stop the server: ")
    if cont == 'Y' or cont == 'y':
        stop_server()
        break
