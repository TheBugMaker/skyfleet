from flask import Blueprint, current_app, request, render_template, jsonify

recommendation_bp = Blueprint('recommendation', __name__)

@recommendation_bp.route('/decision/v1', methods=["POST"])
def recommendation():
    recommender = current_app.container.recommender()

    data = request.json
    result = recommender.generate_recommendation(data)
    return jsonify(result)
