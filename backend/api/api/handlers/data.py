from flask import Blueprint, jsonify, abort
from flask_restful import Resource, Api

from api.tools.api import get_inn_data, get_auction_id_data
from api.database.operations import Periodicity

blueprint = Blueprint(
    "data_resource",
    __name__,
)
api = Api(blueprint)


class InnResource(Resource):
    def get(self, inn_number):
        data = get_inn_data(inn_number)
        if not data:
            abort(404, "No suggestions found")
        return jsonify(data)


class AuctionResource(Resource):
    def get(self, auction_id):
        data = get_auction_id_data(auction_id)
        if not data:
            abort(404, "No auctions found")
        return jsonify({"data": data})


class PeriodicityPredictionsResource(Resource):
    def get(self, inn_number):
        data = Periodicity.get_records_by_inn(inn_number)
        if type(data) is str:
            abort(404, data)
        # if not data:
        #     abort(404, "No records found")
        return jsonify({"records": data[::-1]})


# class LastPeriodicityPredictionsResource(Resource):
#     def get(self, inn_number):
#         data = Periodicity.get_records_by_inn(inn_number)
#         if type(data) is str:
#             abort(404, data)
#         return jsonify({"data": data[-1]})


api.add_resource(InnResource, "/inn/<inn_number>")
api.add_resource(AuctionResource, "/auction/<auction_id>")
api.add_resource(PeriodicityPredictionsResource, "/predictions/periodicity/<inn_number>")
# api.add_resource(LastPeriodicityPredictionsResource, "/predictions/periodicity/last/<inn_number>")
