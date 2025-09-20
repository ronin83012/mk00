from flask import Flask, send_from_directory, render_template, request, abort
import logging
import os
from pathlib import Path

app = Flask(__name__, static_folder='static', template_folder='templates')

# Logging config
logging.basicConfig(filename='downloads.log', level=logging.INFO, format='%(asctime)s %(message)s')

# File you already have (place inside static/)
EXE_FILENAME = "BOMB.exe"   # <-- rename to your real exe filename located in static/

@app.route("/")
def index():
    # optionally compute checksum to inject into template (safer to compute once and paste)
    return render_template("index.html")

@app.route("/download")
def download():
    static_dir = Path(app.static_folder)
    filepath = static_dir / EXE_FILENAME
    if not filepath.exists():
        abort(404)

    # Basic audit log
    ip = request.remote_addr
    ua = request.headers.get("User-Agent", "unknown")
    logging.info(f"DOWNLOAD REQUEST - file={EXE_FILENAME} ip={ip} ua={ua}")

    # send the file as an attachment so browser prompts Save/Open
    return send_from_directory(directory=static_dir, path=EXE_FILENAME, as_attachment=True)

if __name__ == "__main__":
    # In production run behind a proper WSGI server with TLS.
    app.run(host="0.0.0.0", port=5000)
