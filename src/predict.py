import pandas as pd

from recommendation.recommender import Recommender

print("Starting")

rides_df = pd.read_csv("../Data/skyfleet_rides.csv")
feat_df = pd.read_csv("../Data/features.csv")

df = rides_df.merge(feat_df, on=["ride_id"])
recommender = Recommender()

df["recommendation"] = recommender.recommend(df)

df[["ride_id", "recommendation"]].to_json("../Data/results.json", orient='records', lines=True)

print("Done - created Data/results.json")
