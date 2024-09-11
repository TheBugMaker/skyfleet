from enum import Enum

class Recommendation(str, Enum):
    ACCEPT = "ACCEPT"
    CHECK_AVAILABILITY = "HOLD, CHECK_AVAILABILITY"
    CHECK_WEATHER = "HOLD, CHECK_WEATHER"
    CHECK_PAYEMENT = "HOLD, CHECK_PAYEMENT"
    DECLINE = "DECLINE"
    UNDEFINED = "UNDEFINED"

class Recommender:
    MIN_BATTER_LEVEL = 50

    def recommend(self, df):
        return df.apply(self._apply_rules, axis=1)

    def _apply_rules(self, data):
        # Extract the required parameters from the dictionary
        drone_availability = data.get("availability")
        battery_level = data.get("battery_level")
        payment_status = data.get("payment_status_encoded")
        weather_condition = data.get("weather_conditions_encoded")
        customer_sentiment = data.get("customer_sentiment")

        # Rule 1: ACCEPT
        if (drone_availability == 1 and
            battery_level >= self.MIN_BATTER_LEVEL and
            payment_status == 0 and
            weather_condition in [0, 1] and
            customer_sentiment >= 0):
            return Recommendation.ACCEPT

        # Rule 5: DECLINE
        # (would be more logically to be evaluated second)
        elif (customer_sentiment == -1 or
              payment_status == 1 or
              battery_level < self.MIN_BATTER_LEVEL):
              #battery_level < 20): # doesn't make sense to set it at 20
            return Recommendation.DECLINE

        # Rule 2: HOLD, CHECK AVAILABILITY
        elif drone_availability == 0:
            return Recommendation.CHECK_AVAILABILITY

        # Rule 3: HOLD, CHECK WEATHER
        elif weather_condition in [3, 4]:
            return Recommendation.CHECK_WEATHER

        # Rule 4: HOLD, CHECK PAYMENT
        elif payment_status in [2, 3]:
            return Recommendation.CHECK_PAYEMENT

        # Default case if no conditions match
        return Recommendation.UNDEFINED
