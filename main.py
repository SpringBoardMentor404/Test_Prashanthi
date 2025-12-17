from flask import Flask, request, jsonify
from flasgger import Swagger
import json

# Create the Flask application instance
app = Flask(__name__)

# Load Swagger (OpenAPI) template from workspace file `swagger.json`.
# Flasgger will use this template to render the Swagger UI at /apidocs by default.
with open("swagger.json") as f:
    swagger_template = json.load(f)

# Initialize Flasgger with the loaded template
swagger = Swagger(app, template=swagger_template)

# -----------------------------------------------------------------------------
# Route: GET /api/users
# Purpose: Return a static list of users for demonstration and tests.
# Notes: In a real app this would query a database or service.
# -----------------------------------------------------------------------------
@app.route("/api/users", methods=["GET"])
def get_users():
    """
    Return a static list of user objects.
    Response: 200 OK, JSON array of users.
    """
    users = [
        {"id": 1, "name": "John Doe", "email": "john@example.com"},
        {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
    ]
    return jsonify(users), 200

# -----------------------------------------------------------------------------
# Route: POST /api/users
# Purpose: Create a new user from JSON payload.
# Expected body: {"name": "<str>", "email": "<str>"}
# Responses:
#   201 Created -> returns created user object
#   400 Bad Request -> missing name or email
# -----------------------------------------------------------------------------
@app.route("/api/users", methods=["POST"])
def create_user():
    """
    Create a new user from the provided JSON body.
    Validates presence of 'name' and 'email'.
    """
    data = request.get_json()

    # Basic validation: ensure payload is present and contains required fields.
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "Name and email required"}), 400

    # NOTE: Using current time as a simple integer id for demo/testing only.
    # In production, use a proper ID generator or database-assigned id.
    new_user = {
        "id": int(__import__("time").time()),
        "name": name,
        "email": email
    }

    return jsonify(new_user), 201

# -----------------------------------------------------------------------------
# Route: GET /api/users/<user_id>
# Purpose: Return a mocked user object for the given user_id.
# Notes: This is a stub returning a predictable object for testing.
# -----------------------------------------------------------------------------
@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    """
    Return a mocked user object for the provided user_id.
    Response: 200 OK, JSON object.
    """
    user = {
        "id": user_id,
        "name": "John Doe",
        "email": f"user{user_id}@example.com"
    }
    return jsonify(user), 200

# -----------------------------------------------------------------------------
# Application entrypoint
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # Run Flask development server on port 3000 with debug enabled.
    app.run(debug=True, port=3000)
