from flask import Flask, jsonify
import os
import psycopg2

app = Flask(__name__)


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "postgres"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "demo"),
        user=os.getenv("DB_USER", "demo"),
        password=os.getenv("DB_PASSWORD", "demo123")
    )


@app.route("/")
def home():
    return jsonify({
        "message": "DevOps Kubernetes Challenge",
        "status": "running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/ready")
def ready():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({
            "status": "ready",
            "database": "connected"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "not ready",
            "database": "disconnected",
            "error": str(e)
        }), 503


@app.route("/api/db")
def database():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT current_database();")
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        return jsonify({
            "database": result[0],
            "status": "connected"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
