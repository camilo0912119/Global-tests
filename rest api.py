from flask import Flask, jsonify, request
from fuctions_sql import create_table_from_df,select_all,update_table_from_df,delete_table
import pandas as pd
# Crea una instancia de la aplicación Flask
app = Flask(__name__)

# Inicializa una lista de "tables" con información sobre diferentes tablas de datos
tables = [
    {
        'name': 'departments',
        'source_file': 'C:/Users/jerodrod/Downloads/data_challenge_files/departments.csv',
        'description': 'Information about departments from a company',
        'nrows': 1,
        'all_rows':False
    },
    {
        'name': 'jobs',
        'source_file': 'C:/Users/jerodrod/Downloads/data_challenge_files/jobs.csv',
        'description': 'Information about jobs from a company',
        'nrows': 1,
        'all_rows':False
    },
    {
        'name': 'hired_employees',
        'source_file': 'C:/Users/jerodrod/Downloads/data_challenge_files/hired_employees.csv',
        'description': 'Information about hiring processes from a company',
        'nrows': 1,
        'all_rows':False
    }
]
##Creamos todas las tablas por defecto
for table in tables:
    if table['all_rows']:    
        df=pd.read_csv(table['source_file'],sep=',')
    else:
        df=pd.read_csv(table['source_file'],sep=',',nrows=table['nrows'])
    create_table_from_df(df, table['name'], database_name='my_database.db')        
# Define una ruta para obtener la lista de "tables"
@app.route('/tables', methods=['GET'])
def get_tables():
    values=[]
    for table in tables:
        value=select_all(table['name'], database_name='my_database.db')
        values.append(value.to_json())
    return jsonify({'tables': tables, 'data':values})
# Define una ruta para crear una nueva "table"
@app.route('/tables', methods=['POST'])
def create_table():
    # Obtiene la información de la nueva "table" desde la solicitud JSON
    new_table = {
        'name': request.json['name'],
        'source_file': request.json['source_file'],
        'description': request.json['description'],
        'nrows': request.json['nrows'],
        'all_rows':True
    }
    # Agrega la nueva "table" a la lista de "tables"
    if new_table['all_rows']:    
        df=pd.read_csv(new_table['source_file'],sep=',')
    else:
        df=pd.read_csv(new_table['source_file'],sep=',',nrows=table['nrows'])
    create_table_from_df(df, new_table['name'], database_name='my_database.db')
    tables.append(new_table)
    return jsonify({'table': new_table})

# Define una ruta para obtener detalles de una "table" específica por nombre
@app.route('/tables/<string:name>', methods=['GET'])
def get_table(name):
    # Busca la "table" por nombre en la lista de "tables"
    table = [table for table in tables if table['name'] == name]
    if len(table) == 0:
        return jsonify({'error': 'Table not found'})
    data=select_all(table[0]['name'], database_name='my_database.db')
    return jsonify({'exist': True,'data':data.to_json()})
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
    table[0]['all_rows'] = request.json.get('all_rows', table[0]['all_rows'])
    if table[0]['all_rows']:    
        df=pd.read_csv(table[0]['source_file'],sep=',')
    else:
        df=pd.read_csv(table[0]['source_file'],sep=',',nrows=table[0]['nrows']) 
    update_table_from_df(df, table[0]['name'], database_name='my_database.db')
    return jsonify({'table': table[0]})

# Define una ruta para eliminar una "table" por nombre
@app.route('/tables/<string:name>', methods=['DELETE'])
def delete_table_r(name):
    # Busca la "table" por nombre en la lista de "tables"
    table = [table for table in tables if table['name'] == name]
    if len(table) == 0:
        return jsonify({'error': 'Table not found'})
    # Elimina la "table" de la lista de "tables"
    tables.remove(table[0])
    delete_table(table[0]['name'], database_name='my_database.db')
    return jsonify({'result': 'Table deleted'})

# Ejecuta la aplicación si este script es el programa principal
if __name__ == '__main__':
    app.run(debug=True)
