from flask import Flask, request, jsonify
import mysql.connector
import os
import time

app = Flask(__name__)


# ==============================
# MySQL Configuration
# ==============================

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_NAME = os.getenv("DB_NAME", "todo")


# ==============================
# Database Connection
# ==============================

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


# ==============================
# Initialize Database
# ==============================

def init_db():

    for attempt in range(10):

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    task VARCHAR(255) NOT NULL
                )
            """)

            connection.commit()

            cursor.close()
            connection.close()

            print("Database initialized successfully")
            return

        except mysql.connector.Error as error:

            print(f"Database connection failed: {error}")
            print("Retrying in 5 seconds...")

            time.sleep(5)

    raise Exception("Could not connect to MySQL")


# ==============================
# Get All Tasks
# GET /api/tasks
# ==============================

@app.route("/api/tasks", methods=["GET"])
def get_tasks():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, task FROM tasks ORDER BY id"
    )

    tasks = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(tasks)


# ==============================
# Add Task
# POST /api/add
# ==============================

@app.route("/api/add", methods=["POST"])
def add_task():

    data = request.get_json()

    if not data or "task" not in data:
        return jsonify({
            "error": "Task is required"
        }), 400

    task = data["task"].strip()

    if not task:
        return jsonify({
            "error": "Task cannot be empty"
        }), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO tasks (task) VALUES (%s)",
        (task,)
    )

    connection.commit()

    task_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return jsonify({
        "id": task_id,
        "task": task
    }), 201


# ==============================
# Delete Task
# DELETE /api/delete/<id>
# ==============================

@app.route("/api/delete/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id = %s",
        (task_id,)
    )

    connection.commit()

    rows_deleted = cursor.rowcount

    cursor.close()
    connection.close()

    if rows_deleted == 0:
        return jsonify({
            "error": "Task not found"
        }), 404

    return jsonify({
        "message": "Task deleted successfully"
    })


# ==============================
# Application Startup
# ==============================

if __name__ == "__main__":

    init_db()

    app.run(
        host="0.0.0.0",
        port=5000
    )