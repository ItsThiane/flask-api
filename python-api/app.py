from flask import Flask, request, jsonify
from database import get_db_connection
import mysql.connector



app = Flask(__name__)



@app.route('/')
def hello_world():
    return "Bienvenue sur l'API de gestion des tâches Taskmap!"


#Tasks

# Endpoint pour ajouter une tache
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    description = data.get('description')
    user_id = data.get('user_id')

    if not description or not user_id:
        return jsonify({"error": "Description and user_id are required"}), 400

    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO tasks (description, user_id) VALUES (%s, %s)",
            (description, user_id)
        )    
        db.comit()
        return jsonify({"message": "Task added successfully", "task_id": cursor.lastrowid}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    finally:
        cursor.close()


# Endpoint pour lister toutes les tâches d’un utilisateur
@app.route('/users/<int:user_id>/tasks', methods=['GET'])
def get_user_tasks(user_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
    tasks = cursor.fetchall()
    cursor.close()
    return jsonify(tasks)

#  Endpoint pour mettre à jour une tâche
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    db = get_db_connection()
    data = request.json
    status = data.get('status')
    
    if not status:
        return jsonify({"error": "Status is required"}), 400
    
    cursor = db.cursor()
    try:
        cursor.execute("UPDATE tasks SET status = %s WHERE id = %s", (status, task_id))
        db.commit()
        return jsonify({"message": "Task updated successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    finally:
        cursor.close()

# Endpoint pour supprimer une tâche
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        db.commit()
        return jsonify({"message": "Task deleted successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    finally:
        cursor.close()   




#Utilisateurs

# Endpoint pour creer un utilisateur
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({"error": " Name and email are required"}), 400

    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        db.commit()
        return jsonify({"message": "User added successfully", "user_id": cursor.lastrowid}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    finally:
        cursor.close()


#3. Endpoint pour lister tous les utilisateurs
@app.route('/users', methods=['GET'])
def get_users():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    return jsonify(users)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
