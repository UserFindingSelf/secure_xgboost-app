import securexgboost as xgb
import argparse
import pandas as pd
from sklearn.metrics import classification_report

DATA_DIR = "data/"
username = "user1"
users = ["user1", "user2"]
HOME_DIR = "/home/secure-xgboost/central/" # Directory of encrypted data on the server

def run(config_file):
    df = pd.read_csv(DATA_DIR + username + "-test.csv", header=None)
    y_test = df[0].to_numpy()

    xgb.init_client(config=config_file)

    # Remote attestation
    print("Remote attestation")
    # Note: Simulation mode does not support attestation pass in `verify=False` to attest()
    xgb.attest(verify=False)
    print("Report successfully verified")

    print("Load training matrices")
    dtrain = xgb.DMatrix({user: HOME_DIR + f"{user}-train.enc?format=csv&label_column=0" for user in users})

    print("Creating test matrix")
    dtest1 = xgb.DMatrix({users[0]: HOME_DIR + f"{users[0]}-test.enc?format=csv&label_column=0"})
    dtest2 = xgb.DMatrix({users[1]: HOME_DIR + f"{users[1]}-test.enc?format=csv&label_column=0"})

    print("Beginning Training")

    # Set training parameters
    params = {
    	"objective": "binary:logistic",
    	"gamma": "0.1",
    	"nthread": "4",
    	"max_depth": "50",
    	"eval_metric": ["logloss"] # , "auc"
    }
    num_rounds = 50

    # Train and evaluate
    print("Training...")
    booster = xgb.train(params, dtrain, num_rounds)

    # Get our predictions
    print("Getting predictions")
    predictions, num_preds = booster.predict(dtest1, decrypt=False)

    # Enable the other party to get its predictions
    _, _ = booster.predict(dtest2, decrypt=False)

    # Decrypt predictions
    pred_prob = booster.decrypt_predictions(predictions, num_preds)
    threshold = 0.5
    y_pred = [0 if prob<=threshold else 1 for prob in pred_prob]
    print("\n" + classification_report(y_test, y_pred))

    # Get fscores of model
    # print("\nModel Feature Importance: ")
    # print(booster.get_fscore())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Client config file containing user name, client list, remote address of server and locations of keys and certificates", required=True)
    args = parser.parse_args()

    run(args.config)
