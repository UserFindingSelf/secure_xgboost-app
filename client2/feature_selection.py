import pandas as pd

client = "user2"
df_train = pd.read_csv(f"original_data/{client}-train.csv", header=None)
df_test = pd.read_csv(f"original_data/{client}-test.csv", header=None)

fscore = {
  "f9": 108,
  "f1": 6103,
  "f3": 221,
  "f56": 329,
  "f5": 368,
  "f7": 562,
  "f0": 4085,
  "f8": 3086,
  "f32": 539,
  "f26": 142,
  "f50": 24,
  "f42": 137,
  "f29": 371,
  "f37": 578,
  "f14": 121,
  "f31": 208,
  "f28": 211,
  "f10": 513,
  "f6": 693,
  "f19": 288,
  "f13": 32,
  "f48": 51,
  "f2": 1432,
  "f39": 244,
  "f57": 358,
  "f4": 293,
  "f23": 457,
  "f43": 173,
  "f52": 67,
  "f33": 52,
  "f60": 91,
  "f58": 339,
  "f55": 266,
  "f54": 27,
  "f59": 312,
  "f40": 208,
  "f22": 103,
  "f20": 40,
  "f46": 35,
  "f45": 26,
  "f16": 58,
  "f18": 56,
  "f21": 21,
  "f27": 79,
  "f53": 41,
  "f12": 41,
  "f11": 213,
  "f34": 191,
  "f24": 313,
  "f17": 144,
  "f15": 109,
  "f49": 59,
  "f47": 7,
  "f51": 72,
  "f38": 11,
  "f62": 13
}

fscore_sorted ={k: v for k, v in sorted(fscore.items(), key=lambda item: item[1])}
print(fscore_sorted)
remove_top_n = 2
drop_features = []
for i, k in enumerate(fscore_sorted.keys()):
    if i >= len(fscore_sorted)-remove_top_n:
        drop_features.append(int(k[1:]) + 1)
print("Dropping columns: ", drop_features)

print(df_train.shape)
df_train.drop(columns=drop_features, inplace=True)
print(df_train.shape)
df_train.to_csv(f"original_data/rem_top_{remove_top_n}_{client}-train.csv", index=False, header=False)
df_test.drop(columns=drop_features, inplace=True)
df_test.to_csv(f"original_data/rem_top_{remove_top_n}_{client}-test.csv", index=False, header=False)
