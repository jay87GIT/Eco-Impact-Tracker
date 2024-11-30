from datetime import datetime
from app import db

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    carbon_impact = db.Column(db.Float)  # in kg CO2
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Activity categories
    TRANSPORT = 'transport'
    ENERGY = 'energy'
    FOOD = 'food'
    WASTE = 'waste'
    
    @staticmethod
    def calculate_carbon_impact(category, data):
        """Calculate carbon impact based on activity category and data"""
        impacts = {
            'transport': {
                'car': 0.2,  # kg CO2 per km
                'bus': 0.08,
                'train': 0.04,
                'bike': 0,
                'walk': 0
            },
            'energy': {
                'electricity': 0.5,  # kg CO2 per kWh
                'gas': 0.2,
                'renewable': 0
            },
            'food': {
                'meat': 6.0,  # kg CO2 per meal
                'vegetarian': 2.5,
                'vegan': 1.5
            },
            'waste': {
                'recycle': -0.5,  # kg CO2 saved per kg
                'compost': -0.2,
                'landfill': 0.5
            }
        }
        return impacts.get(category, {}).get(data, 0)
