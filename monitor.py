from time import time

from flask import Flask
from flask_restful import Resource, Api

import nvsmi

class GpuStats(Resource):

    def get(self):
        return {} # TODO: parse GPU resource

if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(GpuStats, '/')
    app.run()



