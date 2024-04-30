#!/usr/bin/python3
"""handles all default RESTFul API actions for the link
    between Place objects and Amenity objects
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def amenities_of_place(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify([amenity.to_dict() for amenity in place.amenities])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'], strict_slashes=False)
def link_amenity_place(place_id, amenity_id):
    """Links or deletes an Amenity object to a Place object"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place or amenity is None:
        abort(404)
    if request.method == 'DELETE':
        if amenity not in place.amenities:
            abort(404)
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            place.amenities.remove(amenity)
        else:
            place.amenity_ids.remove(amenity_id)
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            place.amenities.append(amenity)
        else:
            place.amenity_ids.append(amenity_id)
        amenity.save()
        return jsonify(amenity.to_dict()), 201
