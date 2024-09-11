from client.ollama import Ollama
from context.context import USER_SENTIMENT
from preprocessing.extract_features import FeatureTransformer

import pandas as pd

print("Starting")

cl = Ollama(USER_SENTIMENT)
transformer = FeatureTransformer(cl)

dfs = []

for df_name in ["rides","drones","payments","weather","customer_queries"]:
    df = pd.read_csv(f"../Data/skyfleet_{df_name}.csv")
    dfs.append(df)


df = transformer.transform(*dfs)
df.to_csv(f"../Data/features.csv")

print("Done - created Data/features.csv")
