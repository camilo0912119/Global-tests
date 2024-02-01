from flask import Flask, jsonify, request

# Crea una instancia de la aplicación Flask
app = Flask(__name__)

# Inicializa una lista de "tables" con información sobre diferentes tablas de datos
tables = [
    {
        'name': 'departments',
        'source_file': 'C:/Users/jerodrod/Downloads/data_challenge_files/departments.csv',
        'description': 'Information about departments from a company',
        'nrows': 1
    },
    {
        'name': 'jobs',
        'source_file': 'C:/Users/jerodrod/Downloads/data_challenge_files/jobs.csv',
        'description': 'Information about jobs from a company',
        'nrows': 1
    },
    {
        'name': 'hired_employees',
        'source_file': 'C:/Users/jerodrod/Downloads/data_challenge_files/hired_employees.csv',
        'description': 'Information about hiring processes from a company',
        'nrows': 1
    }
]

# Define una ruta para obtener la lista de "tables"
@app.route('/tables', methods=['GET'])
def get_tables():
    return jsonify({'tables': tables})

# Define una ruta para crear una nueva "table"
@app.route('/tables', methods=['POST'])
def create_table():
    # Obtiene la información de la nueva "table" desde la solicitud JSON
    new_table = {
        'name': request.json['name'],
        'source_file': request.json['source_file'],
        'description': request.json['description'],
        'nrows': request.json['nrows']
    }
    # Agrega la nueva "table" a la lista de "tables"
    tables.append(new_table)
    return jsonify({'table': new_table})

# Define una ruta para obtener detalles de una "table" específica por nombre
@app.route('/tables/<string:name>', methods=['GET'])
def get_table(name):
    # Busca la "table" por nombre en la lista de "tables"
    table = [table for table in tables if table['name'] == name]
    if len(table) == 0:
        return jsonify({'error': 'Table not found'})
    return jsonify({'exist': True})

# Define una ruta para actualizar una "table" existente por nombre
@app.route('/tables/<string:name>', methods=['PUT'])
def update_table(name):
    # Busca la "table" por nombre en la lista de "tables"
    table = [table for table in tables if table['name'] == name]
    if len(table) == 0:
        return jsonify({'error': 'Table not found'})
    # Actualiza los campos de la "table" con la información de la solicitud JSON
    table[0]['name'] = request.json.get('name', table[0]['name'])
    table[0]['source_file'] = request.json.get('source_file', table[0]['source_file'])
    table[0]['description'] = request.json.get('description', table[0]['description'])
    table[0]['nrows'] = request.json.get('nrows', table[0]['nrows'])
    return jsonify({'table': table[0]})

# Define una ruta para eliminar una "table" por nombre
@app.route('/tables/<string:name>', methods=['DELETE'])
def delete_table(name):
    # Busca la "table" por nombre en la lista de "tables"
    table = [table for table in tables if table['name'] == name]
    if len(table) == 0:
        return jsonify({'error': 'Table not found'})
    # Elimina la "table" de la lista de "tables"
    tables.remove(table[0])
    return jsonify({'result': 'Table deleted'})

# Ejecuta la aplicación si este script es el programa principal
if __name__ == '__main__':
    app.run(debug=True)
