import os
import openai
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from config import Config
from models import db, User, Scholarship, ExamResource, CareerPath
from forms import SetupForm

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
openai.api_key = app.config['OPENAI_API_KEY']

# Create database tables
with app.app_context():
    db.create_all()
    # Insert sample data if not exists
    if not Scholarship.query.first():
        sample_scholarships = [
            Scholarship(
                name="National Merit Scholarship",
                eligibility="High school students with exceptional PSAT scores",
                deadline="2023-12-31",
                link="https://example.com/nms",
                academic_level="high_school"
            ),
            # Add more sample scholarships...
        ]
        db.session.bulk_save_objects(sample_scholarships)
        db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' in session:
        return redirect(url_for('chat'))
    return render_template('index.html')

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    form = SetupForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            academic_level=form.academic_level.data,
            interests=form.interests.data
        )
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        return redirect(url_for('chat'))
    return render_template('setup.html', form=form)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('chat.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json['message']
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({'response': 'Please complete the setup first.'})
    
    user = User.query.get(user_id)
    
    # Determine intent
    intent = determine_intent(user_message)
    
    # Prepare context data
    context = get_context_data(intent, user)
    
    # Generate response using OpenAI
    response = generate_chat_response(user_message, context)
    
    return jsonify({'response': response})

def determine_intent(message):
    message = message.lower()
    scholarship_keywords = ['scholarship', 'funding', 'financial aid']
    exam_keywords = ['exam', 'test', 'prepare', 'study']
    career_keywords = ['career', 'job', 'future', 'major']
    
    if any(kw in message for kw in scholarship_keywords):
        return 'scholarship'
    elif any(kw in message for kw in exam_keywords):
        return 'exam'
    elif any(kw in message for kw in career_keywords):
        return 'career'
    return 'general'

def get_context_data(intent, user):
    context = f"Student Info: {user.name}, {user.academic_level} student interested in {user.interests}.\n"
    
    if intent == 'scholarship':
        scholarships = Scholarship.query.filter_by(academic_level=user.academic_level).all()
        context += "Available Scholarships:\n"
        for s in scholarships:
            context += f"- {s.name}: {s.eligibility} (Deadline: {s.deadline}, Link: {s.link})\n"
    
    elif intent == 'exam':
        exams = ExamResource.query.all()
        context += "Exam Resources:\n"
        for e in exams:
            context += f"- {e.exam_name}: {e.preparation_tips} (Books: {e.recommended_books}, Website: {e.website})\n"
    
    elif intent == 'career':
        careers = CareerPath.query.all()
        context += "Career Paths:\n"
        for c in careers:
            context += f"- {c.field}: {c.description} (Skills: {c.required_skills}, Avg Salary: {c.average_salary})\n"
    
    return context

def generate_chat_response(user_message, context):
    system_message = (
        f"You are a friendly AI career counselor. Use the following context to help the student:\n"
        f"{context}\n"
        "Provide concise, helpful responses. If you don't know something, suggest they ask more specifically."
    )
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )
        return response.choices[0].message['content']
    except Exception as e:
        return "Sorry, I'm having trouble connecting to the knowledge base. Please try again later."

if __name__ == '__main__':
    app.run(debug=True)