from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Resource
import numpy as np

def get_recommendations(query, top_n=5):
    """
    Get personalized resource recommendations based on user goals using TF-IDF similarity.
    Returns a list of resource dictionaries with title, url, topic, and goal info.
    """
    if not query.strip():
        return []

    # Get all resources
    resources = list(Resource.objects.all())
    if not resources:
        return []

    # Prepare resource texts for vectorization
    resource_texts = []
    for resource in resources:
        text_parts = [
            resource.title,
            resource.topic,
            resource.goal.title if resource.goal else "",
            resource.goal.description if resource.goal else "",
            resource.goal.tags if resource.goal else ""
        ]
        resource_texts.append(" ".join(text_parts).lower())

    # Add the query to the corpus for comparison
    all_texts = resource_texts + [query.lower()]

    try:
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform(all_texts)

        # Calculate similarity between query and all resources
        query_vector = tfidf_matrix[-1]  # Last vector is the query
        resource_vectors = tfidf_matrix[:-1]  # All others are resources

        similarities = cosine_similarity(query_vector, resource_vectors).flatten()

        # Get top similar resources
        top_indices = np.argsort(similarities)[::-1][:top_n]
        top_similarities = similarities[top_indices]

        recommendations = []
        for idx, similarity in zip(top_indices, top_similarities):
            if similarity > 0.1:  # Only include if similarity is above threshold
                resource = resources[idx]
                recommendations.append({
                    'title': resource.title,
                    'url': resource.url,
                    'topic': resource.topic,
                    'goal': resource.goal.title if resource.goal else None,
                    'similarity': round(float(similarity), 3)
                })

        return recommendations

    except Exception as e:
        # Fallback to simple keyword matching if ML fails
        print(f"ML recommendation failed: {e}, falling back to keyword matching")
        return get_fallback_recommendations(query, resources, top_n)

def get_fallback_recommendations(query, resources, top_n=5):
    """
    Fallback recommendation system using simple keyword matching.
    """
    query_lower = query.lower()
    scored_resources = []

    for resource in resources:
        score = 0
        resource_text = f"{resource.title} {resource.topic} {resource.goal.title if resource.goal else ''} {resource.goal.description if resource.goal else ''} {resource.goal.tags if resource.goal else ''}".lower()

        # Simple scoring based on keyword matches
        query_words = set(query_lower.split())
        resource_words = set(resource_text.split())

        # Exact matches get higher score
        exact_matches = len(query_words.intersection(resource_words))
        score += exact_matches * 2

        # Partial matches get lower score
        for q_word in query_words:
            for r_word in resource_words:
                if q_word in r_word or r_word in q_word:
                    score += 0.5

        if score > 0:
            scored_resources.append((score, resource))

    # Sort by score and return top recommendations
    scored_resources.sort(key=lambda x: x[0], reverse=True)
    recommendations = []

    for score, resource in scored_resources[:top_n]:
        recommendations.append({
            'title': resource.title,
            'url': resource.url,
            'topic': resource.topic,
            'goal': resource.goal.title if resource.goal else None,
            'similarity': round(score, 2)
        })

    return recommendations
