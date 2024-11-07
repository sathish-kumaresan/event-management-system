import logging
from flask import Flask, request, jsonify
from flask_restful import Api, Resource

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
api = Api(app)

class Notify(Resource):
    def post(self):
        data = request.get_json()
        event_title = data.get("title")
        logging.info(f"Notification: New event created - {event_title}")
        return {"message": f"Notification sent for event '{event_title}'"}, 200

api.add_resource(Notify, '/notify')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

