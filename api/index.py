from flask import Flask, request, jsonify, send_file
import folium
import psycopg2
from datetime import datetime, timedelta

app = Flask(__name__)

BEARER_TOKEN = "teste"


@app.route("/")
def home():
    return "online"


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


@app.route("/insert", methods=["POST"])
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

@app.route("/iframe")
def iframe():
    try:
        connection = psycopg2.connect(
            user="default",
            password="lGyDhq5ajBc0",
            host="ep-young-wood-a4vgletd-pooler.us-east-1.aws.neon.tech",
            database="verceldb",
        )
        cursor = connection.cursor()

        # Calcular o timestamp de 12 horas atrás
        current_time_utc = datetime.utcnow()
        twelve_hours_ago = current_time_utc - timedelta(hours=12)

        # Consulta para selecionar as linhas adicionadas nas últimas 12 horas
        postgres_select_query = """SELECT * FROM reports WHERE timestamp >= %s"""
        cursor.execute(postgres_select_query, (twelve_hours_ago,))
        records = cursor.fetchall()

        # Criar uma lista de dicionários para armazenar os registros
        reports_list = []
        for row in records:
            report = {
                "ID": row[0],
                "Longitude": row[1],
                "Latitude": row[2],
                "Timestamp": row[3].isoformat()  # Converte o timestamp para string
            }
            reports_list.append(report)

        m = folium.Map(location=[-24.1726268, -46.5631057], zoom_start=9)
        radius = 50
        for i in range(len(reports_list)):
            timestamp_utc = datetime.fromisoformat(reports_list[i]['Timestamp'])
            timestamp_local = timestamp_utc - timedelta(hours=3)
            formatted_timestamp = timestamp_local.strftime("%Y-%m-%d %H:%M:%S")
            folium.CircleMarker(location=[reports_list[i]['Longitude'], reports_list[i]['Latitude']],
                                radius=radius,
                                weight=1,
                                color='red',
                                fill=True,
                                fill_color='red',
                                tooltip=f"Reportado em {formatted_timestamp} ").add_to(m)
        m.get_root().width = "800px"
        m.get_root().height = "600px"
        iframe = m.get_root()._repr_html_()
        print("Records saved successfully into reports.json")
        
    except (Exception, psycopg2.Error) as error:
        
        return(f"Failed to fetch records from reports table", error)

    finally:
        # Fechar a conexão com o banco de dados
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
            return(iframe)

