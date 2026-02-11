import torch  # Fix for WinError 1114 DLL initialization
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from generator_service import QuestionGenerator
import os

app = Flask(__name__)
app.secret_key = "exam_secret_key" # In production, use a secure key

generator = QuestionGenerator()

# In-memory store for active exam (for simplicity)
active_exam = {
    "subject": None,
    "subject": None,
    "topics": [],
    "difficulty": "medium",
    "is_active": False
}

@app.route('/')
def home():
    return render_template('index.html', active_exam=active_exam)

@app.route('/login', methods=['POST'])
def do_login():
    prn = request.form.get('prn')
    if prn:
        session['prn'] = prn
        session['exam_history'] = []
        session['current_index'] = -1
        return redirect(url_for('take_test'))
    return redirect(url_for('student_login'))

@app.route('/test')
def take_test():
    if not session.get('prn'):
        return redirect(url_for('student_login'))
    
    if not active_exam["is_active"]:
        return redirect(url_for('student_login'))

    # Initialize history if missing (safe guard)
    if 'exam_history' not in session:
        session['exam_history'] = []
        session['current_index'] = -1

    history = session['exam_history']
    current_index = session.get('current_index', -1)
    
    action = request.args.get('action')

    if action == 'next':
        current_index += 1
    elif action == 'prev':
        current_index = max(0, current_index - 1)
    elif action == 'submit':
        return redirect(url_for('submit_exam'))
    
    # If we need a new question (start or next past end)
    if current_index >= len(history) or current_index == -1:
        # Generate new question
        question_data = generator.generate(
            active_exam["subject"],
            active_exam["topics"],
            active_exam["difficulty"]
        )
        history.append(question_data)
        current_index = len(history) - 1
        session['exam_history'] = history
    
    session['current_index'] = current_index
    
    current_question = history[current_index]
    
    return render_template('student_test.html', 
                          question_data=current_question, 
                          prn=session['prn'],
                          current_index=current_index,
                          total_questions=len(history))

@app.route('/submit')
def submit_exam():
    session.clear()
    # You might want a specific 'completed' page, for now redirect to login
    return render_template('waiting.html') # Or a "Test Submitted" page

@app.route('/examiner')
def examiner_dashboard():
    subjects = generator.get_subjects()
    return render_template('examiner.html', subjects=subjects, active_exam=active_exam)

@app.route('/api/topics/<subject>')
def get_topics(subject):
    topics = generator.get_topics(subject)
    return jsonify(topics)

@app.route('/api/set_exam', methods=['POST'])
def set_exam():
    data = request.json
    active_exam["subject"] = data.get('subject')
    active_exam["topics"] = data.get('topics')  # Expecting a list now
    active_exam["difficulty"] = data.get('difficulty')
    active_exam["is_active"] = True
    return jsonify({"status": "success"})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('student_login'))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5000)
