import requests
import logging
import psycopg2
from flask import Flask, request, jsonify
from flask_restful import Api, Resource

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
api = Api(app)

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(
        host="postgres",
        database="eventdb",
        user="sathish6",
        password="satkum66"
    )
    return conn

# Initialize the database table
def init_db():
    logging.info("Attempting to initialize the database...")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100),
            description TEXT,
            date DATE
        );
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# Ensure the table exists when the service starts
init_db()

class EventList(Resource):
    def get(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events;")
        events = cursor.fetchall()
        cursor.close()
        conn.close()

        # Convert the list of tuples to a list of dictionaries for JSON response
        event_list = [
            {"id": row[0], "title": row[1], "description": row[2], "date": row[3].isoformat()}
            for row in events
        ]
        return jsonify(event_list)

    def post(self):
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO events (title, description, date) VALUES (%s, %s, %s) RETURNING id;",
            (data['title'], data['description'], data['date'])
        )
        event_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()

        # Notify the Notification Service about the new event
        try:
            notify_url = "http://notification-service:5001/notify"  # URL of the Notification Service
            notify_data = {"title": data["title"]}
            response = requests.post(notify_url, json=notify_data)
            response.raise_for_status()  # Check if the request was successful
        except requests.exceptions.RequestException as e:
            logging.error(f"Error notifying service: {e}")
            return {"message": "Event created, but notification failed"}, 201

        # Return the created event with status 201
        return {"id": event_id, "title": data["title"], "description": data["description"], "date": data["date"]}, 201

class Event(Resource):
    def get(self, event_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events WHERE id = %s;", (event_id,))
        event = cursor.fetchone()
        cursor.close()
        conn.close()

        if event is None:
            return {"message": "Event not found"}, 404

        return jsonify({"id": event[0], "title": event[1], "description": event[2], "date": event[3].isoformat()})

    def put(self, event_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM events WHERE id = %s;", (event_id,))
        event = cursor.fetchone()

        if event is None:
            cursor.close()
            conn.close()
            return {"message": "Event not found"}, 404

        data = request.get_json()
        cursor.execute(
            "UPDATE events SET title = %s, description = %s, date = %s WHERE id = %s;",
            (data.get("title", event[1]), data.get("description", event[2]), data.get("date", event[3]), event_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return {"message": "Event updated"}, 200

    def delete(self, event_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM events WHERE id = %s RETURNING id;", (event_id,))
        deleted_event = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()

        if deleted_event is None:
            return {"message": "Event not found"}, 404

        return {"message": "Event deleted"}, 200

# Define routes for the API
api.add_resource(EventList, '/events')
api.add_resource(Event, '/events/<int:event_id>')

if __name__ == '__main__':
    # Run the application on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)

