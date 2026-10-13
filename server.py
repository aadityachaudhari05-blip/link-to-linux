from flask import Flask, jsonify, render_template_string
from datetime import datetime, timezone
import socket

app = Flask(__name__)
started_at = datetime.now(timezone.utc).isoformat()


@app.route("/")
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Link to Linux</title>
        <style>
            body {
                font-family: sans-serif;
                text-align: center;
                padding: 40px 20px;
                background: #111827;
                color: white;
            }
            .card {
                max-width: 420px;
                margin: 40px auto;
                padding: 30px;
                border-radius: 18px;
                background: #1f2937;
            }
            .status {
                color: #4ade80;
                font-size: 20px;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🐧 Link to Linux</h1>
            <p class="status">✓ Phone connected!</p>
            <p>Your phone can reach your Linux computer.</p>
            <p>Connection test successful.</p>
        </div>
    </body>
    </html>
    """)


@app.route("/pair")
def pair():
    return home()


@app.route("/health")
def health():
    return jsonify({
        "app": "Link to Linux",
        "status": "online",
        "started_at": started_at
    })


if __name__ == "__main__":
    print("Link to Linux server starting...", flush=True)
    print("Waiting for your phone...", flush=True)

    app.run(
        host="0.0.0.0",
        port=8765,
        debug=False
    )
