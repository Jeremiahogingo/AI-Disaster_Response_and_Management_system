# src/ai/inference.py

import joblib
import json
import pandas as pd
import numpy as np
import os

class DisasterAIPredictor:
    def __init__(self, model_path=None, resource_map_path=None):
        # Set default paths if not provided
        if model_path is None:
            model_path = os.path.join(os.path.dirname(__file__), 'models', 'severity_rf.joblib')
        if resource_map_path is None:
            resource_map_path = os.path.join(os.path.dirname(__file__), 'models', 'resource_map.json')
        
        self.model_path = model_path
        self.resource_map_path = resource_map_path
        
        # Load model if it exists
        if os.path.exists(model_path):
            try:
                self.severity_model = joblib.load(model_path)
                print(f"✅ AI model loaded successfully from {model_path}")
            except Exception as e:
                self.severity_model = None
                print(f"❌ Error loading model from {model_path}: {e}")
        else:
            self.severity_model = None
            print(f"⚠️  Warning: Model not found at {model_path}. Using rule-based predictions.")
        
        # Load resource map
        if os.path.exists(resource_map_path):
            try:
                with open(resource_map_path, 'r', encoding='utf-8') as f:
                    self.resource_map = json.load(f)
                print(f"✅ Resource map loaded successfully from {resource_map_path}")
            except Exception as e:
                self.resource_map = {"event_type_map": {}, "severity_map": {}}
                print(f"❌ Error loading resource map from {resource_map_path}: {e}")
        else:
            self.resource_map = {"event_type_map": {}, "severity_map": {}}
            print(f"⚠️  Warning: Resource map not found at {resource_map_path}")
    
    def predict_severity(self, incident_data):
        """Predict incident severity using trained model or fallback rules"""
        if self.severity_model is not None:
            try:
                # Convert incident data to features in the format expected by the model
                features_df = self._prepare_features_dataframe(incident_data)
                severity_prediction = self.severity_model.predict(features_df)[0]
                confidence = np.max(self.severity_model.predict_proba(features_df))
                
                return severity_prediction, round(confidence, 3)
            except Exception as e:
                print(f"⚠️  Model prediction failed: {e}. Using rule-based fallback.")
        
        # Fallback to rule-based prediction
        return self._rule_based_severity(incident_data), 0.5
    
    def _prepare_features_dataframe(self, incident_data):
        """Prepare features as a DataFrame for model prediction"""
        # Create a DataFrame with the same structure as training data
        features_dict = {
            'description': [incident_data.get('description', '')],
            'casualties': [incident_data.get('casualties', 0)],
            'affected_population': [incident_data.get('affected_population', 0)],
            'infrastructure_damage': [incident_data.get('infrastructure_damage', 0)],
            'event_type': [incident_data.get('event_type', 'Unknown')]
        }
        return pd.DataFrame(features_dict)
    
    def _rule_based_severity(self, incident_data):
        """Improved fallback rule-based severity prediction"""
        casualties = incident_data.get('casualties', 0)
        affected = incident_data.get('affected_population', 0)
        infrastructure = incident_data.get('infrastructure_damage', 0)
        
        # Calculate a severity score
        severity_score = 0
        severity_score += min(casualties, 100) / 20  # Up to 5 points for casualties
        severity_score += min(affected, 50000) / 10000  # Up to 5 points for affected population
        severity_score += infrastructure  # 0-3 points for infrastructure damage
        
        # Determine severity level
        if severity_score >= 6:
            return "Critical"
        elif severity_score >= 3:
            return "High"
        elif severity_score >= 1:
            return "Medium"
        else:
            return "Low"
    
    def recommend_resources(self, event_type, severity, available_resources=None):
        """Recommend resources based on event type and severity"""
        recommendations = []
        
        # Get event-specific resources
        event_resources = self.resource_map.get("event_type_map", {}).get(event_type, [])
        # Get severity-based resources  
        severity_resources = self.resource_map.get("severity_map", {}).get(severity, [])
        
        # Combine and prioritize (remove duplicates, keep highest priority)
        all_resources = {}
        for resource in event_resources + severity_resources:
            resource_name = resource["resource"]
            if (resource_name not in all_resources or 
                resource["priority"] < all_resources[resource_name]["priority"]):
                all_resources[resource_name] = resource
        
        # Convert back to list and sort by priority
        recommendations = sorted(all_resources.values(), key=lambda x: x["priority"])
        
        return recommendations
    
    def predict_and_recommend(self, incident_data):
        """Convenience method to predict severity and get recommendations"""
        severity, confidence = self.predict_severity(incident_data)
        event_type = incident_data.get('event_type', 'Unknown')
        recommendations = self.recommend_resources(event_type, severity)
        
        return {
            'predicted_severity': severity,
            'confidence': confidence,
            'event_type': event_type,
            'recommended_resources': recommendations
        }
    
    def get_supported_event_types(self):
        """Get list of all supported event types from resource map"""
        return list(self.resource_map.get("event_type_map", {}).keys())
    
    def get_supported_severity_levels(self):
        """Get list of all supported severity levels from resource map"""
        return list(self.resource_map.get("severity_map", {}).keys())
    
    def is_model_loaded(self):
        """Check if the AI model is successfully loaded"""
        return self.severity_model is not None
    
    def is_resource_map_loaded(self):
        """Check if the resource map is successfully loaded"""
        return bool(self.resource_map.get("event_type_map")) and bool(self.resource_map.get("severity_map"))

# Example usage and comprehensive testing
if __name__ == "__main__":
    print("🚀 Testing Disaster Management AI Predictor")
    print("=" * 50)
    
    # Initialize the predictor
    predictor = DisasterAIPredictor()
    
    # Display system status
    print(f"🤖 AI Model Status: {'✅ Loaded' if predictor.is_model_loaded() else '❌ Not Loaded'}")
    print(f"🗺️  Resource Map Status: {'✅ Loaded' if predictor.is_resource_map_loaded() else '❌ Not Loaded'}")
    
    # Test with various incident scenarios
    test_incidents = [
        {
            "event_type": "Flood",
            "description": "Minor street flooding after heavy rain, no casualties reported",
            "casualties": 0,
            "affected_population": 50,
            "infrastructure_damage": 0
        },
        {
            "event_type": "Earthquake",
            "description": "Major earthquake measuring 7.2 magnitude, multiple building collapses in urban area",
            "casualties": 45,
            "affected_population": 12000,
            "infrastructure_damage": 3
        }
    ]
    
    for i, incident in enumerate(test_incidents, 1):
        print(f"\n📝 Test Scenario {i}: {incident['event_type']}")
        
        # Get prediction and recommendations
        result = predictor.predict_and_recommend(incident)
        
        print(f"🤖 AI ANALYSIS:")
        print(f"  • Predicted Severity: {result['predicted_severity']}")
        print(f"  • Confidence Level: {result['confidence'] * 100:.1f}%")
        print(f"  • Recommended Resources ({len(result['recommended_resources'])}):")
        
        for j, resource in enumerate(result['recommended_resources'], 1):
            print(f"    {j}. {resource['resource']} (priority: {resource['priority']})")