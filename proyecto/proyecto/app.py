from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from geopy.distance import geodesic

app = Flask(__name__)
CORS(app)  # Habilita CORS para permitir peticiones desde diferentes orígenes

# Configuración de la conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',            # Reemplaza con tu usuario de MySQL
        password='12345',     # Reemplaza con tu contraseña de MySQL
        database='sistema_estudiantes'
    )

# Ruta para agregar un nuevo estudiante en la base de datos
@app.route('/estudiantes', methods=['POST'])
def crear_estudiante():
    datos = request.get_json()
    cedula = datos['cedula']
    nombres = datos['nombres']
    apellidos = datos['apellidos']
    direccion_residencia = datos['direccion_residencia']
    lat_residencia = datos['lat_residencia']
    lon_residencia = datos['lon_residencia']
    direccion_trabajo = datos['direccion_trabajo']
    lat_trabajo = datos['lat_trabajo']
    lon_trabajo = datos['lon_trabajo']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Insertar el estudiante en la base de datos con las coordenadas de residencia y trabajo
    try:
        cursor.execute('''
    INSERT INTO Estudiantes (cedula, nombres, apellidos, direccion_residencia, residencia, direccion_trabajo, trabajo)
    VALUES (%s, %s, %s, %s, ST_GeomFromText(%s, 4326), %s, ST_GeomFromText(%s, 4326))
''', (cedula, nombres, apellidos, direccion_residencia, f'POINT({lon_residencia} {lat_residencia})',
    direccion_trabajo, f'POINT({lon_trabajo} {lat_trabajo})'))


        conn.commit()
        response = {"message": "Estudiante creado exitosamente"}
    except mysql.connector.Error as err:
        response = {"error": str(err)}
    finally:
        cursor.close()
        conn.close()

    return jsonify(response), 201



# Ruta para obtener todos los estudiantes con la distancia entre residencia y trabajo
@app.route('/estudiantes', methods=['GET'])
def obtener_estudiantes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT id, cedula, nombres, apellidos, direccion_residencia, direccion_trabajo,
            ST_X(residencia) AS lon_residencia, ST_Y(residencia) AS lat_residencia,
            ST_X(trabajo) AS lon_trabajo, ST_Y(trabajo) AS lat_trabajo,
            ST_Distance_Sphere(residencia, trabajo) AS distancia_residencia_trabajo
        FROM Estudiantes
    ''')
    estudiantes = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(estudiantes)

if __name__ == '__main__':
    app.run(debug=True)
