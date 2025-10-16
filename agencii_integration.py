"""
Agencii.ai Integration for BuyBlack City Guide
This module handles deployment and integration with the Agencii.ai platform
"""

import os
import requests
import json
from typing import Dict, Any, Optional
from agency import create_agency

class AgenciiIntegration:
    """Handle Agencii.ai platform integration"""
    
    def __init__(self):
        self.api_key = os.getenv('AGENCII_API_KEY')
        self.base_url = os.getenv('AGENCII_BASE_URL', 'https://api.agencii.ai')
        self.agency_id = None
        
    def authenticate(self) -> bool:
        """Authenticate with Agencii.ai"""
        if not self.api_key:
            print("❌ AGENCII_API_KEY not found in environment variables")
            return False
            
        headers = {'Authorization': f'Bearer {self.api_key}'}
        try:
            response = requests.get(f'{self.base_url}/auth/verify', headers=headers)
            if response.status_code == 200:
                print("✅ Successfully authenticated with Agencii.ai")
                return True
            else:
                print(f"❌ Authentication failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False
    
    def deploy_agency(self) -> Optional[str]:
        """Deploy the BuyBlack City Guide agency to Agencii.ai"""
        if not self.authenticate():
            return None
            
        agency_config = {
            'name': 'BuyBlack City Guide',
            'description': 'AI-powered city guide for discovering Black-owned businesses and cultural experiences',
            'version': '1.0.0',
            'environment': 'production',
            'agents': [
                {
                    'name': 'City Explorer',
                    'role': 'Business discovery and location-based recommendations',
                    'tools': ['BuyBlackDirectorySearch', 'LandmarkDiscovery']
                },
                {
                    'name': 'Itinerary Planner', 
                    'role': 'Trip planning and scheduling',
                    'tools': ['ItineraryBuilder']
                },
                {
                    'name': 'Cultural Curator',
                    'role': 'Cultural context and storytelling',
                    'tools': ['CulturalStoryFetcher']
                }
            ],
            'capabilities': [
                'Black-owned business discovery',
                'Cultural landmark identification',
                'Personalized itinerary creation',
                'Cultural storytelling',
                'Multi-city support'
            ],
            'webhook_url': os.getenv('WEBHOOK_URL', ''),
            'scaling': {
                'min_instances': 1,
                'max_instances': 10,
                'auto_scale': True
            },
            'features': {
                'webhook_support': True,
                'api_endpoints': True,
                'custom_domain': True,
                'analytics': True
            }
        }
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(
                f'{self.base_url}/agencies',
                json=agency_config,
                headers=headers
            )
            
            if response.status_code == 201:
                result = response.json()
                self.agency_id = result.get('id')
                print(f"✅ Agency deployed successfully! ID: {self.agency_id}")
                print(f"🌐 Agency URL: {result.get('url', 'N/A')}")
                return self.agency_id
            else:
                print(f"❌ Deployment failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Deployment error: {e}")
            return None
    
    def get_agency_status(self) -> Optional[Dict[str, Any]]:
        """Get the status of your deployed agency"""
        if not self.agency_id:
            print("❌ No agency ID found. Deploy agency first.")
            return None
            
        headers = {'Authorization': f'Bearer {self.api_key}'}
        
        try:
            response = requests.get(
                f'{self.base_url}/agencies/{self.agency_id}',
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to get agency status: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error getting agency status: {e}")
            return None
    
    def update_agency(self, updates: Dict[str, Any]) -> bool:
        """Update agency configuration"""
        if not self.agency_id:
            print("❌ No agency ID found. Deploy agency first.")
            return False
            
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.patch(
                f'{self.base_url}/agencies/{self.agency_id}',
                json=updates,
                headers=headers
            )
            
            if response.status_code == 200:
                print("✅ Agency updated successfully!")
                return True
            else:
                print(f"❌ Update failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Update error: {e}")
            return False
    
    def get_analytics(self) -> Optional[Dict[str, Any]]:
        """Get agency usage analytics"""
        if not self.agency_id:
            print("❌ No agency ID found. Deploy agency first.")
            return None
            
        headers = {'Authorization': f'Bearer {self.api_key}'}
        
        try:
            response = requests.get(
                f'{self.base_url}/agencies/{self.agency_id}/analytics',
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to get analytics: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error getting analytics: {e}")
            return None
    
    def deploy_multiple_cities(self, cities: list) -> Dict[str, str]:
        """Deploy agency instances for multiple cities"""
        results = {}
        
        for city in cities:
            print(f"🚀 Deploying agency for {city}...")
            
            # Create city-specific configuration
            city_config = {
                'name': f'BuyBlack City Guide - {city}',
                'description': f'AI-powered city guide for discovering Black-owned businesses in {city}',
                'city': city,
                'parent_agency_id': self.agency_id
            }
            
            # Deploy city instance
            city_agency_id = self.deploy_city_instance(city_config)
            if city_agency_id:
                results[city] = city_agency_id
                print(f"✅ {city} agency deployed: {city_agency_id}")
            else:
                print(f"❌ Failed to deploy {city} agency")
                
        return results
    
    def deploy_city_instance(self, city_config: Dict[str, Any]) -> Optional[str]:
        """Deploy a city-specific agency instance"""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(
                f'{self.base_url}/agencies',
                json=city_config,
                headers=headers
            )
            
            if response.status_code == 201:
                result = response.json()
                return result.get('id')
            else:
                print(f"❌ City deployment failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ City deployment error: {e}")
            return None

def main():
    """Main function to demonstrate Agencii.ai integration"""
    print("🚀 BuyBlack City Guide - Agencii.ai Integration")
    print("=" * 50)
    
    # Initialize integration
    agencii = AgenciiIntegration()
    
    # Authenticate
    if not agencii.authenticate():
        print("❌ Please set AGENCII_API_KEY environment variable")
        return
    
    # Deploy main agency
    agency_id = agencii.deploy_agency()
    if not agency_id:
        print("❌ Failed to deploy agency")
        return
    
    # Get status
    status = agencii.get_agency_status()
    if status:
        print(f"📊 Agency Status: {status.get('status', 'Unknown')}")
        print(f"🌐 Agency URL: {status.get('url', 'N/A')}")
    
    # Deploy multiple cities
    cities = ['Oakland', 'Atlanta', 'Chicago', 'Detroit', 'Houston']
    city_agencies = agencii.deploy_multiple_cities(cities)
    
    print("\n🎉 Integration Complete!")
    print(f"Main Agency ID: {agency_id}")
    print(f"City Agencies: {city_agencies}")

if __name__ == "__main__":
    main()

