from flask import Flask, request, jsonify, render_template, session, redirect, url_for, make_response
from flask_cors import CORS
import database as db
import model as ml
from auth import auth
from functools import wraps

# Safe imports — won't crash if these fail
try:
    from pdf_report import generate_pdf
    PDF_ENABLED = True
except Exception as e:
    print(f"PDF disabled: {e}")
    PDF_ENABLED = False

try:
    from mailer import send_result_email
    MAIL_ENABLED = True
except Exception as e:
    print(f"Email disabled: {e}")
    MAIL_ENABLED = False

app = Flask(__name__)
app.secret_key = 'loan_app_secret_key_2024'
CORS(app)
db.init_db()
app.register_blueprint(auth)

# ── DECORATORS ───────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        if not session.get('is_admin'):
            return jsonify({'success': False, 'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated

# ── PAGES ────────────────────────────────────────────────────
@app.route('/')
@login_required
def index():
    return render_template('index.html',
                           username=session.get('username'),
                           is_admin=session.get('is_admin'))

@app.route('/admin')
@login_required
def admin():
    if not session.get('is_admin'):
        return redirect(url_for('index'))
    return render_template('admin.html', username=session.get('username'))

# ── PREDICTION ───────────────────────────────────────────────
@app.route('/api/predict', methods=['POST'])
@login_required
def predict():
    try:
        data = request.get_json()
        data['user_id'] = session['user_id']
        result = ml.predict(data)
        db.save_prediction(data, result)
        email = data.get('email', '').strip()
        if email and MAIL_ENABLED:
            try:
                send_result_email(email, data.get('name', 'Applicant'), result)
            except Exception as mail_err:
                print(f"Email skipped: {mail_err}")
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
@login_required
def history():
    user_id = None if session.get('is_admin') else session['user_id']
    rows = db.get_history(user_id=user_id)
    return jsonify({'success': True, 'data': rows})

@app.route('/api/stats', methods=['GET'])
@login_required
def stats():
    user_id = None if session.get('is_admin') else session['user_id']
    return jsonify({'success': True, 'data': db.get_stats(user_id=user_id)})

@app.route('/api/train', methods=['POST'])
@login_required
def train():
    acc = ml.train_model()
    return jsonify({'success': True, 'accuracy': acc})

# ── PDF DOWNLOAD ─────────────────────────────────────────────
@app.route('/api/download-pdf', methods=['POST'])
@login_required
def download_pdf():
    if not PDF_ENABLED:
        return jsonify({'success': False, 'error': 'PDF not available'}), 503
    try:
        body       = request.get_json()
        input_data = body.get('input_data', {})
        result     = body.get('result', {})
        pdf_bytes  = generate_pdf(input_data, result)
        response   = make_response(pdf_bytes)
        response.headers['Content-Type'] = 'application/pdf'
        fname = input_data.get('name', 'applicant').replace(' ', '_')
        response.headers['Content-Disposition'] = f'attachment; filename=LoanPro_Report_{fname}.pdf'
        return response
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ── ADMIN API ─────────────────────────────────────────────────
@app.route('/api/admin/users', methods=['GET'])
@admin_required
def admin_users():
    return jsonify({'success': True, 'data': db.get_all_users()})

@app.route('/api/admin/users/<int:uid>', methods=['DELETE'])
@admin_required
def delete_user(uid):
    if uid == session['user_id']:
        return jsonify({'success': False, 'error': 'Cannot delete yourself'}), 400
    db.delete_user(uid)
    return jsonify({'success': True})

@app.route('/api/admin/stats', methods=['GET'])
@admin_required
def admin_stats():
    return jsonify({'success': True, 'data': db.get_stats()})

if __name__ == '__main__':
    app.run(debug=True, port=5000)