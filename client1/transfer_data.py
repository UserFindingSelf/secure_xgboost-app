from Utils import *

data_dir = "data/"
user = "user1"
with open("config/hosts.config") as f:
    nodes = f.readlines()
nodes = [x.strip().split(":")[0] for x in nodes]

for n in nodes:
    transfer_data(data_dir + user + "-test.enc", n)
    transfer_data(data_dir + user + "-train.enc", n)

print(f"Encrypted {user} data tranferred")
