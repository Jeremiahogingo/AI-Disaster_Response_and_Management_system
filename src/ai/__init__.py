#src/ai/__init__.py
"""
Disaster Management AI Package
Provides AI-powered severity prediction and resource recommendations for disaster incidents.
"""

__version__ = "1.0.0"
__author__ = "Disaster Management Team - lion bouy"
__description__ = "AI system for disaster severity prediction and resource allocation"

# Import main classes for easy access
from .inference import DisasterAIPredictor
from .resource_availability import ResourceManager
from .train_severity_model import train_severity_model

# Define what gets imported with "from ai import *"
__all__ = [
    'DisasterAIPredictor',
    'ResourceManager', 
    'train_severity_model'
]

# Package initialization
print(f"🚀 Disaster AI System v{__version__} initialized")

# Check if required model files exist
import os
def check_dependencies():
    """Check if all required model files are available"""
    required_files = [
        'models/severity_rf.joblib',
        'models/resource_map.json'
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        if not os.path.exists(full_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"⚠️  Warning: Missing files: {missing_files}")
        if 'severity_rf.joblib' in missing_files:
            print("   Run: python train_severity_model.py to train the model")
        if 'resource_map.json' in missing_files:
            print("   Ensure resource_map.json exists in ai/models/ folder")
    else:
        print("✅ All AI dependencies loaded successfully")

# Run dependency check on import
check_dependencies()