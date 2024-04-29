#!/usr/bin/python3
"""Basic routes for status and stats"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """retrieves the number of each objects by type"""
    from models import storage
    classes = {"Amenity": "amenities", "City": "cities",
               "Place": "places", "Review": "reviews",
               "State": "states", "User": "users"}
    stats = {}
    for key, value in classes.items():
        stats[value] = storage.count(key)
    return jsonify(stats)


@app_views.app_errorhandler(404)
def not_found(error):
    """Return 404 error jsonified"""
    return jsonify({"error": "Not found"}), 404
