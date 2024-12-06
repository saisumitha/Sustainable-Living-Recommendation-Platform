import pandas as pd
from sklearn.neighbors import NearestNeighbors
from .models import Recommendation
# Load the dataset from recommendations.csv
data = pd.read_csv(r'C:\Users\ACER\OneDrive_Amrita_university\Desktop\Sustainable_platform\Sustainable_platform\recommendations\recommendations.csv')

# Check the first few rows of the dataset to verify
print(data.head())

# Create a feature matrix for recommendations (e.g., category, difficulty, and carbon_saved)
X = pd.get_dummies(data[['category', 'difficulty', 'carbon_saved']])

# Train the NearestNeighbors model
model = NearestNeighbors(n_neighbors=3)
model.fit(X)

def recommend(user_id):
    recommendations = Recommendation.objects.filter(user_id=user_id)

    # Convert to DataFrame
    data = pd.DataFrame(list(recommendations.values('user', 'category', 'difficulty', 'carbon_saved')))

    # Ensure correct columns for the feature matrix
    X = pd.get_dummies(data[['category', 'difficulty', 'carbon_saved']])

    # Use NearestNeighbors to find similar recommendations
    model = NearestNeighbors(n_neighbors=3)
    model.fit(X)

    # Get similar recommendations for the current user
    user_data = data[data['user'] == user_id]
    recommended_ids = []

    for _, row in user_data.iterrows():
        distances, indices = model.kneighbors([X.iloc[row.name].values])
        for index in indices[0]:
            recommended_ids.append(data.iloc[index]['recommendation_id'])

    # Return recommended recommendation_ids
    return recommended_ids
