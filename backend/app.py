from flask import Flask, request, jsonify

app = Flask(__name__)

tasks = []

@app.route("/tasks")
def get_tasks():
    return jsonify(tasks)

@app.route("/add", methods=["POST"])
def add_task():
    data = request.get_json()

    if data and data.get("task"):
        tasks.append(data["task"])

    return jsonify({"message": "Task added"})

@app.route("/delete/<int:index>", methods=["DELETE"])
def delete_task(index):
    if 0 <= index < len(tasks):
        tasks.pop(index)

    return jsonify({"message": "Task deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)