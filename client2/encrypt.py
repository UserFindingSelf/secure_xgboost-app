import securexgboost as xgb
from Utils import *

data_dir = "data/"
user = "user2"

# Generating certificates and keys
generate_certificate(user)
PRIV_KEY = f"config/{user}.pem"
CERT_FILE = f"config/{user}.crt"
KEY_FILE = f"config/{user}_key.txt"
xgb.generate_client_key(KEY_FILE)

# Server node ips file and cleint list
HOSTS_FILE = "config/hosts.config"
PORT = "50052"
CLIENTS = "user1"

# Creating client config file
output_dir = "config/"
create_client_config(output_dir, user, PRIV_KEY, CERT_FILE, KEY_FILE, HOSTS_FILE, PORT, CLIENTS)

# Setting file locations
training_data = data_dir + "{}-train.csv".format(user)
test_data = data_dir + "{}-test.csv".format(user)

enc_training_data = data_dir + "{}-train.enc".format(user)
enc_test_data = data_dir + "{}-test.enc".format(user)

# Encrypting data
xgb.encrypt_file(training_data, enc_training_data, KEY_FILE)
xgb.encrypt_file(test_data, enc_test_data, KEY_FILE)

print("\n******************************************************\n\
Config file generated and data encrypted successfully")
