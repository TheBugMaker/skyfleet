from client.ollama import ResponseGenerator
import re
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
from typing import Optional

class FeatureTransformer:
    def __init__(self, responseGen: ResponseGenerator):
        self.responseGen = responseGen

    def transform(self,
                  rides_df: pd.DataFrame,
                  drones_df: pd.DataFrame,
                  payments_df: pd.DataFrame,
                  weather_df: pd.DataFrame,
                  customer_queries_df: pd.DataFrame) -> dict[str, pd.DataFrame]:
        """Apply transformations to all the provided DataFrames."""
        rides_df = self.transform_rides(rides_df)
        drones_df = self.transform_drones(drones_df)
        payments_df = self.transform_payments(payments_df)
        #weather_df = self.transform_weather(weather_df) file incomplete use info from rides instead
        rides_df = self.transform_weather(rides_df)
        customer_queries_df = self.transform_consumer_sentiment(customer_queries_df)


        df = rides_df.merge(drones_df, on="drone_id")
        df = df.merge(payments_df, on="ride_id")
        #df = df.merge(weather_df, on=["location", "timestamp"], how="left")
        df = df.merge(customer_queries_df, on=["ride_id"])

        return df[["ride_id", "drone_id", "hour_of_day", "availability", "battery_level", "payment_status_encoded", "weather_conditions_encoded", "customer_sentiment"]]


    def transform_rides(self, rides_df: pd.DataFrame) -> pd.DataFrame:
        rides_df["hour_of_day"] = pd.to_datetime(rides_df["timestamp"]).dt.hour
        return rides_df

    def transform_drones(self, drones_df: pd.DataFrame) -> pd.DataFrame:
        drones_df["availability"] = drones_df["status"].str.lower() == "available"
        drones_df["availability"] = drones_df["availability"].astype(int)
        return drones_df

    def transform_payments(self, payments_df: pd.DataFrame) -> pd.DataFrame:
        encoder = OrdinalEncoder(categories=[["OK", "FAILED", "VERIFY_ADDRESS", "VERIFY_BANK_DETAILS"]])
        payments_df["payment_status_encoded"] = encoder.fit_transform(payments_df[["payment_status"]])
        payments_df["payment_status_encoded"] = payments_df["payment_status_encoded"].astype(int)
        return payments_df

    def transform_weather(self, weather_df: pd.DataFrame) -> pd.DataFrame:
        encoder = OrdinalEncoder(categories=[["Clear", "Rain", "Wind", "Storm", "Fog"]])
        weather_df["weather_conditions_encoded"] = encoder.fit_transform(weather_df[["weather_conditions"]])
        weather_df["weather_conditions_encoded"] = weather_df["weather_conditions_encoded"].astype(int)
        return weather_df

    def transform_consumer_sentiment(self, customer_queries_df: pd.DataFrame) -> pd.DataFrame:
        queries = customer_queries_df["customer_query"].unique()
        encoding: dict[str, Optional[int]] = {}

        for q in queries:
            ch = self.responseGen.generate(q)
            # Extract encoding in case LLM returns more than needed
            r = re.search(r'-1|0|1', ch)
            result = r.group(0) if r else None
            encoding[q] = result

        customer_queries_df["customer_sentiment"] = customer_queries_df["customer_query"].map(encoding).astype(int)
        return customer_queries_df
