# src/ai/train_severity_model.py
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import numpy as np
import os

def train_severity_model():
    """Train the severity prediction model using incident data"""
    print("=== Starting Disaster Severity Model Training ===")
    
    # Get absolute paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, '..', 'data', 'incidents.csv')
    models_dir = os.path.join(current_dir, 'models')
    
    # Create models directory if it doesn't exist
    os.makedirs(models_dir, exist_ok=True)
    
    print(f"Data path: {data_path}")
    print(f"Models dir: {models_dir}")
    
    # Check if data exists
    if not os.path.exists(data_path):
        print(f"ERROR: No incident data found at {data_path}")
        print("   Please run create_incidents_dataset.py from the src/ folder first.")
        return None
    
    try:
        # Load training data
        print("LOADING: Loading incident data...")
        df = pd.read_csv(data_path)
        print(f"   Loaded {len(df)} incidents")
        
        # Check for required columns
        required_columns = ['description', 'casualties', 'affected_population', 'infrastructure_damage', 'event_type', 'severity']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"ERROR: Missing columns in dataset: {missing_columns}")
            return None
        
        # Data validation and cleaning
        print("PROCESSING: Validating and cleaning data...")
        original_size = len(df)
        
        # Remove rows with missing critical values
        df = df.dropna(subset=required_columns)
        
        # Ensure numerical columns are positive
        df['casualties'] = df['casualties'].clip(lower=0)
        df['affected_population'] = df['affected_population'].clip(lower=0)
        df['infrastructure_damage'] = df['infrastructure_damage'].clip(lower=0, upper=3)
        
        if len(df) < original_size:
            print(f"   Removed {original_size - len(df)} rows with missing/invalid data")
        
        print(f"   Final dataset size: {len(df)} incidents")
        
        # Display dataset overview
        print(f"\nDATASET OVERVIEW:")
        print(f"   Event types: {df['event_type'].nunique()} types")
        print(f"   Severity distribution:")
        severity_counts = df['severity'].value_counts()
        for severity, count in severity_counts.items():
            print(f"     - {severity}: {count} incidents ({count/len(df)*100:.1f}%)")
        
        # Prepare features and target
        X = df[['description', 'casualties', 'affected_population', 'infrastructure_damage', 'event_type']]
        y = df['severity']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=0.2, 
            random_state=42,
            stratify=y  # Maintain class distribution in splits
        )
        
        print(f"\nDATA SPLITS:")
        print(f"   Training set: {len(X_train)} incidents")
        print(f"   Test set: {len(X_test)} incidents")
        
        # Create preprocessing pipeline
        preprocessor = ColumnTransformer(
            transformers=[
                ('text', TfidfVectorizer(
                    max_features=500,
                    stop_words='english',
                    ngram_range=(1, 1),
                    min_df=1
                ), 'description'),
                ('num', StandardScaler(), ['casualties', 'affected_population', 'infrastructure_damage']),
                ('cat', OneHotEncoder(handle_unknown='ignore'), ['event_type'])
            ]
        )
        
        # Create pipeline with Random Forest
        pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', RandomForestClassifier(
                n_estimators=50,
                max_depth=10,
                random_state=42,
                class_weight='balanced'
            ))
        ])
        
        # Train model
        print("\nTRAINING: Training model...")
        pipeline.fit(X_train, y_train)
        
        # Evaluate model
        print("\nMODEL EVALUATION:")
        
        # Training accuracy
        train_predictions = pipeline.predict(X_train)
        train_accuracy = accuracy_score(y_train, train_predictions)
        print(f"   Training Accuracy: {train_accuracy:.3f}")
        
        # Test accuracy
        test_predictions = pipeline.predict(X_test)
        test_accuracy = accuracy_score(y_test, test_predictions)
        print(f"   Test Accuracy: {test_accuracy:.3f}")
        
        # Detailed classification report
        print(f"\nDETAILED CLASSIFICATION REPORT:")
        print(classification_report(y_test, test_predictions, target_names=sorted(y.unique())))
        
        # Confusion matrix (text-based)
        print(f"\nCONFUSION MATRIX (Text-based):")
        cm = confusion_matrix(y_test, test_predictions)
        labels = sorted(y.unique())
        print("     " + " ".join(f"{label:>8}" for label in labels))
        for i, label in enumerate(labels):
            print(f"{label:>5} " + " ".join(f"{count:8}" for count in cm[i]))
        
        # Save model
        model_path = os.path.join(models_dir, 'severity_rf.joblib')
        joblib.dump(pipeline, model_path)
        print(f"\nSUCCESS: Model saved successfully as {model_path}")
        
        # Test the model with some examples
        print(f"\nMODEL TESTING WITH EXAMPLES:")
        test_examples = [
            {
                "description": "Minor flooding in streets after heavy rainfall",
                "casualties": 0,
                "affected_population": 50,
                "infrastructure_damage": 0,
                "event_type": "Flood"
            },
            {
                "description": "Major earthquake causing building collapses and mass casualties",
                "casualties": 45,
                "affected_population": 12000,
                "infrastructure_damage": 3,
                "event_type": "Earthquake"
            }
        ]
        
        for i, example in enumerate(test_examples, 1):
            try:
                example_df = pd.DataFrame([example])
                prediction = pipeline.predict(example_df)[0]
                probability = np.max(pipeline.predict_proba(example_df))
                print(f"   Example {i}: Predicted '{prediction}' with {probability:.1%} confidence")
            except Exception as e:
                print(f"   Example {i}: Prediction failed - {e}")
        
        # Verify model can be loaded back
        print(f"\nVERIFYING: Verifying saved model...")
        try:
            loaded_model = joblib.load(model_path)
            test_prediction = loaded_model.predict(X_test[:1])
            print(f"   SUCCESS: Model verification passed - Prediction: {test_prediction[0]}")
        except Exception as e:
            print(f"   ERROR: Model verification failed: {e}")
        
        return pipeline
        
    except Exception as e:
        print(f"ERROR: Training failed with error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("DISASTER SEVERITY MODEL TRAINING")
    print("=" * 60)
    
    model = train_severity_model()
    if model is not None:
        print("\nSUCCESS: Model training completed successfully!")
    else:
        print("\nERROR: Model training failed!")
    print("=" * 60)