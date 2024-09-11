from dependency_injector import containers, providers
from .services import RecommenderService

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    recommender = providers.Factory(
        RecommenderService,
        sentimentAnalyser=config.sentimentAnalyser,
        features_df = config.features
    )
