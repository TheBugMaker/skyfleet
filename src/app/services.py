from sklearn.preprocessing import OrdinalEncoder
from ..client.ollama import ResponseGenerator
from ..recommendation.recommender import Recommender
import pandas as pd

class RecommenderService:
    def __init__(self, sentimentAnalyser : ResponseGenerator, features_df):
        self.sentimentAnalyser = sentimentAnalyser
        self.weather_encoder =  OrdinalEncoder(categories=[["Clear", "Rain", "Wind", "Storm", "Fog"]])
        self.features_df = features_df

    def _run_sentiment_analysis(self, query):
        return self.sentimentAnalyser.generate(query)

    def generate_recommendation(self, data):
        data["customer_sentiment"] = self._run_sentiment_analysis(data["customer_query"])
        data["weather_conditions_encoded"] = self.weather_encoder.fit_transform([[data["weather_conditions"]]])[0]

        df = pd.DataFrame([data])
        df = df.merge(self.features_df[["ride_id", "drone_id", "availability", "payment_status_encoded", "battery_level"]], on=["ride_id"])
        if df.empty:
            return {
                "ride_id": data["ride_id"],
                "error": "UNKNOWEN ID"
            }
        df["recommendation"] = Recommender().recommend(df)
        return df[["ride_id", "recommendation"]].iloc[0].to_dict()
