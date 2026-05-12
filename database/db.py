"""
Antigravity - Addict Aware
Database Connection & Schema Utilities
"""
from pymongo import MongoClient
from datetime import datetime
import os


def get_db():
    """Get MongoDB database connection"""
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/addict_aware')
    client = MongoClient(mongo_uri)
    # Extracts the specific database name dynamically from the URI if present, 
    # otherwise defaults to 'addict_aware' 
    db = client.get_default_database('addict_aware')
    return db


def init_db(db):
    """Initialize database collections and indexes"""
    # Create collections if they don't exist
    collections = ['users', 'assessments', 'health_tips', 'feedback', 'model_logs']
    existing = db.list_collection_names()
    for col in collections:
        if col not in existing:
            db.create_collection(col)

    # Create indexes
    db.users.create_index('email', unique=True)
    db.assessments.create_index([('user_id', 1), ('created_at', -1)])
    db.feedback.create_index('user_id')

    # Seed default admin if not exists
    admin = db.users.find_one({'role': 'admin'})
    if not admin:
        from flask_bcrypt import generate_password_hash
        db.users.insert_one({
            'name': 'Admin',
            'email': 'admin@addictaware.com',
            'password': generate_password_hash('admin123').decode('utf-8'),
            'role': 'admin',
            'created_at': datetime.utcnow()
        })

    # Seed default health tips
    if db.health_tips.count_documents({}) == 0:
        tips = [
            {
                'title': 'Digital Detox Hour',
                'content': 'Set aside one hour each day completely free from screens. Use this time for reading, walking, or meditation.',
                'category': 'low',
                'created_at': datetime.utcnow()
            },
            {
                'title': 'The 20-20-20 Rule',
                'content': 'Every 20 minutes, look at something 20 feet away for 20 seconds. This reduces eye strain and breaks the screen trance.',
                'category': 'low',
                'created_at': datetime.utcnow()
            },
            {
                'title': 'Notification Audit',
                'content': 'Turn off non-essential notifications. Each notification is a trigger that pulls you back into your device.',
                'category': 'medium',
                'created_at': datetime.utcnow()
            },
            {
                'title': 'Mindful Social Media',
                'content': 'Before opening social media, ask yourself: "Why am I opening this?" Set a 15-minute timer and stick to it.',
                'category': 'medium',
                'created_at': datetime.utcnow()
            },
            {
                'title': 'Sleep Hygiene Protocol',
                'content': 'No screens 1 hour before bed. Blue light disrupts melatonin production. Use night mode if you must use devices.',
                'category': 'medium',
                'created_at': datetime.utcnow()
            },
            {
                'title': 'App Usage Tracking',
                'content': 'Install a screen time tracker. Awareness is the first step to change. Review your usage weekly.',
                'category': 'high',
                'created_at': datetime.utcnow()
            },
            {
                'title': 'Professional Support',
                'content': 'Consider talking to a counselor or therapist who specializes in digital wellness. High addiction levels benefit from professional guidance.',
                'category': 'high',
                'created_at': datetime.utcnow()
            },
            {
                'title': 'Device-Free Zones',
                'content': 'Designate areas in your home (bedroom, dining table) as device-free zones. Physical boundaries create mental boundaries.',
                'category': 'high',
                'created_at': datetime.utcnow()
            }
        ]
        db.health_tips.insert_many(tips)

    print("[✓] Database initialized successfully")
    return db


# Database Schema Documentation
SCHEMAS = {
    'users': {
        'name': 'string',
        'email': 'string (unique)',
        'password': 'string (hashed)',
        'role': 'string (user/admin)',
        'created_at': 'datetime'
    },
    'assessments': {
        'user_id': 'ObjectId (ref: users)',
        'screen_time': 'float (hours/day)',
        'phone_pickups': 'int (times/day)',
        'social_media_time': 'float (hours/day)',
        'emotional_text': 'string',
        'addiction_level': 'string (Low/Medium/High)',
        'addiction_score': 'float (0-100)',
        'sentiment': 'string (Positive/Negative/Neutral)',
        'sentiment_score': 'float (-1 to 1)',
        'created_at': 'datetime'
    },
    'health_tips': {
        'title': 'string',
        'content': 'string',
        'category': 'string (low/medium/high)',
        'created_at': 'datetime'
    },
    'feedback': {
        'user_id': 'ObjectId (ref: users)',
        'message': 'string',
        'rating': 'int (1-5)',
        'created_at': 'datetime'
    },
    'model_logs': {
        'model_type': 'string (addiction/sentiment)',
        'accuracy': 'float',
        'trained_at': 'datetime',
        'samples_used': 'int',
        'parameters': 'dict'
    }
}
