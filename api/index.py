from flask import Flask, request, jsonify, send_file
import folium
import psycopg2


app = Flask(__name__)

BEARER_TOKEN = "teste"


@app.route("/")
def home():
    return "teste"


@app.route("/about")
def about():
    return "About"


def token_required(f):
    def decorator(*args, **kwargs):
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            return jsonify({"error": "Token ausente ou inválido"}), 401
        token = auth.split(" ")[1]
        if token != BEARER_TOKEN:
            return jsonify({"error": "Token inválido"}), 403
        return f(*args, **kwargs)

    return decorator


@app.route("/sum", methods=["POST"])
@token_required
def sum_values():
    error = False
    data = request.get_json()
    if "long" in data and "lat" in data:
        long = data["long"]
        lat = data["lat"]

        try:
            connection = psycopg2.connect(
                user="default",
                password="lGyDhq5ajBc0",
                host="ep-young-wood-a4vgletd-pooler.us-east-1.aws.neon.tech",
                database="verceldb",
            )
            cursor = connection.cursor()

            postgres_insert_query = (
                """ INSERT INTO reports ( longitude, latitude) VALUES (%s,%s)"""
            )
            record_to_insert = ( long, lat)
            cursor.execute(postgres_insert_query, record_to_insert)

            connection.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into reports table")

        except (Exception, psycopg2.Error) as error:
            print(f"Failed to insert record into reports table", error)
            
        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
                
        if error:
            return jsonify({"error": error}), 500
        else:
            return jsonify({"Added to database": 200})
    else:
        return jsonify({"error": "Both long and lat are required"}), 400

