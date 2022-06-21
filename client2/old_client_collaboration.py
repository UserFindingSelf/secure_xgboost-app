import securexgboost as xgb
import argparse

username = "user2"
HOME_DIR = "/home/secure-xgboost/central/"

def run(channel_addr, sym_key_file, priv_key_file, cert_file):
    xgb.init_client(user_name=username, client_list=[username, "user1"], sym_key_file=sym_key_file, priv_key_file=priv_key_file, cert_file=cert_file, remote_addr=channel_addr)

    # Remote attestation
    print("Remote attestation")
    # Note: Simulation mode does not support attestation pass in `verify=False` to attest()
    xgb.attest(verify=False)
    print("Report successfully verified")

    print("Load training matrices")
    dtrain = xgb.DMatrix({username: HOME_DIR + f"{username}-train.enc?format=csv&label_column=0", "user1": HOME_DIR + "user1-train.enc?format=csv&label_column=0"})

    print("Creating test matrix")
    dtest1 = xgb.DMatrix({"user1": HOME_DIR + "user1-test.enc?format=csv&label_column=0"})
    dtest2 = xgb.DMatrix({username: HOME_DIR + f"{username}-test.enc?format=csv&label_column=0"})

    print("Beginning Training")

    # Set training parameters
    params = {
            "tree_method": "hist",
            "n_gpus": "0",
            "objective": "binary:logistic",
            "min_child_weight": "1",
            "gamma": "0.1",
            "max_depth": "3",
            "verbosity": "0"
    }

    # Train and evaluate
    num_rounds = 10
    print("Training...")
    booster = xgb.train(params, dtrain, num_rounds)

    # Enable the other party to get its predictions
    print("Getting predictions")
    _, _ = booster.predict(dtest1, decrypt=False)

    # Get our predictions
    predictions, num_preds = booster.predict(dtest2, decrypt=False)

    # Decrypt predictions
    print("Predictions: ", booster.decrypt_predictions(predictions, num_preds)[:10])

    # Get fscores of model
    print("\nModel Feature Importance: ")
    print(booster.get_fscore())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip-addr", help="server IP address", required=True)
    parser.add_argument("--symmkey", help="path to symmetrix key used to encrypt data on client", required=True)
    parser.add_argument("--privkey", help="path to user's private key for signing data", required=True)
    parser.add_argument("--cert", help="path to user's public key certificate", required=True)
    parser.add_argument("--port", help="orchestrator port", default=50052)

    args = parser.parse_args()

    # Connect to the orchestrator
    channel_addr = str(args.ip_addr) + ":" + str(args.port)
    run(channel_addr, str(args.symmkey), str(args.privkey), str(args.cert))
