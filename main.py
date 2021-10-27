from flask import Flask, abort, request, url_for, Blueprint
from flask_restx import Resource, Api, fields
from flask_cors import CORS
import json
from flask_ngrok import run_with_ngrok
from .queries import get_geocode, find_food

app = Flask(__name__)
cors = CORS(app)
run_with_ngrok(app)

blueprint = Blueprint("api", __name__, url_prefix="/")

api = Api(
    blueprint,
    version="0.1.0",
    title="Foodie Web Service",
    doc="/docs"
)

app.register_blueprint(blueprint)

BUSINESS_MODEL = api.model("Business", {
    'name': fields.String(required=True),
    'address': fields.String(required=True),
    'rating': fields.Float(required=True),
})

RESTAURANT_RESULTS_MODEL = api.model("Restaurants", {
    'restaurants': fields.List(fields.Nested(BUSINESS_MODEL)),
})

# documentation for swagger UI
restaurants = api.namespace(
    "restaurants", description="Returns list of nearby restaurants given an address"
)

@restaurants.route("")
class GetUserAnalytics(Resource):
    """
    Returns list of restaurants
    """
    @api.param(
        "Address",
        description="The address you would like to find restaurants near (Ex. 3425 Stone Street, Apt. 2A, Jacksonville, FL 39404)",
        type="string",
    )
    @api.marshal_with(RESTAURANT_RESULTS_MODEL, mask=None)
    def get(self):
        lat, long = get_geocode(request.args.get("Address"))
        results = find_food(lat, long)
        return {'restaurants': results}