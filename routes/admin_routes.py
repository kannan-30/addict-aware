"""
Antigravity - Addict Aware
Admin Routes: Dashboard, User Management, Content Manager, ML Panel
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from database.db import get_db
from models.ml_model import train_model, get_model_info
from utils.nlp_engine import analyze_sentiment, get_sentiment_summary
from bson import ObjectId
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(fn):
    """Decorator to check admin role"""
    from functools import wraps

    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get('role') != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('auth.login'))
        return fn(*args, **kwargs)

    return wrapper


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Admin dashboard with KPIs and analytics"""
    db = get_db()

    # KPI Stats
    total_users = db.users.count_documents({'role': 'user'})
    total_assessments = db.assessments.count_documents({})
    total_feedback = db.feedback.count_documents({})

    # Addiction distribution
    pipeline_addiction = [
        {'$group': {'_id': '$addiction_level', 'count': {'$sum': 1}}}
    ]
    addiction_dist = {d['_id']: d['count'] for d in db.assessments.aggregate(pipeline_addiction)}

    # Sentiment distribution
    pipeline_sentiment = [
        {'$group': {'_id': '$sentiment', 'count': {'$sum': 1}}}
    ]
    sentiment_dist = {d['_id']: d['count'] for d in db.assessments.aggregate(pipeline_sentiment)}

    # Recent assessments
    recent_assessments = list(db.assessments.aggregate([
        {'$sort': {'created_at': -1}},
        {'$limit': 10},
        {'$lookup': {
            'from': 'users',
            'let': {'uid': {'$toObjectId': '$user_id'}},
            'pipeline': [{'$match': {'$expr': {'$eq': ['$_id', '$$uid']}}}],
            'as': 'user_info'
        }},
        {'$unwind': {'path': '$user_info', 'preserveNullAndEmptyArrays': True}}
    ]))

    # Average addiction score
    avg_pipeline = [{'$group': {'_id': None, 'avg_score': {'$avg': '$addiction_score'}}}]
    avg_result = list(db.assessments.aggregate(avg_pipeline))
    avg_score = round(avg_result[0]['avg_score'], 1) if avg_result else 0

    # Recent feedback
    recent_feedback = list(db.feedback.find().sort('created_at', -1).limit(5))

    # Model info
    model_info = get_model_info()

    return render_template('admin_dashboard.html',
                           total_users=total_users,
                           total_assessments=total_assessments,
                           total_feedback=total_feedback,
                           addiction_dist=addiction_dist,
                           sentiment_dist=sentiment_dist,
                           recent_assessments=recent_assessments,
                           avg_score=avg_score,
                           recent_feedback=recent_feedback,
                           model_info=model_info)


@admin_bp.route('/users')
@admin_required
def manage_users():
    """View and manage users"""
    db = get_db()
    users = list(db.users.find({'role': 'user'}).sort('created_at', -1))

    # Add assessment count for each user
    for user in users:
        user['assessment_count'] = db.assessments.count_documents({'user_id': str(user['_id'])})

    return render_template('admin_users.html', users=users)


@admin_bp.route('/users/delete/<user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    """Delete a user and their data"""
    db = get_db()
    db.users.delete_one({'_id': ObjectId(user_id)})
    db.assessments.delete_many({'user_id': user_id})
    db.feedback.delete_many({'user_id': user_id})
    flash('User deleted successfully.', 'success')
    return redirect(url_for('admin.manage_users'))


@admin_bp.route('/content', methods=['GET', 'POST'])
@admin_required
def content_manager():
    """Manage health tips / awareness content"""
    db = get_db()

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        category = request.form.get('category', 'low')

        if title and content:
            db.health_tips.insert_one({
                'title': title,
                'content': content,
                'category': category,
                'created_at': datetime.utcnow()
            })
            flash('Health tip added!', 'success')
        else:
            flash('Title and content are required.', 'danger')

        return redirect(url_for('admin.content_manager'))

    tips = list(db.health_tips.find().sort('created_at', -1))
    return render_template('admin_content.html', tips=tips)


@admin_bp.route('/content/delete/<tip_id>', methods=['POST'])
@admin_required
def delete_tip(tip_id):
    """Delete a health tip"""
    db = get_db()
    db.health_tips.delete_one({'_id': ObjectId(tip_id)})
    flash('Tip deleted.', 'success')
    return redirect(url_for('admin.content_manager'))


@admin_bp.route('/content/edit/<tip_id>', methods=['POST'])
@admin_required
def edit_tip(tip_id):
    """Edit a health tip"""
    db = get_db()
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    category = request.form.get('category', 'low')

    if title and content:
        db.health_tips.update_one(
            {'_id': ObjectId(tip_id)},
            {'$set': {'title': title, 'content': content, 'category': category}}
        )
        flash('Tip updated!', 'success')

    return redirect(url_for('admin.content_manager'))


@admin_bp.route('/ml-panel')
@admin_required
def ml_panel():
    """ML & NLP Control Panel"""
    db = get_db()
    model_info = get_model_info()

    # Model training logs
    model_logs = list(db.model_logs.find().sort('trained_at', -1).limit(10))

    # Sentiment trends
    pipeline = [
        {'$group': {
            '_id': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$created_at'}},
            'avg_sentiment': {'$avg': '$sentiment_score'},
            'count': {'$sum': 1}
        }},
        {'$sort': {'_id': 1}},
        {'$limit': 30}
    ]
    try:
        sentiment_trends = list(db.assessments.aggregate(pipeline))
    except Exception:
        sentiment_trends = []

    return render_template('admin_ml_panel.html',
                           model_info=model_info,
                           model_logs=model_logs,
                           sentiment_trends=sentiment_trends)


@admin_bp.route('/retrain', methods=['POST'])
@admin_required
def retrain_model():
    """Trigger model retraining"""
    db = get_db()
    try:
        metrics = train_model()
        # Log training
        db.model_logs.insert_one({
            'model_type': 'addiction',
            'accuracy': metrics['accuracy'],
            'trained_at': datetime.utcnow(),
            'samples_used': metrics['samples_used'],
            'parameters': metrics.get('feature_importance', {})
        })
        flash(f'Model retrained! Accuracy: {metrics["accuracy"]}%', 'success')
    except Exception as e:
        flash(f'Retraining failed: {str(e)}', 'danger')

    return redirect(url_for('admin.ml_panel'))


@admin_bp.route('/feedback')
@admin_required
def view_feedback():
    """View all feedback"""
    db = get_db()
    feedback_list = list(db.feedback.aggregate([
        {'$sort': {'created_at': -1}},
        {'$lookup': {
            'from': 'users',
            'let': {'uid': {'$toObjectId': '$user_id'}},
            'pipeline': [{'$match': {'$expr': {'$eq': ['$_id', '$$uid']}}}],
            'as': 'user_info'
        }},
        {'$unwind': {'path': '$user_info', 'preserveNullAndEmptyArrays': True}}
    ]))
    return render_template('admin_feedback.html', feedback_list=feedback_list)


# API endpoints for admin charts
@admin_bp.route('/api/analytics')
@admin_required
def analytics_data():
    """API: Get analytics data for admin charts"""
    db = get_db()

    # Addiction level distribution
    addiction_pipeline = [
        {'$group': {'_id': '$addiction_level', 'count': {'$sum': 1}}}
    ]
    addiction_data = {d['_id']: d['count'] for d in db.assessments.aggregate(addiction_pipeline)}

    # Sentiment distribution
    sentiment_pipeline = [
        {'$group': {'_id': '$sentiment', 'count': {'$sum': 1}}}
    ]
    sentiment_data = {d['_id']: d['count'] for d in db.assessments.aggregate(sentiment_pipeline)}

    # Daily assessment counts (last 30 days)
    daily_pipeline = [
        {'$group': {
            '_id': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$created_at'}},
            'count': {'$sum': 1},
            'avg_score': {'$avg': '$addiction_score'}
        }},
        {'$sort': {'_id': 1}},
        {'$limit': 30}
    ]
    try:
        daily_data = list(db.assessments.aggregate(daily_pipeline))
    except Exception:
        daily_data = []

    return jsonify({
        'addiction_dist': addiction_data,
        'sentiment_dist': sentiment_data,
        'daily_labels': [d['_id'] for d in daily_data],
        'daily_counts': [d['count'] for d in daily_data],
        'daily_avg_scores': [round(d['avg_score'], 1) for d in daily_data]
    })
