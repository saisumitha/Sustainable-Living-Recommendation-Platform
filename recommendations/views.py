from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse
from .models import UserProfile, Recommendation, Category, SavedRecommendation, CompletedRecommendation
from .forms import RegisterForm
import json
from django import forms
from django.shortcuts import get_object_or_404
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


# Registration View
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user to the database
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1") 
            user = authenticate(username=username, password=password)  # Authenticate the user
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {username}! Your account has been created.")
                return redirect("dashboard")  # Redirect to the dashboard
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


# Dashboard View
@login_required
def dashboard(request):
    user = request.user
    categories = Category.objects.all()
    saved_recommendations = SavedRecommendation.objects.filter(user=user)

    # Prepare data for the chart
    months = []
    carbon_savings = []
    total_carbon_reduced = 0  # Initialize total carbon reduced

    for saved in saved_recommendations:
        month_year = saved.saved_at.strftime('%b %Y')  # Extract month/year from saved_at
        if month_year not in months:
            months.append(month_year)

        recommendation = saved.recommendation
        carbon_saved = float(recommendation.carbon_saved)
        carbon_savings.append(carbon_saved)

        if saved.completed:
            total_carbon_reduced += carbon_saved  # Add carbon saved if recommendation is completed

    total_recommendations = saved_recommendations.count()
    completed_recommendations = saved_recommendations.filter(completed=True).count()

    context = {
        'months': json.dumps(months),
        'carbon_savings': json.dumps(carbon_savings),
        'total_carbon_reduced': total_carbon_reduced,  # Pass total carbon reduced to template
        'completed_recommendations': completed_recommendations,
        'total_recommendations': total_recommendations,
        'categories': categories,
    }

    return render(request, 'dashboard.html', context)



# Home View
def home(request):
    return render(request, 'home.html')


# Recommendations View
def recommendations(request):
    # Fetch all recommendations from the database
    recommendations = Recommendation.objects.all()
    return render(request, 'recommendations.html', {'recommendations': recommendations})


# User Profile View
@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def saved(request):
    if request.method == 'POST':
        try:
            # Parse JSON body from the AJAX request
            data = json.loads(request.body)
            recommendation_id = data.get('recommendation_id')

            # Check if the recommendation exists
            recommendation = Recommendation.objects.get(id=recommendation_id)

            # Check if the recommendation is already saved
            saved_rec, created = SavedRecommendation.objects.get_or_create(
                user=request.user,
                recommendation=recommendation,
                defaults={'progress': 0}  # Initialize progress if saving
            )

            if created:
                return JsonResponse({'message': f"Recommendation '{recommendation.title}' saved successfully!"})
            else:
                return JsonResponse({'message': f"The recommendation '{recommendation.title}' is already in your saved list."})
        except Recommendation.DoesNotExist:
            return JsonResponse({'error': 'Recommendation not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # For GET requests, render the saved recommendations page
    saved_recommendations = SavedRecommendation.objects.filter(user=request.user).select_related('recommendation')
    return render(request, 'saved.html', {'saved_recommendations': saved_recommendations})

@login_required
def settings(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'settings.html', {'form': form})


@login_required
def tracker(request):
    # Get the current logged-in user
    user = request.user
    saved_recommendations = SavedRecommendation.objects.all()

    # Get total goals (saved recommendations) for the current user
    total_goals = SavedRecommendation.objects.filter(user=user).count()

    # Get completed goals (recommendations marked as completed) for the current user
    completed_goals = SavedRecommendation.objects.filter(user=user, completed=True).count()

    # Calculate progress rate
    if total_goals > 0:
        progress_rate = (completed_goals / total_goals) * 100
    else:
        progress_rate = 0

    # Get completed recommendations for the tracker page
    completed_recommendations = SavedRecommendation.objects.filter(user=user, completed=True)

    context = {
        'total_goals': total_goals,
        'completed_goals': completed_goals,
        'progress_rate': progress_rate,
        'completed_recommendations': completed_recommendations,
        'saved_recommendations': saved_recommendations,
    }

    return render(request, 'tracker.html', context)


def mark_as_completed(request):
    if request.method == 'POST':
        recommendation_id = request.POST.get('recommendation_id')

        # Ensure a recommendation_id is provided
        if not recommendation_id:
            return JsonResponse({'error': 'Recommendation ID is missing.'}, status=400)

        # Get the SavedRecommendation object
        saved_recommendation = get_object_or_404(SavedRecommendation, id=recommendation_id)

        # Check if it's already completed
        if saved_recommendation.completed:
            return JsonResponse({
                'success': True,
                'message': 'This recommendation is already marked as completed.'
            })

        # Mark the recommendation as completed
        saved_recommendation.completed = True
        saved_recommendation.progress = 100  # Update progress to 100%
        saved_recommendation.save()

        # Save the completed recommendation in the CompletedRecommendation table
        completed_recommendation, created = CompletedRecommendation.objects.get_or_create(
            user=saved_recommendation.user,
            recommendation=saved_recommendation.recommendation
        )

        # Respond based on whether the entry was newly created or already existed
        if created:
            message = 'Recommendation marked as completed and saved successfully.'
        else:
            message = 'Recommendation marked as completed, but it was already saved in the completed list.'

        return JsonResponse({'success': True, 'message': message})
    else:
        return JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=405)



class UserProfileForm(forms.ModelForm):
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}), 
        required=False
    )
    class Meta:
        model = UserProfile
        fields = ['bio']


@csrf_exempt
@login_required
def save_recommendation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user
        recommendation_id = data.get('recommendation_id')

        try:
            recommendation = Recommendation.objects.get(id=recommendation_id)
            SavedRecommendation.objects.create(user=user, recommendation=recommendation)
            return JsonResponse({'success': True, 'message': 'Recommendation saved successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


@csrf_exempt  # Allow CSRF-exempt for this view, since you are sending the CSRF token in the header
@require_http_methods(["DELETE"]) # Only allow DELETE requests
def remove_saved_recommendation(request, id):
    try:
        # Get the saved recommendation by its ID
        saved_recommendation = SavedRecommendation.objects.get(id=id)
        saved_recommendation.delete()  # Delete the saved recommendation
        
        return JsonResponse({'message': 'Saved recommendation removed successfully.'})
    except SavedRecommendation.DoesNotExist:
        return JsonResponse({'error': 'Saved recommendation not found.'}, status=404) 
    



def recommend_based_on_search(request):
    # Get user preferences from the search bar (query parameters)
    search_query = request.GET.get('q', '')  # Fetch 'q' parameter from the request
    if not search_query:
        return render(request, 'recommendations.html', {'error': 'Please enter a search query.'})

    # Fetch all recommendation descriptions from the database
    recommendations = Recommendation.objects.all()
    if not recommendations.exists():
        return render(request, 'recommendations.html', {'error': 'No recommendations available.'})

    recommendation_descriptions = [r.description for r in recommendations]

    # Initialize TF-IDF Vectorizer
    vectorizer = TfidfVectorizer()

    # Fit the vectorizer on recommendation descriptions to build the TF-IDF matrix
    tfidf_matrix = vectorizer.fit_transform(recommendation_descriptions)

    # Transform search query into the same vector space
    search_query_vector = vectorizer.transform([search_query])

    # Calculate cosine similarity between search query and recommendation descriptions
    cos_similarities = cosine_similarity(search_query_vector, tfidf_matrix)

    # Get the indices of the top 5 most similar recommendations
    most_similar_indexes = cos_similarities.argsort()[0, -5:][::-1]  # Top 5 recommendations in descending order

    # Fetch the recommended items based on the calculated similarities
    recommended_items = [recommendations[i] for i in most_similar_indexes]

    # Render the recommendations in the template
    return render(request, 'recommendations.html', {'recommendations': recommended_items, 'search_query': search_query})
