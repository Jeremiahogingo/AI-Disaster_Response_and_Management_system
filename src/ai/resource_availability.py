# src/ai/resource_availability.py
import json
from datetime import datetime, timedelta
import os

class ResourceManager:
    def __init__(self, resource_map_path=None):
        # Set default path if not provided
        if resource_map_path is None:
            resource_map_path = os.path.join(os.path.dirname(__file__), 'models', 'resource_map.json')
        
        self.resource_map_path = resource_map_path
        
        # Load resource map
        if os.path.exists(resource_map_path):
            try:
                with open(resource_map_path, 'r', encoding='utf-8') as f:
                    self.resource_map = json.load(f)
                print(f"SUCCESS: Resource map loaded from {resource_map_path}")
            except Exception as e:
                self.resource_map = {"event_type_map": {}, "severity_map": {}}
                print(f"ERROR: Error loading resource map: {e}")
        else:
            self.resource_map = {"event_type_map": {}, "severity_map": {}}
            print(f"WARNING: Resource map not found at {resource_map_path}")
        
        self.allocated_resources = {}
        self.available_resources = self._initialize_availability()
    
    def _initialize_availability(self):
        """Initialize resource availability based on region/capacity"""
        availability = {}
        # This would typically load from a database
        for event_type, resources in self.resource_map.get("event_type_map", {}).items():
            for resource in resources:
                resource_name = resource["resource"]
                availability[resource_name] = {
                    "total": self._get_default_quantity(resource),
                    "allocated": 0,
                    "maintenance": 0,
                    "available": self._get_default_quantity(resource)
                }
        return availability
    
    def _get_default_quantity(self, resource):
        """Extract default quantity from resource definition"""
        quantity_str = resource.get("quantity", "1 unit")
        # Parse quantity string like "5-10 units" to get max
        if "-" in quantity_str:
            return int(quantity_str.split("-")[1].split()[0])
        return 1
    
    def check_availability(self, resource_name, quantity_needed=1):
        """Check if resources are available"""
        if resource_name not in self.available_resources:
            return False
        
        available = (self.available_resources[resource_name]["total"] - 
                    self.available_resources[resource_name]["allocated"] -
                    self.available_resources[resource_name]["maintenance"])
        
        return available >= quantity_needed
    
    def allocate_resources(self, incident_id, resources_needed):
        """Allocate resources to an incident"""
        allocations = []
        for resource in resources_needed:
            resource_name = resource["resource"]
            quantity = resource.get("quantity", 1)
            
            if self.check_availability(resource_name, quantity):
                # Mark as allocated
                self.available_resources[resource_name]["allocated"] += quantity
                self.available_resources[resource_name]["available"] -= quantity
                allocations.append(resource)
        
        self.allocated_resources[incident_id] = {
            "resources": allocations,
            "timestamp": datetime.now().isoformat()
        }
        return allocations
    
    def release_resources(self, incident_id):
        """Release resources back to available pool"""
        if incident_id in self.allocated_resources:
            for resource in self.allocated_resources[incident_id]["resources"]:
                resource_name = resource["resource"]
                quantity = resource.get("quantity", 1)
                
                if resource_name in self.available_resources:
                    self.available_resources[resource_name]["allocated"] -= quantity
                    self.available_resources[resource_name]["available"] += quantity
                    
            del self.allocated_resources[incident_id]
            print(f"SUCCESS: Resources released for incident {incident_id}")
    
    def get_available_resources(self):
        """Get current availability of all resources"""
        return {name: data["available"] for name, data in self.available_resources.items()}
    
    def get_resource_categories(self):
        """Get resource categories from resource map"""
        return self.resource_map.get("resource_categories", {})
    
    def get_response_times(self):
        """Get response time categories from resource map"""
        return self.resource_map.get("response_times", {})

# Example usage
if __name__ == "__main__":
    print("TESTING: Testing Resource Manager...")
    manager = ResourceManager()
    print(f"Available resources: {len(manager.available_resources)}")
    print(f"Resource categories: {list(manager.get_resource_categories().keys())}")