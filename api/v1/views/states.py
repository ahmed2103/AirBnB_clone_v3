#!/usr/bin/python3
"""Handles all default RestFul API actions for State objects"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import base_model, storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    states = storage.all("State")
    return jsonify([state.to_dict() for state in states.values()])


@app_views.route('/states/<state_id>',
                 methods=['GET', 'DELETE'], strict_slashes=False)
def get_or_del_state(state_id):
    """Retrieves a State object & deletes it if requested"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(state.to_dict())
    else:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State object and saves it to the database """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    state = State(**request.get_json())
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
