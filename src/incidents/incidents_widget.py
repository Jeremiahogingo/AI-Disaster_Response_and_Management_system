#src/incidents/incidents_widget.py
"""Incident management widget for Disaster_Management_System."""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QFrame, QTableWidget, QTableWidgetItem,
                           QComboBox, QLineEdit, QDialog, QFormLayout,
                           QTextEdit, QMessageBox, QHeaderView, QGroupBox,
                           QProgressBar, QListWidget, QListWidgetItem,
                           QDialogButtonBox, QProgressDialog, QApplication)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QBrush
import os
import sys
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the parent directory to path to import AI modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Enhanced AI availability check with simplified diagnostics
def check_ai_availability():
    """Check AI availability and provide detailed diagnostics"""
    ai_status = {
        'available': False,
        'reason': "Unknown",
        'details': {}
    }
    
    print("\n" + "="*60)
    print("🤖 AI SYSTEM DIAGNOSTICS")
    print("="*60)
    
    # Check if ai directory exists
    ai_path = os.path.join(parent_dir, 'ai')
    if not os.path.exists(ai_path):
        ai_status['reason'] = "AI directory not found"
        ai_status['details']['ai_directory'] = f"Missing: {ai_path}"
        print(f"❌ AI Directory: {ai_path} - NOT FOUND")
        return ai_status
    
    print(f"✅ AI Directory: {ai_path} - FOUND")
    
    # Check if inference module exists
    inference_path = os.path.join(ai_path, 'inference.py')
    if not os.path.exists(inference_path):
        ai_status['reason'] = "AI inference module not found"
        ai_status['details']['inference_module'] = f"Missing: {inference_path}"
        print(f"❌ AI Inference Module: {inference_path} - NOT FOUND")
        return ai_status
    
    print(f"✅ AI Inference Module: {inference_path} - FOUND")
    
    # Try to import AI predictor
    try:
        from ai.inference import DisasterAIPredictor
        ai_status['available'] = True
        ai_status['reason'] = "AI module loaded successfully"
        print("✅ AI Module Import: SUCCESS")
        
        # Check model files with correct extensions
        model_files = {
            'severity_model': os.path.join(ai_path, "models", "severity_rf.joblib"),
            'resource_map': os.path.join(ai_path, "models", "resource_map.json")
        }
        
        print("\n🔍 Checking AI Model Files:")
        all_files_exist = True
        for file_type, file_path in model_files.items():
            if os.path.exists(file_path):
                print(f"   ✅ {file_type}: {os.path.basename(file_path)} - FOUND")
                ai_status['details'][file_type] = "Found"
            else:
                print(f"   ⚠️  {file_type}: {os.path.basename(file_path)} - NOT FOUND")
                ai_status['details'][file_type] = "Missing"
                all_files_exist = False
        
        if not all_files_exist:
            print("   ℹ️  AI will use fallback mode with basic recommendations")
            ai_status['details']['mode'] = "Fallback"
        else:
            ai_status['details']['mode'] = "Full AI"
            print("   ✅ All model files found - Full AI mode available")
            
        # Test AI predictor initialization
        try:
            predictor = DisasterAIPredictor()
            if predictor and predictor.is_model_loaded():
                print("✅ AI Predictor Initialization: SUCCESS")
                ai_status['details']['predictor_status'] = "Initialized"
            else:
                print("⚠️  AI Predictor Initialization: PARTIAL (using fallbacks)")
                ai_status['details']['predictor_status'] = "Fallback"
        except Exception as e:
            print(f"❌ AI Predictor Initialization: FAILED - {e}")
            ai_status['details']['predictor_status'] = f"Failed: {e}"
            
    except ImportError as e:
        ai_status['reason'] = f"AI module import failed: {e}"
        ai_status['details']['import_error'] = str(e)
        print(f"❌ AI Module Import: FAILED - {e}")
    except Exception as e:
        ai_status['reason'] = f"AI initialization error: {e}"
        ai_status['details']['init_error'] = str(e)
        print(f"❌ AI Initialization: FAILED - {e}")
    
    print("="*60)
    print(f"📊 FINAL AI STATUS: {'✅ ONLINE' if ai_status['available'] else '❌ OFFLINE'}")
    print("="*60)
    
    return ai_status

# Run AI diagnostics
ai_diagnostics = check_ai_availability()
AI_AVAILABLE = ai_diagnostics['available']

# Define a fallback predictor class if AI is not available
if not AI_AVAILABLE:
    class DisasterAIPredictor:
        def __init__(self, *args, **kwargs):
            print("✅ Basic AI Predictor initialized (fallback mode)")
            self.is_loaded = True
            
        def is_model_loaded(self):
            return True
            
        def is_resource_map_loaded(self):
            return True
            
        def recommend_resources(self, event_type, severity):
            # Enhanced fallback recommendations with better descriptions
            base_recommendations = {
                "Flood": [
                    {"resource": "Rescue Boats", "priority": 1, "purpose": "Watercraft for search and rescue operations in flooded areas. Essential for accessing submerged locations and evacuating stranded individuals.", "quantity": 2},
                    {"resource": "Emergency Shelter", "priority": 1, "purpose": "Temporary housing facilities for displaced individuals and families. Includes tents, temporary structures, and basic amenities for affected populations.", "quantity": 5},
                    {"resource": "Medical Team", "priority": 2, "purpose": "Emergency medical professionals including doctors, nurses, and paramedics. Provide immediate medical care, triage, and emergency treatment for injuries.", "quantity": 3},
                    {"resource": "Water Purification", "priority": 3, "purpose": "Systems and equipment to provide clean drinking water. Includes purification tablets, filtration systems, and water testing kits to prevent waterborne diseases.", "quantity": 2}
                ],
                "Earthquake": [
                    {"resource": "Search & Rescue", "priority": 1, "purpose": "Specialized teams trained in locating and extracting individuals from collapsed structures. Equipped with technical rescue gear and emergency medical supplies.", "quantity": 4},
                    {"resource": "Structural Engineers", "priority": 1, "purpose": "Professional engineers to assess building integrity and safety. Critical for determining structural stability and identifying collapse risks.", "quantity": 2},
                    {"resource": "Medical Team", "priority": 1, "purpose": "Emergency medical professionals for immediate healthcare services. Handle trauma cases, fractures, and emergency medical treatment.", "quantity": 4},
                    {"resource": "Heavy Equipment", "priority": 2, "purpose": "Machinery including excavators, bulldozers, and cranes for debris removal and access creation. Essential for clearing collapsed structures.", "quantity": 3}
                ],
                "Wildfire": [
                    {"resource": "Firefighters", "priority": 1, "purpose": "Trained fire suppression and technical rescue personnel. Equipped with firefighting gear, extraction tools, and emergency response equipment.", "quantity": 6},
                    {"resource": "Helicopters", "priority": 1, "purpose": "Aircraft for aerial reconnaissance, medical evacuation, and resource transport. Provide rapid response and access to remote or inaccessible areas.", "quantity": 2},
                    {"resource": "Evacuation Team", "priority": 1, "purpose": "Personnel specialized in organizing and executing safe evacuations. Coordinate transportation, temporary shelter, and population movement.", "quantity": 3},
                    {"resource": "Emergency Shelter", "priority": 2, "purpose": "Temporary housing for displaced residents. Provides basic necessities and safety for those forced to leave their homes.", "quantity": 4}
                ],
                "Chemical Spill": [
                    {"resource": "Hazmat Team", "priority": 1, "purpose": "Hazardous materials specialists for chemical, biological, or radiological incidents. Equipped with protective gear and containment equipment.", "quantity": 3},
                    {"resource": "Decontamination Unit", "priority": 1, "purpose": "Facilities and equipment for cleaning and decontaminating affected individuals and areas. Prevents spread of hazardous materials.", "quantity": 2},
                    {"resource": "Medical Team", "priority": 1, "purpose": "Emergency medical care for chemical exposure treatment. Specialized in toxicology and emergency decontamination procedures.", "quantity": 3},
                    {"resource": "Evacuation Team", "priority": 2, "purpose": "Safe relocation of affected populations from contaminated areas. Ensures public safety and prevents further exposure.", "quantity": 2}
                ],
                "Building Collapse": [
                    {"resource": "Search & Rescue", "priority": 1, "purpose": "Specialized teams for locating and extracting trapped individuals. Use technical equipment for structural collapse response.", "quantity": 4},
                    {"resource": "Structural Engineers", "priority": 1, "purpose": "Building stability assessment and safety evaluation. Determine structural integrity and collapse risks.", "quantity": 2},
                    {"resource": "Medical Team", "priority": 1, "purpose": "Emergency medical care for trauma patients. Handle crush injuries, fractures, and emergency treatment.", "quantity": 3},
                    {"resource": "Heavy Equipment", "priority": 2, "purpose": "Machinery for debris removal and access creation. Essential for reaching trapped individuals safely.", "quantity": 2}
                ],
                "Road Accident": [
                    {"resource": "Emergency Medical", "priority": 1, "purpose": "Immediate medical care for accident victims. Provide emergency treatment and stabilization at the scene.", "quantity": 2},
                    {"resource": "Fire Department", "priority": 1, "purpose": "Vehicle extraction and safety operations. Specialized in technical rescue and fire suppression.", "quantity": 1},
                    {"resource": "Police", "priority": 2, "purpose": "Traffic control, scene security, and investigation. Maintain public safety and gather evidence.", "quantity": 2},
                    {"resource": "Tow Truck", "priority": 3, "purpose": "Vehicle recovery and road clearance. Restore traffic flow and remove damaged vehicles.", "quantity": 1}
                ],
                "Train Derailment": [
                    {"resource": "Emergency Medical", "priority": 1, "purpose": "Mass casualty medical care for injured passengers. Provide triage and emergency treatment.", "quantity": 4},
                    {"resource": "Search & Rescue", "priority": 1, "purpose": "Location and extraction of trapped passengers. Specialized in railway incident response.", "quantity": 3},
                    {"resource": "Hazmat Team", "priority": 2, "purpose": "Chemical leak containment and safety. Handle hazardous materials from damaged rail cars.", "quantity": 2},
                    {"resource": "Heavy Equipment", "priority": 2, "purpose": "Righting overturned trains and clearing tracks. Restore railway operations safely.", "quantity": 2}
                ],
                "Terrorist Attack": [
                    {"resource": "SWAT Team", "priority": 1, "purpose": "Neutralize active threats and secure the area. Specialized in high-risk tactical operations.", "quantity": 2},
                    {"resource": "Emergency Medical", "priority": 1, "purpose": "Mass casualty care for multiple victims. Handle trauma cases and emergency treatment.", "quantity": 6},
                    {"resource": "Bomb Squad", "priority": 1, "purpose": "Explosive device disposal and safety. Render safe suspicious packages and devices.", "quantity": 1},
                    {"resource": "Crisis Counselors", "priority": 3, "purpose": "Mental health support for victims and responders. Provide psychological first aid and trauma support.", "quantity": 3}
                ],
                "Industrial Fire": [
                    {"resource": "Firefighters", "priority": 1, "purpose": "Industrial fire suppression and containment. Specialized in complex industrial fire scenarios.", "quantity": 5},
                    {"resource": "Hazmat Team", "priority": 1, "purpose": "Chemical hazard control and containment. Handle industrial chemical releases and spills.", "quantity": 2},
                    {"resource": "Medical Team", "priority": 2, "purpose": "Emergency medical care for injured workers. Handle chemical exposure and burn treatment.", "quantity": 3},
                    {"resource": "Evacuation Team", "priority": 2, "purpose": "Safe evacuation of industrial facility personnel. Coordinate emergency exits and assembly points.", "quantity": 2}
                ],
                "Utility Failure": [
                    {"resource": "Utility Repair Crew", "priority": 1, "purpose": "Restore essential services including electricity, water, and gas. Repair damaged infrastructure and utilities.", "quantity": 3},
                    {"resource": "Emergency Generator", "priority": 2, "purpose": "Backup power sources for critical facilities and operations. Ensure continuous operation of emergency services.", "quantity": 2},
                    {"resource": "Water Distribution", "priority": 2, "purpose": "Emergency water supply distribution systems. Provide clean water to affected populations.", "quantity": 2},
                    {"resource": "Communication Unit", "priority": 3, "purpose": "Emergency communication systems restoration. Maintain critical communication channels.", "quantity": 1}
                ],
                "Maritime Incident": [
                    {"resource": "Coast Guard", "priority": 1, "purpose": "Maritime security and rescue services. Specialized in water-based emergencies and search and rescue.", "quantity": 2},
                    {"resource": "Rescue Boats", "priority": 1, "purpose": "Watercraft for maritime search and rescue operations. Essential for water-based emergency response.", "quantity": 3},
                    {"resource": "Medical Team", "priority": 1, "purpose": "Emergency medical care for maritime incident victims. Handle drowning, hypothermia, and injuries.", "quantity": 3},
                    {"resource": "Divers", "priority": 2, "purpose": "Underwater search and rescue specialists. Conduct submerged operations and recovery missions.", "quantity": 2}
                ],
                "Pandemic Cluster": [
                    {"resource": "Medical Team", "priority": 1, "purpose": "Medical care, testing, and treatment for infectious diseases. Handle outbreak containment and patient care.", "quantity": 5},
                    {"resource": "Contact Tracers", "priority": 1, "purpose": "Disease spread monitoring and infection tracking. Identify and monitor potential exposure cases.", "quantity": 4},
                    {"resource": "PPE Supplies", "priority": 2, "purpose": "Personal protective equipment for responders and medical staff. Prevent disease transmission.", "quantity": 100},
                    {"resource": "Vaccination Team", "priority": 3, "purpose": "Immunization and preventative care services. Administer vaccines and conduct public health interventions.", "quantity": 3}
                ]
            }
            
            # Default recommendations if type not found
            recommendations = base_recommendations.get(event_type, [
                {"resource": "Emergency Team", "priority": 1, "purpose": "Initial assessment and coordination of emergency response. Establish command structure and resource allocation.", "quantity": 2},
                {"resource": "First Aid", "priority": 2, "purpose": "Basic medical support and initial treatment. Provide immediate care until advanced medical help arrives.", "quantity": 2},
                {"resource": "Coordination", "priority": 3, "purpose": "Incident management and multi-agency coordination. Ensure efficient resource deployment and communication.", "quantity": 1}
            ])
            
            # Adjust quantities based on severity
            severity_multiplier = {"Low": 0.5, "Medium": 1.0, "High": 1.5, "Critical": 2.0}
            multiplier = severity_multiplier.get(severity, 1.0)
            
            for resource in recommendations:
                if 'quantity' in resource:
                    resource['quantity'] = max(1, int(resource['quantity'] * multiplier))
            
            return recommendations

class AIWorker(QThread):
    """Worker thread for AI predictions"""
    prediction_finished = pyqtSignal(dict)  # incident_id -> resources
    
    def __init__(self, incident_data, predictor):
        super().__init__()
        self.incident_data = incident_data
        self.predictor = predictor
    
    def run(self):
        try:
            resources = self.predictor.recommend_resources(
                self.incident_data['type'],
                self.incident_data['severity']
            )
            self.prediction_finished.emit({
                'incident_id': self.incident_data.get('id', 'new'),
                'resources': resources
            })
        except Exception as e:
            logger.error(f"AI prediction failed: {e}")
            self.prediction_finished.emit({
                'incident_id': self.incident_data.get('id', 'new'),
                'resources': [],
                'error': str(e)
            })

class AIRecommendationsDialog(QDialog):
    """Dialog to show detailed AI resource recommendations"""
    
    def __init__(self, resources, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🤖 AI Resource Recommendations")
        self.setModal(True)
        self.setMinimumWidth(800)  # Increased width
        self.setMinimumHeight(600)  # Increased height
        self.setup_ui(resources)
        
    def setup_ui(self, resources):
        layout = QVBoxLayout(self)
        
        if not resources:
            no_data_label = QLabel("No AI recommendations available for this incident.")
            no_data_label.setAlignment(Qt.AlignCenter)
            no_data_label.setStyleSheet("color: #666; padding: 20px; font-size: 12pt;")
            layout.addWidget(no_data_label)
        else:
            # Enhanced header
            header_label = QLabel(f"🤖 AI Resource Recommendations")
            header_label.setFont(QFont("Arial", 16, QFont.Bold))
            header_label.setStyleSheet("""
                padding: 20px; 
                background-color: #2c3e50; 
                border-radius: 8px; 
                color: white;
                margin-bottom: 10px;
            """)
            layout.addWidget(header_label)
            
            # Summary info
            summary_label = QLabel(f"Total Resources Recommended: {len(resources)}")
            summary_label.setFont(QFont("Arial", 11, QFont.Bold))
            summary_label.setStyleSheet("color: #34495e; padding: 10px; background-color: #ecf0f1; border-radius: 5px;")
            layout.addWidget(summary_label)
            
            # Enhanced resources list with better styling
            resources_list = QListWidget()
            resources_list.setStyleSheet("""
                QListWidget {
                    background-color: white;
                    border: 2px solid #bdc3c7;
                    border-radius: 8px;
                    font-size: 11pt;
                }
                QListWidget::item {
                    border-bottom: 1px solid #ecf0f1;
                    padding: 15px;
                }
                QListWidget::item:selected {
                    background-color: #3498db;
                    color: white;
                }
                QListWidget::item:hover {
                    background-color: #f8f9fa;
                }
            """)
            
            for resource in resources:
                item_widget = QWidget()
                item_layout = QVBoxLayout(item_widget)
                item_layout.setSpacing(8)
                
                # Top row: Resource name and priority
                top_layout = QHBoxLayout()
                
                name_label = QLabel(resource['resource'])
                name_label.setFont(QFont("Arial", 12, QFont.Bold))
                name_label.setStyleSheet("color: #2c3e50;")
                
                # Enhanced priority display with text labels
                priority_num = resource['priority']
                priority_text = self.get_priority_text(priority_num)
                priority_label = QLabel(f"Priority: {priority_text}")
                priority_label.setStyleSheet(f"""
                    color: {self.get_priority_color(priority_num)};
                    font-weight: bold;
                    padding: 6px 16px;
                    border-radius: 15px;
                    background-color: {self.get_priority_bg_color(priority_num)};
                    border: 1px solid {self.get_priority_border_color(priority_num)};
                """)
                
                # Quantity if available
                quantity_text = f"Quantity: {resource.get('quantity', 'As needed')}"
                quantity_label = QLabel(quantity_text)
                quantity_label.setStyleSheet("color: #7f8c8d; font-size: 10pt; font-weight: bold;")
                
                top_layout.addWidget(name_label)
                top_layout.addStretch()
                top_layout.addWidget(quantity_label)
                top_layout.addWidget(priority_label)
                
                # Purpose with enhanced styling
                purpose_text = self.get_enhanced_purpose(resource)
                purpose_label = QLabel(purpose_text)
                purpose_label.setWordWrap(True)
                purpose_label.setStyleSheet("""
                    color: #555;
                    font-size: 10.5pt;
                    margin-top: 5px;
                    padding: 8px;
                    background-color: #f8f9fa;
                    border-radius: 4px;
                    border-left: 3px solid #3498db;
                """)
                
                item_layout.addLayout(top_layout)
                item_layout.addWidget(purpose_label)
                
                list_item = QListWidgetItem(resources_list)
                list_item.setSizeHint(item_widget.sizeHint())
                resources_list.addItem(list_item)
                resources_list.setItemWidget(list_item, item_widget)
            
            layout.addWidget(resources_list)
        
        # Enhanced close button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        close_button = QPushButton("✅ Close Recommendations")
        close_button.clicked.connect(self.accept)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #219653;
            }
        """)
        
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)

    def get_priority_text(self, priority):
        """Convert priority number to meaningful text"""
        priority_map = {
            1: "CRITICAL - Immediate Response Required",
            2: "HIGH - Urgent Attention Needed", 
            3: "MEDIUM - Important Resource",
            4: "LOW - Standard Priority",
            5: "MINIMAL - Supplementary Resource"
        }
        return priority_map.get(priority, f"Priority {priority}")

    def get_priority_color(self, priority):
        """Get text color for priority"""
        colors = {
            1: "#ffffff",  # White
            2: "#ffffff",  # White
            3: "#000000",  # Black
            4: "#000000",  # Black
            5: "#000000"   # Black
        }
        return colors.get(priority, "#000000")

    def get_priority_bg_color(self, priority):
        """Get background color for priority"""
        colors = {
            1: "#e74c3c",  # Red for critical
            2: "#e67e22",  # Orange for high
            3: "#f1c40f",  # Yellow for medium
            4: "#2ecc71",  # Green for low
            5: "#3498db"   # Blue for minimal
        }
        return colors.get(priority, "#95a5a6")

    def get_priority_border_color(self, priority):
        """Get border color for priority"""
        colors = {
            1: "#c0392b",  # Dark red
            2: "#d35400",  # Dark orange
            3: "#f39c12",  # Dark yellow
            4: "#27ae60",  # Dark green
            5: "#2980b9"   # Dark blue
        }
        return colors.get(priority, "#7f8c8d")

    def get_enhanced_purpose(self, resource):
        """Get enhanced purpose description with fallback"""
        purpose = resource.get('purpose', '')
        
        # If purpose is missing or generic, provide detailed descriptions
        if not purpose or purpose == 'No description available':
            resource_name = resource['resource']
            purpose_map = {
                "Life Jackets": "Essential personal flotation devices for water rescue operations. Critical for flood scenarios to prevent drowning and ensure safety of rescue teams and victims.",
                "Emergency Shelter": "Temporary housing facilities for displaced individuals and families. Includes tents, temporary structures, and basic amenities for affected populations.",
                "Medical Team": "Emergency medical professionals including doctors, nurses, and paramedics. Provide immediate medical care, triage, and emergency treatment for injuries.",
                "Water Purification": "Systems and equipment to provide clean drinking water. Includes purification tablets, filtration systems, and water testing kits to prevent waterborne diseases.",
                "Rescue Boats": "Watercraft for search and rescue operations in flooded areas. Essential for accessing submerged locations and evacuating stranded individuals.",
                "Search & Rescue": "Specialized teams trained in locating and extracting individuals from dangerous situations. Equipped with technical rescue gear and emergency medical supplies.",
                "Structural Engineers": "Professional engineers to assess building integrity and safety. Critical for determining structural stability and identifying collapse risks.",
                "Heavy Equipment": "Machinery including excavators, bulldozers, and cranes for debris removal and access creation. Essential for clearing blocked roads and collapsed structures.",
                "Firefighters": "Trained fire suppression and technical rescue personnel. Equipped with firefighting gear, extraction tools, and emergency response equipment.",
                "Helicopters": "Aircraft for aerial reconnaissance, medical evacuation, and resource transport. Provide rapid response and access to remote or inaccessible areas.",
                "Evacuation Team": "Personnel specialized in organizing and executing safe evacuations. Coordinate transportation, temporary shelter, and population movement.",
                "Hazmat Team": "Hazardous materials specialists for chemical, biological, or radiological incidents. Equipped with protective gear and containment equipment.",
                "Decontamination Unit": "Facilities and equipment for cleaning and decontaminating affected individuals and areas. Prevents spread of hazardous materials.",
                "Emergency Medical": "Mobile medical units and field hospitals for immediate healthcare services. Include emergency treatment facilities and medical supplies.",
                "Fire Department": "Comprehensive fire and rescue services with apparatus, equipment, and trained personnel for various emergency scenarios.",
                "Police": "Law enforcement for security, traffic control, and public safety. Maintain order and secure affected areas during emergency operations.",
                "Tow Truck": "Vehicle recovery and removal services. Clear roadways of disabled or damaged vehicles to restore access and traffic flow.",
                "SWAT Team": "Special weapons and tactics for high-risk situations. Handle armed threats, hostage situations, and complex security operations.",
                "Bomb Squad": "Explosive ordnance disposal specialists. Safely handle and dispose of explosive devices and suspicious packages.",
                "Crisis Counselors": "Mental health professionals providing psychological first aid and trauma support. Assist victims, families, and responders with emotional support.",
                "Utility Repair Crew": "Technicians for restoring essential services including electricity, water, and gas. Repair damaged infrastructure and utilities.",
                "Emergency Generator": "Backup power sources for critical facilities and operations. Ensure continuous operation of emergency services and medical equipment.",
                "Water Distribution": "Systems for distributing clean water to affected populations. Include water trucks, storage tanks, and distribution points.",
                "Communication Unit": "Emergency communication systems and equipment. Restore and maintain communication channels for coordination and public information.",
                "Coast Guard": "Maritime security and rescue services. Specialized in water-based emergencies, search and rescue, and maritime safety.",
                "Divers": "Underwater search and rescue specialists. Conduct submerged operations, evidence recovery, and underwater assessments.",
                "Contact Tracers": "Public health professionals for disease control and prevention. Track and monitor infectious disease spread and contacts.",
                "PPE Supplies": "Personal protective equipment including masks, gloves, and protective suits. Ensure safety of responders and prevent contamination.",
                "Vaccination Team": "Medical personnel for immunization and disease prevention. Administer vaccines and conduct public health interventions."
            }
            return purpose_map.get(resource_name, "Essential resource required for effective emergency response and incident management.")
        
        return purpose

class IncidentDialog(QDialog):
    """Dialog for creating/editing incidents."""
    
    def __init__(self, parent=None, incident_data=None):
        super().__init__(parent)
        self.incident_data = incident_data
        self.setWindowTitle("Incident Details")
        self.setModal(True)
        self.setMinimumWidth(500)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        form = QFormLayout()
        
        # Title
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter incident title...")
        if self.incident_data:
            self.title_input.setText(self.incident_data.get('title', ''))
        form.addRow("Title*:", self.title_input)
        
        # Type
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "Flood", "Earthquake", "Wildfire", "Road Accident", 
            "Train Derailment", "Chemical Spill", "Building Collapse",
            "Pandemic Cluster", "Terrorist Attack", "Industrial Fire",
            "Utility Failure", "Maritime Incident", "Other"
        ])
        if self.incident_data:
            self.type_combo.setCurrentText(self.incident_data.get('type', ''))
        form.addRow("Type*:", self.type_combo)
        
        # Severity
        self.severity_combo = QComboBox()
        self.severity_combo.addItems(["Low", "Medium", "High", "Critical"])
        if self.incident_data:
            self.severity_combo.setCurrentText(self.incident_data.get('severity', ''))
        form.addRow("Severity*:", self.severity_combo)
        
        # Location
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Enter location...")
        if self.incident_data:
            self.location_input.setText(self.incident_data.get('location', ''))
        form.addRow("Location*:", self.location_input)
        
        # Description
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Describe the incident in detail...")
        if self.incident_data:
            self.description_input.setText(self.incident_data.get('description', ''))
        form.addRow("Description*:", self.description_input)
        
        layout.addLayout(form)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("💾 Save Incident")
        save_button.clicked.connect(self.validate_and_save)
        save_button.setObjectName("primary-button")
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLineEdit, QComboBox, QTextEdit {
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: #f8f9fa;
            }
            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
                border-color: #3498db;
                background-color: white;
            }
            #primary-button {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
            }
            #primary-button:hover {
                background-color: #219653;
            }
        """)
    
    def validate_and_save(self):
        """Validate form before saving"""
        if not self.title_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Title is required.")
            return
        if not self.location_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Location is required.")
            return
        if not self.description_input.toPlainText().strip():
            QMessageBox.warning(self, "Validation Error", "Description is required.")
            return
        
        self.accept()
    
    def get_incident_data(self):
        """Get the incident data from the form."""
        data = {
            'title': self.title_input.text().strip(),
            'type': self.type_combo.currentText(),
            'severity': self.severity_combo.currentText(),
            'location': self.location_input.text().strip(),
            'description': self.description_input.toPlainText().strip(),
            'timestamp': datetime.now().isoformat(),
            'status': 'Active'
        }
        
        if self.incident_data and 'id' in self.incident_data:
            data['id'] = self.incident_data['id']
        
        return data

class IncidentManager:
    """Manager for incident data operations"""
    
    def __init__(self):
        self.data_file = os.path.join(current_dir, "..", "data", "incidents.json")
        self.incidents = []
        self.load_incidents()
    
    def load_incidents(self):
        """Load incidents from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    self.incidents = json.load(f)
                print(f"✅ Loaded {len(self.incidents)} incidents from {self.data_file}")
            else:
                self.incidents = []
                print("ℹ️ No existing incident data found. Starting fresh.")
        except Exception as e:
            logger.error(f"Error loading incidents: {e}")
            self.incidents = []
    
    def save_incidents(self):
        """Save incidents to JSON file"""
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, 'w') as f:
                json.dump(self.incidents, f, indent=2)
            logger.info(f"Saved {len(self.incidents)} incidents to {self.data_file}")
        except Exception as e:
            logger.error(f"Error saving incidents: {e}")
            raise
    
    def add_incident(self, incident_data):
        """Add new incident"""
        incident_id = f"inc_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        incident_data['id'] = incident_id
        incident_data['created_at'] = datetime.now().isoformat()
        self.incidents.append(incident_data)
        self.save_incidents()
        return incident_id
    
    def update_incident(self, incident_id, updated_data):
        """Update existing incident"""
        for incident in self.incidents:
            if incident.get('id') == incident_id:
                incident.update(updated_data)
                incident['updated_at'] = datetime.now().isoformat()
                self.save_incidents()
                return True
        return False
    
    def delete_incident(self, incident_id):
        """Delete incident by ID"""
        initial_count = len(self.incidents)
        self.incidents = [inc for inc in self.incidents if inc.get('id') != incident_id]
        if len(self.incidents) < initial_count:
            self.save_incidents()
            return True
        return False
    
    def get_all_incidents(self):
        """Get all incidents"""
        return self.incidents
    
    def search_incidents(self, search_text, type_filter, severity_filter):
        """Search and filter incidents"""
        filtered_incidents = []
        
        for incident in self.incidents:
            # Search filter
            if search_text and search_text.lower() not in incident.get('title', '').lower() and \
               search_text.lower() not in incident.get('description', '').lower() and \
               search_text.lower() not in incident.get('location', '').lower():
                continue
            
            # Type filter
            if type_filter != "All Types" and incident.get('type') != type_filter:
                continue
            
            # Severity filter
            if severity_filter != "All Severities" and incident.get('severity') != severity_filter:
                continue
            
            filtered_incidents.append(incident)
        
        return filtered_incidents

class IncidentWidget(QWidget):
    """Widget for managing incidents with AI predictions."""
    
    def __init__(self, auth_manager=None):
        super().__init__()
        self.auth_manager = auth_manager
        
        # Store AI diagnostics for detailed status display
        self.ai_diagnostics = ai_diagnostics
        
        # Initialize incident manager
        self.incident_manager = IncidentManager()
        
        # Initialize AI predictor with enhanced diagnostics
        self.ai_predictor = None
        self.ai_available = AI_AVAILABLE
        self.predicted_resources = {}  # Cache for predictions
        
        print(f"\n🎯 INITIALIZING INCIDENT WIDGET WITH AI: {'✅ ONLINE' if self.ai_available else '❌ OFFLINE'}")
        
        # Initialize AI predictor
        self.initialize_ai_predictor()
        
        # Show detailed AI status
        self.show_ai_status_details()
        
        self.setup_ui()
        self.load_incidents()

    def initialize_ai_predictor(self):
        """Initialize the AI predictor with proper error handling"""
        if self.ai_available:
            try:
                from ai.inference import DisasterAIPredictor
                self.ai_predictor = DisasterAIPredictor()
                print("✅ AI predictor initialized successfully")
                
                # Check if model is actually loaded
                if hasattr(self.ai_predictor, 'is_model_loaded'):
                    model_loaded = self.ai_predictor.is_model_loaded()
                    resource_map_loaded = self.ai_predictor.is_resource_map_loaded()
                    print(f"   • Model loaded: {model_loaded}")
                    print(f"   • Resource map loaded: {resource_map_loaded}")
                    
            except Exception as e:
                print(f"❌ Failed to initialize AI predictor: {e}")
                self.ai_available = False
                self.ai_predictor = DisasterAIPredictor()  # Use fallback
        else:
            # Use fallback predictor
            self.ai_predictor = DisasterAIPredictor()
            print("✅ Using fallback AI predictor (basic mode)")

    def show_ai_status_details(self):
        """Show detailed AI status information in console"""
        print(f"\n📋 DETAILED AI STATUS FOR INCIDENT WIDGET:")
        print(f"   • AI Available: {'✅ YES' if self.ai_available else '❌ NO'}")
        print(f"   • AI Reason: {self.ai_diagnostics.get('reason', 'Unknown')}")
        print(f"   • AI Predictor: {'✅ Initialized' if self.ai_predictor else '❌ Not available'}")
        
        if self.ai_predictor and hasattr(self.ai_predictor, 'is_model_loaded'):
            print(f"   • AI Model Loaded: {'✅ YES' if self.ai_predictor.is_model_loaded() else '❌ NO'}")
            print(f"   • Resource Map Loaded: {'✅ YES' if self.ai_predictor.is_resource_map_loaded() else '❌ NO'}")
        
        print("   • AI Details:")
        for key, value in self.ai_diagnostics.get('details', {}).items():
            status_icon = "✅" if value in ["Found", "Initialized", "Full AI"] else "⚠️" if value == "Fallback" else "❌"
            print(f"     {status_icon} {key}: {value}")

    def refresh_data(self):
        """Refresh incident data - called by main window after login"""
        print("🔄 Refreshing incident data...")
        
        # Clear AI predictions cache
        self.predicted_resources = {}
        
        # Reload incidents
        self.incident_manager.load_incidents()
        self.load_incidents()
        
        # Hide AI section
        if hasattr(self, 'ai_section'):
            self.ai_section.setVisible(False)
        
        print("✅ Incident data refreshed successfully")
    
    def clear_data(self):
        """Clear all data - useful for logout"""
        print("🧹 Clearing incident data...")
        
        # Clear table
        self.table.setRowCount(0)
        
        # Clear AI predictions cache
        self.predicted_resources = {}
        
        # Hide AI section
        if hasattr(self, 'ai_section'):
            self.ai_section.setVisible(False)
        
        print("✅ Incident data cleared")
    
    def setup_ui(self):
        """Initialize the incident management UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Header with AI status
        header = QFrame()
        header.setObjectName("page-header")
        header_layout = QHBoxLayout(header)
        
        title = QLabel("🚨 Incident Management")
        title.setObjectName("page-title")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        header_layout.addWidget(title)
        
        # AI status with detailed tooltip
        ai_status_text = "🤖 AI: Online" if self.ai_available else "🤖 AI: Offline"
        ai_status = QLabel(ai_status_text)
        ai_status.setStyleSheet(f"""
            color: {'#27ae60' if self.ai_available else '#e74c3c'}; 
            font-weight: bold; 
            padding: 8px 16px;
            background-color: {'#e8f5e8' if self.ai_available else '#fde8e8'};
            border-radius: 15px;
            border: 2px solid {'#27ae60' if self.ai_available else '#e74c3c'};
        """)
        
        # Set tooltip with detailed AI status
        tooltip_text = self.get_ai_status_tooltip()
        ai_status.setToolTip(tooltip_text)
        
        header_layout.addWidget(ai_status)
        
        header_layout.addStretch()
        
        # Add incident button
        add_button = QPushButton("📝 Report New Incident")
        add_button.setObjectName("primary-button")
        add_button.clicked.connect(self.show_incident_dialog)
        header_layout.addWidget(add_button)
        
        layout.addWidget(header)
        
        # Filters
        filter_frame = QFrame()
        filter_frame.setObjectName("filter-frame")
        filter_layout = QHBoxLayout(filter_frame)
        
        # Search
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search incidents by title, description, or location...")
        self.search_input.textChanged.connect(self.filter_incidents)
        filter_layout.addWidget(self.search_input)
        
        # Type filter
        self.type_filter = QComboBox()
        self.type_filter.addItems(["All Types", "Flood", "Earthquake", "Wildfire", 
                                 "Road Accident", "Chemical Spill", "Building Collapse",
                                 "Terrorist Attack", "Industrial Fire", "Utility Failure"])
        self.type_filter.currentTextChanged.connect(self.filter_incidents)
        filter_layout.addWidget(self.type_filter)
        
        # Severity filter
        self.severity_filter = QComboBox()
        self.severity_filter.addItems(["All Severities", "Low", "Medium", "High", "Critical"])
        self.severity_filter.currentTextChanged.connect(self.filter_incidents)
        filter_layout.addWidget(self.severity_filter)
        
        # Clear filters button
        clear_filters_btn = QPushButton("Clear Filters")
        clear_filters_btn.clicked.connect(self.clear_filters)
        clear_filters_btn.setObjectName("secondary-button")
        filter_layout.addWidget(clear_filters_btn)
        
        layout.addWidget(filter_frame)
        
        # Incident table
        self.table = QTableWidget()
        self.table.setColumnCount(7)  # Added AI column
        self.table.setHorizontalHeaderLabels([
            "Title", "Type", "Severity", "Location", "Time", "AI Status", "Actions"
        ])
        
        # Set column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Title
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Type
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Severity
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Location
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Time
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # AI Status
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Actions
        
        layout.addWidget(self.table)
        
        # AI RESOURCE PREDICTIONS SECTION
        self.ai_section = QGroupBox("🤖 AI Resource Predictions")
        self.ai_section.setVisible(False)  # Hidden until incident selected
        self.ai_section.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                margin-top: 15px;
                padding-top: 20px;
                border: 2px solid #3498db;
                border-radius: 10px;
                background-color: #f8f9fa;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 12px 0 12px;
                color: #3498db;
                font-size: 14pt;
            }
        """)
        ai_layout = QVBoxLayout(self.ai_section)
        
        # Selected incident info
        self.selected_incident_label = QLabel("Select an incident to view AI recommendations")
        self.selected_incident_label.setWordWrap(True)
        self.selected_incident_label.setStyleSheet("""
            padding: 12px; 
            background-color: white; 
            border-radius: 6px;
            border: 1px solid #bdc3c7;
            font-size: 11pt;
        """)
        ai_layout.addWidget(self.selected_incident_label)
        
        # AI predictions table
        self.ai_predictions_table = QTableWidget()
        self.ai_predictions_table.setColumnCount(3)
        self.ai_predictions_table.setHorizontalHeaderLabels(["Resource", "Priority", "Purpose"])
        
        # Set better column widths for AI predictions table
        self.ai_predictions_table.setColumnWidth(0, 200)  # Resource
        self.ai_predictions_table.setColumnWidth(1, 150)  # Priority
        self.ai_predictions_table.horizontalHeader().setStretchLastSection(True)  # Purpose
        
        # Style AI predictions table
        self.ai_predictions_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #ecf0f1;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        ai_layout.addWidget(self.ai_predictions_table)
        
        # AI action buttons
        ai_buttons_layout = QHBoxLayout()
        
        self.analyze_btn = QPushButton("🔍 Analyze with AI")
        self.analyze_btn.clicked.connect(self.analyze_selected_incident)
        self.analyze_btn.setVisible(False)
        self.analyze_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
        """)
        
        self.view_details_btn = QPushButton("📋 View Detailed Recommendations")
        self.view_details_btn.clicked.connect(self.show_ai_details)
        self.view_details_btn.setVisible(False)
        self.view_details_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 10px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #219653;
            }
        """)
        
        ai_buttons_layout.addWidget(self.analyze_btn)
        ai_buttons_layout.addWidget(self.view_details_btn)
        ai_buttons_layout.addStretch()
        
        ai_layout.addLayout(ai_buttons_layout)
        
        layout.addWidget(self.ai_section)
        
        # Connect table selection
        self.table.itemSelectionChanged.connect(self.on_incident_selected)
        
        # Set stylesheet
        self.setStyleSheet("""
            #page-header {
                background-color: white;
                padding: 15px;
                border-radius: 8px;
                border: 1px solid #bdc3c7;
            }
            #filter-frame {
                background-color: white;
                border-radius: 8px;
                margin: 5px;
                padding: 12px;
                border: 1px solid #bdc3c7;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: #f8f9fa;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #3498db;
                background-color: white;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 8px;
                margin: 5px;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #ecf0f1;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 12px 8px;
                border: none;
                font-weight: bold;
            }
            #primary-button {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12pt;
            }
            #primary-button:hover {
                background-color: #c0392b;
            }
            #secondary-button {
                background-color: #95a5a6;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            #secondary-button:hover {
                background-color: #7f8c8d;
            }
            .action-button {
                background-color: #f8f9fa;
                color: #2c3e50;
                border: 1px solid #bdc3c7;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 10pt;
            }
            .action-button:hover {
                background-color: #3498db;
                color: white;
                border-color: #3498db;
            }
        """)
    
    def get_ai_status_tooltip(self):
        """Generate detailed AI status tooltip"""
        tooltip = "AI Status Details:\n\n"
        
        if self.ai_available:
            tooltip += "✅ AI System: ONLINE\n"
            tooltip += f"📊 Mode: {self.ai_diagnostics.get('details', {}).get('mode', 'Unknown')}\n"
            tooltip += f"🔧 Predictor: {self.ai_diagnostics.get('details', {}).get('predictor_status', 'Unknown')}\n"
        else:
            tooltip += "❌ AI System: OFFLINE\n"
            tooltip += f"📋 Reason: {self.ai_diagnostics.get('reason', 'Unknown')}\n"
        
        # Add file status details
        tooltip += "\n📁 File Status:\n"
        details = self.ai_diagnostics.get('details', {})
        for key, value in details.items():
            if key in ['severity_model', 'resource_map']:
                status_icon = "✅" if value == "Found" else "❌"
                tooltip += f"  {status_icon} {key}: {value}\n"
        
        return tooltip
    
    def on_incident_selected(self):
        """Handle incident selection in table"""
        selected_items = self.table.selectedItems()
        if not selected_items:
            self.ai_section.setVisible(False)
            return
            
        row = selected_items[0].row()
        
        # Get incident data from table
        incident_title = self.table.item(row, 0).text()
        incident_type = self.table.item(row, 1).text()
        incident_severity = self.table.item(row, 2).text()
        incident_location = self.table.item(row, 3).text()
        
        # Find the actual incident data
        incident_id = None
        for incident in self.incident_manager.get_all_incidents():
            if (incident.get('title') == incident_title and 
                incident.get('type') == incident_type and
                incident.get('location') == incident_location):
                incident_id = incident.get('id')
                break
        
        # Store selected incident data
        self.selected_incident = {
            'id': incident_id,
            'row': row,
            'title': incident_title,
            'type': incident_type,
            'severity': incident_severity,
            'location': incident_location
        }
        
        # Update AI section
        self.selected_incident_label.setText(
            f"<b>Selected Incident:</b> {incident_title}<br>"
            f"<b>Type:</b> {incident_type} | <b>Severity:</b> {incident_severity} | <b>Location:</b> {incident_location}"
        )
        
        # Check if we already have AI predictions
        if incident_id and incident_id in self.predicted_resources:
            self.show_ai_predictions(incident_id)
            self.analyze_btn.setVisible(False)
            self.view_details_btn.setVisible(True)
        else:
            self.ai_predictions_table.setRowCount(0)
            self.analyze_btn.setVisible(True)
            self.view_details_btn.setVisible(False)
        
        self.ai_section.setVisible(True)
    
    def analyze_selected_incident(self):
        """Analyze selected incident with AI"""
        if not hasattr(self, 'selected_incident'):
            QMessageBox.warning(self, "No Selection", "Please select an incident first.")
            return
            
        incident_data = {
            'id': self.selected_incident['id'],
            'type': self.selected_incident['type'],
            'severity': self.selected_incident['severity'],
            'title': self.selected_incident['title']
        }
        
        if self.ai_predictor:
            print(f"🔍 Starting AI analysis for incident: {self.selected_incident['title']}")
            self.analyze_btn.setText("⏳ Analyzing...")
            self.analyze_btn.setEnabled(False)
            
            # Show progress dialog
            progress = QProgressDialog("AI is analyzing the incident...", "Cancel", 0, 0, self)
            progress.setWindowTitle("AI Analysis")
            progress.setModal(True)
            progress.show()
            
            # Start AI prediction in background
            self.ai_worker = AIWorker(incident_data, self.ai_predictor)
            self.ai_worker.prediction_finished.connect(lambda result: self.on_ai_analysis_complete(result, progress))
            self.ai_worker.start()
        else:
            QMessageBox.warning(self, "AI Not Available", 
                              "AI analysis is not available. Please check if AI models are properly installed.")
    
    def on_ai_analysis_complete(self, result, progress):
        """Handle completed AI analysis"""
        progress.close()
        self.analyze_btn.setText("🔍 Analyze with AI")
        self.analyze_btn.setEnabled(True)
        
        resources = result.get('resources', [])
        error = result.get('error')
        incident_id = result.get('incident_id')
        
        if error:
            print(f"❌ AI analysis failed: {error}")
            QMessageBox.warning(self, "AI Analysis Failed", 
                              f"AI analysis failed: {error}\nUsing fallback recommendations.")
            # Use fallback
            resources = self.ai_predictor.recommend_resources(
                self.selected_incident['type'],
                self.selected_incident['severity']
            ) if self.ai_predictor else []
        else:
            print(f"✅ AI analysis completed successfully. Found {len(resources)} resource recommendations.")
        
        # Store predictions
        if incident_id:
            self.predicted_resources[incident_id] = resources
            
            # Update AI status in main table
            ai_status_item = QTableWidgetItem("✅ AI Ready")
            ai_status_item.setBackground(QColor(220, 255, 220))
            self.table.setItem(self.selected_incident['row'], 5, ai_status_item)
            
            # Show predictions
            self.show_ai_predictions(incident_id)
            self.analyze_btn.setVisible(False)
            self.view_details_btn.setVisible(True)
    
    def show_ai_predictions(self, incident_id):
        """Show AI predictions in the table with enhanced display"""
        resources = self.predicted_resources[incident_id]
        self.ai_predictions_table.setRowCount(len(resources))
        
        for row, resource in enumerate(resources):
            # Resource name
            resource_item = QTableWidgetItem(resource['resource'])
            resource_item.setToolTip(resource['resource'])  # Tooltip for full name
            self.ai_predictions_table.setItem(row, 0, resource_item)
            
            # Priority with enhanced text and color coding
            priority_num = resource['priority']
            priority_text = self.get_priority_text(priority_num)
            priority_item = QTableWidgetItem(priority_text)
            
            # Color coding based on priority
            if priority_num == 1:
                priority_item.setBackground(QColor(231, 76, 60))  # Red
                priority_item.setForeground(QBrush(QColor(255, 255, 255)))
            elif priority_num == 2:
                priority_item.setBackground(QColor(230, 126, 34))  # Orange
                priority_item.setForeground(QBrush(QColor(255, 255, 255)))
            elif priority_num == 3:
                priority_item.setBackground(QColor(241, 196, 15))  # Yellow
            else:
                priority_item.setBackground(QColor(46, 204, 113))  # Green
                priority_item.setForeground(QBrush(QColor(255, 255, 255)))
                
            priority_item.setToolTip(f"Priority Level: {priority_num} - {priority_text}")
            self.ai_predictions_table.setItem(row, 1, priority_item)
            
            # Enhanced purpose with fallback descriptions
            purpose = resource.get('purpose', '')
            if not purpose or purpose == 'No description available':
                purpose = self.get_default_purpose(resource['resource'])
            
            purpose_item = QTableWidgetItem(purpose)
            purpose_item.setToolTip(purpose)  # Show full purpose on hover
            self.ai_predictions_table.setItem(row, 2, purpose_item)
    
    def get_priority_text(self, priority):
        """Convert priority number to meaningful text"""
        priority_map = {
            1: "CRITICAL",
            2: "HIGH", 
            3: "MEDIUM",
            4: "LOW",
            5: "MINIMAL"
        }
        return priority_map.get(priority, f"P{priority}")
    
    def get_default_purpose(self, resource_name):
        """Get default purpose description for resources"""
        purpose_map = {
            "Life Jackets": "Personal flotation devices for water safety and rescue operations",
            "Emergency Shelter": "Temporary housing facilities for displaced individuals",
            "Medical Team": "Emergency medical professionals for immediate healthcare",
            "Water Purification": "Systems and equipment for clean drinking water supply",
            "Rescue Boats": "Watercraft for search and rescue in flooded areas",
            "Search & Rescue": "Specialized teams for locating and extracting individuals",
            "Structural Engineers": "Building safety assessment and stability evaluation",
            "Heavy Equipment": "Machinery for debris removal and access creation",
            "Firefighters": "Trained personnel for fire suppression and rescue",
            "Helicopters": "Aircraft for aerial reconnaissance and transport",
            "Evacuation Team": "Personnel for organizing safe population relocations",
            "Hazmat Team": "Specialists for hazardous materials handling",
            "Decontamination Unit": "Facilities for cleaning and safety procedures",
            "Emergency Medical": "Mobile medical units for immediate healthcare",
            "Fire Department": "Comprehensive fire and emergency response services",
            "Police": "Law enforcement for security and public safety",
            "Tow Truck": "Vehicle recovery and road clearance services",
            "SWAT Team": "Tactical units for high-risk situations",
            "Bomb Squad": "Explosive device disposal specialists",
            "Crisis Counselors": "Mental health and trauma support professionals",
            "Utility Repair Crew": "Technicians for restoring essential services",
            "Emergency Generator": "Backup power supply systems",
            "Water Distribution": "Clean water distribution systems",
            "Communication Unit": "Emergency communication restoration",
            "Coast Guard": "Maritime emergency response services",
            "Divers": "Underwater search and rescue specialists",
            "Contact Tracers": "Disease spread monitoring professionals",
            "PPE Supplies": "Safety equipment for emergency responders",
            "Vaccination Team": "Immunization and preventative care services"
        }
        return purpose_map.get(resource_name, "Essential emergency response resource")
    
    def show_ai_details(self):
        """Show detailed AI recommendations dialog"""
        if hasattr(self, 'selected_incident') and self.selected_incident['id'] in self.predicted_resources:
            resources = self.predicted_resources[self.selected_incident['id']]
            dialog = AIRecommendationsDialog(resources, self)
            dialog.exec_()
        else:
            QMessageBox.information(self, "AI Recommendations", 
                                  "AI analysis not yet completed for this incident.\nPlease analyze the incident first.")
    
    def show_incident_dialog(self, incident_data=None):
        """Show dialog for creating/editing incidents."""
        dialog = IncidentDialog(self, incident_data)
        if dialog.exec_() == QDialog.Accepted:
            incident_data = dialog.get_incident_data()
            self.save_incident(incident_data)
    
    def save_incident(self, incident_data):
        """Save incident data"""
        try:
            if 'id' in incident_data:
                # Update existing incident
                success = self.incident_manager.update_incident(incident_data['id'], incident_data)
                action = "updated"
            else:
                # Create new incident
                incident_id = self.incident_manager.add_incident(incident_data)
                success = bool(incident_id)
                action = "created"
            
            if success:
                QMessageBox.information(self, "Success", f"Incident {action} successfully!")
                self.load_incidents()
            else:
                QMessageBox.warning(self, "Error", f"Failed to {action} incident")
                
        except Exception as e:
            logger.error(f"Error saving incident: {e}")
            QMessageBox.critical(self, "Error", f"Failed to save incident: {str(e)}")
    
    def load_incidents(self):
        """Load incidents from the backend"""
        try:
            incidents = self.incident_manager.get_all_incidents()
            self.update_table(incidents)
        except Exception as e:
            logger.error(f"Error loading incidents: {e}")
            QMessageBox.critical(self, "Error", f"Failed to load incidents: {str(e)}")
    
    def update_table(self, incidents):
        """Update the incident table with data"""
        self.table.setRowCount(0)
        for incident in incidents:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Add incident data
            self.table.setItem(row, 0, QTableWidgetItem(incident.get('title', 'N/A')))
            self.table.setItem(row, 1, QTableWidgetItem(incident.get('type', 'N/A')))
            
            # Severity with color coding
            severity_item = QTableWidgetItem(incident.get('severity', 'Medium'))
            severity = incident.get('severity', 'Medium')
            if severity == 'Critical':
                severity_item.setBackground(QColor(231, 76, 60))  # Red
                severity_item.setForeground(QBrush(QColor(255, 255, 255)))
            elif severity == 'High':
                severity_item.setBackground(QColor(230, 126, 34))  # Orange
                severity_item.setForeground(QBrush(QColor(255, 255, 255)))
            elif severity == 'Medium':
                severity_item.setBackground(QColor(241, 196, 15))  # Yellow
            else:  # Low
                severity_item.setBackground(QColor(46, 204, 113))  # Green
                severity_item.setForeground(QBrush(QColor(255, 255, 255)))
            self.table.setItem(row, 2, severity_item)
            
            self.table.setItem(row, 3, QTableWidgetItem(incident.get('location', 'N/A')))
            
            # Format timestamp
            timestamp = incident.get('timestamp', '')
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    time_str = dt.strftime("%Y-%m-%d %H:%M")
                except:
                    time_str = timestamp
            else:
                time_str = "Unknown"
            self.table.setItem(row, 4, QTableWidgetItem(time_str))
            
            # AI Status column
            incident_id = incident.get('id')
            if incident_id and incident_id in self.predicted_resources:
                ai_status_item = QTableWidgetItem("✅ AI Ready")
                ai_status_item.setBackground(QColor(220, 255, 220))
            else:
                ai_status_item = QTableWidgetItem("🤖 Click to analyze")
                ai_status_item.setBackground(QColor(255, 255, 200))
            self.table.setItem(row, 5, ai_status_item)
            
            # Add action buttons
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(4, 4, 4, 4)
            
            edit_btn = QPushButton("✏️ Edit")
            edit_btn.setObjectName("action-button")
            edit_btn.clicked.connect(lambda checked, i=incident: self.show_incident_dialog(i))
            
            delete_btn = QPushButton("🗑️ Delete")
            delete_btn.setObjectName("action-button")
            delete_btn.clicked.connect(lambda checked, r=row: self.delete_incident(r))
            
            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)
            
            self.table.setCellWidget(row, 6, action_widget)
    
    def filter_incidents(self):
        """Filter incidents based on search and filters"""
        search_text = self.search_input.text()
        type_filter = self.type_filter.currentText()
        severity_filter = self.severity_filter.currentText()
        
        filtered_incidents = self.incident_manager.search_incidents(
            search_text, type_filter, severity_filter
        )
        
        self.update_table(filtered_incidents)
    
    def clear_filters(self):
        """Clear all filters"""
        self.search_input.clear()
        self.type_filter.setCurrentIndex(0)
        self.severity_filter.setCurrentIndex(0)
        self.filter_incidents()
    
    def delete_incident(self, row):
        """Delete an incident"""
        # Get incident ID from the table
        incident_title = self.table.item(row, 0).text()
        incident_type = self.table.item(row, 1).text()
        incident_location = self.table.item(row, 3).text()
        
        # Find the incident in the manager
        incident_id = None
        for incident in self.incident_manager.get_all_incidents():
            if (incident.get('title') == incident_title and 
                incident.get('type') == incident_type and
                incident.get('location') == incident_location):
                incident_id = incident.get('id')
                break
        
        if not incident_id:
            QMessageBox.warning(self, "Error", "Could not find incident to delete.")
            return
        
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete incident '{incident_title}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                if self.incident_manager.delete_incident(incident_id):
                    # Remove from AI predictions cache
                    if incident_id in self.predicted_resources:
                        del self.predicted_resources[incident_id]
                    
                    self.load_incidents()
                    QMessageBox.information(self, "Success", "Incident deleted successfully!")
                else:
                    QMessageBox.warning(self, "Error", "Failed to delete incident")
            except Exception as e:
                logger.error(f"Error deleting incident: {e}")
                QMessageBox.critical(self, "Error", f"Failed to delete incident: {str(e)}")

if __name__ == "__main__":
    # Test the widget
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    widget = IncidentWidget()
    widget.show()
    sys.exit(app.exec_())