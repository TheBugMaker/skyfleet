import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pytest
import pandas as pd
from unittest.mock import Mock
from preprocessing.extract_features import FeatureTransformer
from client.ollama import ResponseGenerator

@pytest.fixture
def mock_response_gen():
    # Mock the ResponseGenerator
    mock = Mock(spec=ResponseGenerator)
    mock.generate.side_effect = lambda query: "1" if "positive" in query.lower() else "-1"
    return mock


@pytest.fixture
def sample_dataframes():
    # Sample data to test with
    rides_data = {
        "ride_id": [1, 2],
        "timestamp": ["2024-09-10 10:00:00", "2024-09-10 15:00:00"],
        "drone_id": [101, 102],
        "weather_conditions": ["Clear", "Rain"]
    }

    drones_data = {
        "drone_id": [101, 102],
        "status": ["available", "unavailable"],
        "battery_level": [60, 80]
    }

    payments_data = {
        "ride_id": [1, 2],
        "payment_status": ["OK", "FAILED"]
    }

    weather_data = {
        "location": ["Downtown", "Uptown"],
        "timestamp": ["2024-09-10 10:00:00", "2024-09-10 15:00:00"],
        "weather_conditions": ["Clear", "Rain"]
    }

    customer_queries_data = {
        "ride_id": [1, 2],
        "customer_query": ["Is everything fine?", "Not satisfied with the ride"]
    }

    rides_df = pd.DataFrame(rides_data)
    drones_df = pd.DataFrame(drones_data)
    payments_df = pd.DataFrame(payments_data)
    weather_df = pd.DataFrame(weather_data)
    customer_queries_df = pd.DataFrame(customer_queries_data)

    return rides_df, drones_df, payments_df, weather_df, customer_queries_df


def test_transform_rides():
    rides_data = {
        "ride_id": [1],
        "timestamp": ["2024-09-10 10:00:00"],
        "drone_id": [101]
    }
    rides_df = pd.DataFrame(rides_data)

    transformer = FeatureTransformer(Mock())
    transformed_df = transformer.transform_rides(rides_df)

    assert "hour_of_day" in transformed_df.columns
    assert transformed_df["hour_of_day"].iloc[0] == 10


def test_transform_drones():
    drones_data = {
        "drone_id": [101, 102],
        "status": ["available", "unavailable"],
        "battery_level": [60, 80]
    }
    drones_df = pd.DataFrame(drones_data)

    transformer = FeatureTransformer(Mock())
    transformed_df = transformer.transform_drones(drones_df)

    assert "availability" in transformed_df.columns
    assert transformed_df["availability"].iloc[0] == 1
    assert transformed_df["availability"].iloc[1] == 0


def test_transform_payments():
    payments_data = {
        "ride_id": [1, 2],
        "payment_status": ["OK", "FAILED"]
    }
    payments_df = pd.DataFrame(payments_data)

    transformer = FeatureTransformer(Mock())
    transformed_df = transformer.transform_payments(payments_df)

    assert "payment_status_encoded" in transformed_df.columns
    assert transformed_df["payment_status_encoded"].iloc[0] == 0
    assert transformed_df["payment_status_encoded"].iloc[1] == 1


def test_transform_consumer_sentiment(mock_response_gen):
    customer_queries_data = {
        "ride_id": [1, 2],
        "customer_query": ["positive feedback", "negative feedback"]
    }
    customer_queries_df = pd.DataFrame(customer_queries_data)

    transformer = FeatureTransformer(mock_response_gen)
    transformed_df = transformer.transform_consumer_sentiment(customer_queries_df)

    assert "customer_sentiment" in transformed_df.columns
    assert transformed_df["customer_sentiment"].iloc[0] == 1
    assert transformed_df["customer_sentiment"].iloc[1] == -1


def test_transform_full(mock_response_gen, sample_dataframes):
    rides_df, drones_df, payments_df, weather_df, customer_queries_df = sample_dataframes

    transformer = FeatureTransformer(mock_response_gen)
    transformed_df = transformer.transform(rides_df, drones_df, payments_df, weather_df, customer_queries_df)

    # Ensure the resulting DataFrame has all expected columns
    expected_columns = [
        "ride_id", "drone_id", "hour_of_day", "availability",
        "battery_level", "payment_status_encoded",
        "weather_conditions_encoded", "customer_sentiment"
    ]
    for column in expected_columns:
        assert column in transformed_df.columns
    assert len(transformed_df) == 2  # Make sure we have 2 rows


def test_transform_weather():
    weather_data = {
        "location": ["Downtown", "Uptown"],
        "timestamp": ["2024-09-10 10:00:00", "2024-09-10 15:00:00"],
        "weather_conditions": ["Clear", "Rain"]
    }
    weather_df = pd.DataFrame(weather_data)

    transformer = FeatureTransformer(Mock())
    transformed_df = transformer.transform_weather(weather_df)

    assert "weather_conditions_encoded" in transformed_df.columns
    assert transformed_df["weather_conditions_encoded"].iloc[0] == 0
    assert transformed_df["weather_conditions_encoded"].iloc[1] == 1

