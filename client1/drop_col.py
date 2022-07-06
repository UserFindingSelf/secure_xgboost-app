import pandas as pd

client = "user1"
df_test = pd.read_csv(f"original_data/{client}-test.csv", header=None)

drop_features = 0
print("Dropping columns: ", drop_features)
df_test.drop(columns=drop_features, inplace=True)
df_test.to_csv(f"original_data/{client}-test_dropped.csv", index=False, header=False)
