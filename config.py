"""
Antigravity - Addict Aware
Application Configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'antigravity-addict-aware-secret-2024')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/addict_aware')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-addict-aware-super-secret-key-2024-secure')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    JWT_TOKEN_LOCATION = ['cookies', 'headers']
    JWT_COOKIE_CSRF_PROTECT = False
    DEBUG = False


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
