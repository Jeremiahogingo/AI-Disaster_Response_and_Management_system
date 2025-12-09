#src/setup_ai.py
"""
AI System Setup
"""

import os
import subprocess
import sys
import time

def setup_ai_system():
    print("🚀 Setting up Disaster Management AI System...")
    print("=" * 60)
    
    # Verify we're in the correct directory
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}")
    
    if not os.path.exists("create_incidents_dataset.py"):
        print("❌ Error: Please run this script from the src/ folder")
        return False
    
    # Step 1: Create dataset
    print("\n1. Creating incident dataset...")
    try:
        result = subprocess.run([sys.executable, "create_incidents_dataset.py"], 
                              capture_output=True, text=True, check=True)
        print("   ✅ Dataset created successfully")
        if "incidents.csv" in result.stdout:
            print("   📊 " + [line for line in result.stdout.split('\n') if "incidents" in line][0])
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Dataset creation failed: {e}")
        if e.stderr:
            print(f"   Error details: {e.stderr}")
        return False
    except Exception as e:
        print(f"   ❌ Dataset creation failed: {e}")
        return False
    
    # Step 2: Train model
    print("\n2. Training AI model...")
    try:
        # Add a small delay to ensure file system is ready
        time.sleep(1)
        
        result = subprocess.run([sys.executable, "ai/train_severity_model.py"], 
                              capture_output=True, text=True, check=True)
        print("   ✅ AI model trained successfully")
        
        # Check for training accuracy in output
        if "Test Accuracy:" in result.stdout:
            accuracy_line = [line for line in result.stdout.split('\n') if "Test Accuracy:" in line][0]
            print(f"   {accuracy_line.strip()}")
            
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Model training failed: {e}")
        if e.stderr:
            print(f"   Error details: {e.stderr}")
        return False
    except Exception as e:
        print(f"   ❌ Model training failed: {e}")
        return False
    
    # Step 3: Test system
    print("\n3. Testing AI system...")
    try:
        # Test import
        sys.path.append('.')
        from ai import DisasterAIPredictor
        predictor = DisasterAIPredictor()
        print("   ✅ AI system imported successfully")
        
        # Test prediction
        test_incident = {
            "event_type": "Flood",
            "description": "River flooding in residential area with multiple families affected",
            "casualties": 3,
            "affected_population": 1200,
            "infrastructure_damage": 2
        }
        result = predictor.predict_and_recommend(test_incident)
        print(f"   ✅ Test prediction: {result['predicted_severity']} (confidence: {result['confidence']:.1%})")
        print(f"   ✅ Resources recommended: {len(result['recommended_resources'])}")
        
        # Show a couple of recommended resources
        if result['recommended_resources']:
            print(f"   ✅ Sample resources: {', '.join([r['resource'] for r in result['recommended_resources'][:3]])}")
        
    except Exception as e:
        print(f"   ❌ AI system test failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 AI System setup completed successfully!")
    print("=" * 60)
    print("\n📝 Usage Examples:")
    print("   from ai import DisasterAIPredictor")
    print("   predictor = DisasterAIPredictor()")
    print("   result = predictor.predict_and_recommend({")
    print("       'event_type': 'Flood',")
    print("       'description': 'Your incident description',")
    print("       'casualties': 5,")
    print("       'affected_population': 1000,")
    print("       'infrastructure_damage': 2")
    print("   })")
    print("\n🔧 Advanced usage:")
    print("   from ai import ResourceManager")
    print("   manager = ResourceManager()")
    
    return True

if __name__ == "__main__":
    success = setup_ai_system()
    sys.exit(0 if success else 1)