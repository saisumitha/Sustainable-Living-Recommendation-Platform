import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Sustainable_platform.settings')  # Replace with your project name
django.setup()

import csv
from recommendations.models import Recommendation, Category  # Import models

def map_difficulty(difficulty_str):
    """Map string difficulty values to numeric values."""
    mapping = {
        'Easy': 1,
        'Medium': 2,
        'Hard': 3
    }
    return mapping.get(difficulty_str, 0)  # Default to 0 if no match

def run():
    with open('data/recommendations.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Get or create the category
            category_name = row['category']  # Assuming the category name is in the CSV
            category, created = Category.objects.get_or_create(name=category_name)

            # Map difficulty to numeric value
            difficulty_numeric = map_difficulty(row['difficulty'])

            # Create the recommendation
            Recommendation.objects.create(
                title=row['title'],
                description=row['description'],
                category=category,
                impact=row['impact'],
                difficulty=difficulty_numeric,
                carbon_saved=row['carbon_saved']
            )
    print("Data imported successfully!")

if __name__ == '__main__':
    run()
