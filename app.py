import os
import sqlite3
import uuid
import threading
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from worker import process_jobs

# --- Configuration ---
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
DATABASE = 'jobs.db'
ALLOWED_EXTENSIONS = {'xlsx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Worker state tracking
worker_running = False

# --- Database Helpers ---
def get_db():
    try:
        db = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        return db
    except sqlite3.Error as e:
        raise RuntimeError(f"Database connection failed: {e}")

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        # Add logs column if it doesn't exist
        try:
            db.execute('ALTER TABLE jobs ADD COLUMN logs TEXT DEFAULT ""')
        except sqlite3.OperationalError:
            pass  # Column already exists
        db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(Flask, '_database', None)
    if db is not None:
        db.close()

# --- File Helpers ---
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Routes ---
@app.route('/', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(url_for('upload_page'))
        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            return redirect(url_for('upload_page'))
        
        if file:
            job_id = str(uuid.uuid4())
            filename = f"{job_id}.xlsx"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # Validate path to prevent traversal
            if not os.path.abspath(filepath).startswith(os.path.abspath(app.config['UPLOAD_FOLDER'])):
                return "Invalid file path", 400
            file.save(filepath)
            
            db = get_db()
            db.execute('INSERT INTO jobs (id, status, input_file) VALUES (?, ?, ?)', 
                       (job_id, 'PENDING', filepath))
            db.commit()
            
            # Start worker in background thread if not already running
            global worker_running
            if not worker_running:
                worker_running = True
                threading.Thread(target=process_jobs, daemon=True).start()
            
            return redirect(url_for('status_page', job_id=job_id))
            
    return render_template('index.html')

@app.route('/status/<job_id>')
def status_page(job_id):
    db = get_db()
    job = db.execute('SELECT * FROM jobs WHERE id = ?', (job_id,)).fetchone()
    
    if not job:
        return "Job not found", 404
        
    return render_template('index.html', job=job)

@app.route('/download/<job_id>')
def download_zip(job_id):
    try:
        db = get_db()
        job = db.execute('SELECT * FROM jobs WHERE id = ? AND status = ?', (job_id, 'COMPLETED')).fetchone()
        
        if not job:
            return "Job not ready or not found.", 404

        return send_from_directory(
            app.config['OUTPUT_FOLDER'],
            os.path.basename(job['output_file']),
            as_attachment=True
        )
    except (sqlite3.Error, FileNotFoundError, OSError) as e:
        return f"Download failed: {str(e)}", 500

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    # Initialize DB if missing
    if not os.path.exists(DATABASE):
        init_db()
        
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0' if os.environ.get('PORT') else '127.0.0.1'
    app.run(host=host, port=port)