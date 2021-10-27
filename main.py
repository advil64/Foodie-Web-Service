from flask import Flask, abort, request, url_for, Blueprint
from flask_restx import Resource, Api, fields
from flask_cors import CORS
import json
from flask_ngrok import run_with_ngrok

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

GET_TWITTER_INFO = api.model("UserInfo", {
    "username": fields.String(),
    "profile_url": fields.String(),
    "bio": fields.String(),
    "date_created": fields.DateTime(dt_format="iso8601"),
    "display_name": fields.String(),
    "vectors": fields.List(fields.String()),
    "scores": fields.List(fields.Float())})

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
        description="The address you would like to find restaurants near",
        type="string",
    )
    # @api.marshal_with(GET_TWITTER_INFO, mask=None)
    def get(self):
        # user's screen name
        address = request.args.get("Address")
        # vec = getTwitterTimeline(request.args.get("Username"))
        # print(list(vec.values()))
        # return {"username": user.screen_name,
        #         "profile_url": user.profile_image_url,
        #         "bio": user.description,
        #         "date_created": user.created_at,
        #         "display_name": user.name,
        #         "vectors": list(vec.keys()),
        #         "scores": list(vec.values())}
        return {"Address": address}