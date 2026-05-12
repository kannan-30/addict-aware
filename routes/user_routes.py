"""
Antigravity - Addict Aware
User Routes: Dashboard, Assessment, Progress, Feedback, PDF Download
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from database.db import get_db
from models.ml_model import predict_addiction
from utils.nlp_engine import analyze_sentiment
from utils.pdf_generator import generate_progress_report
from bson import ObjectId
from datetime import datetime

user_bp = Blueprint('user', __name__)


@user_bp.route('/dashboard')
@jwt_required()
def dashboard():
    """User dashboard with latest results and progress"""
    db = get_db()
    claims = get_jwt()
    user_id = get_jwt_identity()

    # Get user info
    user = db.users.find_one({'_id': ObjectId(user_id)})
    if not user or user['role'] != 'user':
        flash('Access denied.', 'danger')
        return redirect(url_for('auth.login'))

    # Get assessments (latest first)
    assessments = list(db.assessments.find(
        {'user_id': user_id}
    ).sort('created_at', -1).limit(20))

    # Get tips for user's current level
    latest_level = assessments[0]['addiction_level'].lower() if assessments else 'low'
    tips = list(db.health_tips.find({'category': latest_level}).limit(4))

    # Calculate streak (days with assessments)
    streak = 0
    if assessments:
        from datetime import timedelta
        check_date = datetime.utcnow().date()
        for a in assessments:
            a_date = a['created_at'].date() if isinstance(a['created_at'], datetime) else check_date
            if a_date == check_date or a_date == check_date - timedelta(days=1):
                streak += 1
                check_date = a_date - timedelta(days=1)
            else:
                break

    return render_template('dashboard.html',
                           user=user,
                           assessments=assessments,
                           tips=tips,
                           streak=streak,
                           claims=claims)


@user_bp.route('/assessment', methods=['GET', 'POST'])
@jwt_required()
def assessment():
    """Addiction assessment form and prediction"""
    if request.method == 'POST':
        db = get_db()
        user_id = get_jwt_identity()

        try:
            screen_time = float(request.form.get('screen_time', 0))
            phone_pickups = int(request.form.get('phone_pickups', 0))
            social_media_time = float(request.form.get('social_media_time', 0))
            emotional_text = request.form.get('emotional_text', '').strip()
        except (ValueError, TypeError):
            flash('Please enter valid numbers.', 'danger')
            return render_template('assessment.html')

        # Validate inputs
        if screen_time < 0 or phone_pickups < 0 or social_media_time < 0:
            flash('Values cannot be negative.', 'danger')
            return render_template('assessment.html')

        # ML Prediction
        prediction = predict_addiction(screen_time, phone_pickups, social_media_time)

        # NLP Sentiment Analysis
        sentiment = analyze_sentiment(emotional_text)

        # Store assessment
        assessment_doc = {
            'user_id': user_id,
            'screen_time': screen_time,
            'phone_pickups': phone_pickups,
            'social_media_time': social_media_time,
            'emotional_text': emotional_text,
            'addiction_level': prediction['addiction_level'],
            'addiction_score': prediction['addiction_score'],
            'probabilities': prediction['probabilities'],
            'sentiment': sentiment['sentiment'],
            'sentiment_score': sentiment['compound_score'],
            'emotion': sentiment['emotion'],
            'sentiment_explanation': sentiment.get('brief_explanation', ''),
            'created_at': datetime.utcnow()
        }
        db.assessments.insert_one(assessment_doc)

        flash('Assessment completed successfully!', 'success')
        return redirect(url_for('user.results', level=prediction['addiction_level'],
                                score=prediction['addiction_score'],
                                sentiment=sentiment['sentiment'],
                                emotion=sentiment['emotion'],
                                explanation=sentiment.get('brief_explanation', '')))

    return render_template('assessment.html')


@user_bp.route('/results')
@jwt_required()
def results():
    """Display assessment results"""
    db = get_db()
    level = request.args.get('level', 'Low')
    score = request.args.get('score', 0)
    sentiment = request.args.get('sentiment', 'Neutral')
    emotion = request.args.get('emotion', '😐 Neutral')
    explanation = request.args.get('explanation', '')

    # Get tips for this level
    tips = list(db.health_tips.find({'category': level.lower()}).limit(4))

    return render_template('results.html',
                           level=level,
                           score=score,
                           sentiment=sentiment,
                           emotion=emotion,
                           explanation=explanation,
                           tips=tips)


@user_bp.route('/progress')
@jwt_required()
def progress():
    """View progress history"""
    db = get_db()
    user_id = get_jwt_identity()

    assessments = list(db.assessments.find(
        {'user_id': user_id}
    ).sort('created_at', -1))

    return render_template('progress.html', assessments=assessments)


@user_bp.route('/download-report')
@jwt_required()
def download_report():
    """Download PDF progress report"""
    db = get_db()
    user_id = get_jwt_identity()
    user = db.users.find_one({'_id': ObjectId(user_id)})

    assessments = list(db.assessments.find({'user_id': user_id}).sort('created_at', -1))

    latest_level = assessments[0]['addiction_level'].lower() if assessments else 'low'
    tips = list(db.health_tips.find({'category': latest_level}))

    buffer = generate_progress_report(user['name'], assessments, tips)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"progress_report_{user['name']}_{datetime.now().strftime('%Y%m%d')}.pdf",
        mimetype='application/pdf'
    )


@user_bp.route('/feedback', methods=['GET', 'POST'])
@jwt_required()
def feedback():
    """Submit feedback"""
    if request.method == 'POST':
        db = get_db()
        user_id = get_jwt_identity()

        message = request.form.get('message', '').strip()
        rating = int(request.form.get('rating', 3))

        if not message:
            flash('Feedback message is required.', 'danger')
            return render_template('feedback.html')

        db.feedback.insert_one({
            'user_id': user_id,
            'message': message,
            'rating': rating,
            'sentiment': analyze_sentiment(message)['sentiment'],
            'created_at': datetime.utcnow()
        })

        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('user.dashboard'))

    return render_template('feedback.html')


@user_bp.route('/tips')
@jwt_required()
def tips():
    """View health tips"""
    db = get_db()
    all_tips = list(db.health_tips.find())
    return render_template('tips.html', tips=all_tips)


# API endpoints for Chart.js
@user_bp.route('/api/progress-data')
@jwt_required()
def progress_data():
    """API: Get progress data for charts"""
    db = get_db()
    user_id = get_jwt_identity()

    assessments = list(db.assessments.find(
        {'user_id': user_id}
    ).sort('created_at', 1).limit(30))

    labels = []
    scores = []
    screen_times = []
    sentiments = []

    for a in assessments:
        date = a['created_at'].strftime('%m/%d') if isinstance(a['created_at'], datetime) else ''
        labels.append(date)
        scores.append(a.get('addiction_score', 0))
        screen_times.append(a.get('screen_time', 0))
        sentiments.append(a.get('sentiment_score', 0))

    return jsonify({
        'labels': labels,
        'scores': scores,
        'screen_times': screen_times,
        'sentiments': sentiments
    })
