import pytest
import pandas as pd
from enum import Enum
from recommendation.recommender import Recommendation, Recommender  # Assuming the code is in recommender.py

# Sample test data to be used in the tests
@pytest.fixture
def sample_data():
    return pd.DataFrame([
        # Rule 1: ACCEPT
        {"availability": 1, "battery_level": 60, "payment_status_encoded": 0, "weather_conditions_encoded": 0, "customer_sentiment": 1},  # ACCEPT
        {"availability": 1, "battery_level": 55, "payment_status_encoded": 0, "weather_conditions_encoded": 1, "customer_sentiment": 0},  # ACCEPT

        # Rule 5: DECLINE (negative sentiment, failed payment, or low battery)
        {"availability": 1, "battery_level": 40, "payment_status_encoded": 1, "weather_conditions_encoded": 0, "customer_sentiment": -1},  # DECLINE
        {"availability": 1, "battery_level": 40, "payment_status_encoded": 1, "weather_conditions_encoded": 2, "customer_sentiment": -1},  # DECLINE

        # Rule 2: HOLD, CHECK AVAILABILITY
        {"availability": 0, "battery_level": 60, "payment_status_encoded": 0, "weather_conditions_encoded": 0, "customer_sentiment": 1},  # CHECK_AVAILABILITY

        # Rule 3: HOLD, CHECK WEATHER
        {"availability": 1, "battery_level": 70, "payment_status_encoded": 0, "weather_conditions_encoded": 3, "customer_sentiment": 1},  # CHECK_WEATHER
        {"availability": 1, "battery_level": 70, "payment_status_encoded": 0, "weather_conditions_encoded": 4, "customer_sentiment": 1},  # CHECK_WEATHER

        # Rule 4: HOLD, CHECK PAYMENT
        {"availability": 1, "battery_level": 70, "payment_status_encoded": 2, "weather_conditions_encoded": 0, "customer_sentiment": 1},  # CHECK_PAYEMENT
        {"availability": 1, "battery_level": 70, "payment_status_encoded": 3, "weather_conditions_encoded": 0, "customer_sentiment": 1},  # CHECK_PAYEMENT

        # Default: UNDEFINED
        {"availability": 1, "battery_level": 70, "payment_status_encoded": 0, "weather_conditions_encoded": 2, "customer_sentiment": -5},  # UNDEFINED
    ])


def test_recommend_accept(sample_data):
    recommender = Recommender()

    # Extract the first and second rows (both should return ACCEPT)
    recommendation = recommender.recommend(sample_data.iloc[[0, 1]])

    assert recommendation.iloc[0] == Recommendation.ACCEPT
    assert recommendation.iloc[1] == Recommendation.ACCEPT


def test_recommend_decline(sample_data):
    recommender = Recommender()

    # Extract the third and fourth rows (both should return DECLINE)
    recommendation = recommender.recommend(sample_data.iloc[[2, 3]])

    assert recommendation.iloc[0] == Recommendation.DECLINE
    assert recommendation.iloc[1] == Recommendation.DECLINE


def test_recommend_check_availability(sample_data):
    recommender = Recommender()

    # Extract the fifth row (should return CHECK_AVAILABILITY)
    recommendation = recommender.recommend(sample_data.iloc[[4]])

    assert recommendation.iloc[0] == Recommendation.CHECK_AVAILABILITY


def test_recommend_check_weather(sample_data):
    recommender = Recommender()

    # Extract the sixth and seventh rows (both should return CHECK_WEATHER)
    recommendation = recommender.recommend(sample_data.iloc[[5, 6]])

    assert recommendation.iloc[0] == Recommendation.CHECK_WEATHER
    assert recommendation.iloc[1] == Recommendation.CHECK_WEATHER


def test_recommend_check_payment(sample_data):
    recommender = Recommender()

    # Extract the eighth and ninth rows (both should return CHECK_PAYEMENT)
    recommendation = recommender.recommend(sample_data.iloc[[7, 8]])

    assert recommendation.iloc[0] == Recommendation.CHECK_PAYEMENT
    assert recommendation.iloc[1] == Recommendation.CHECK_PAYEMENT


def test_recommend_undefined(sample_data):
    recommender = Recommender()

    # Extract the last row (should return UNDEFINED)
    recommendation = recommender.recommend(sample_data.iloc[[9]])

    assert recommendation.iloc[0] == Recommendation.UNDEFINED

