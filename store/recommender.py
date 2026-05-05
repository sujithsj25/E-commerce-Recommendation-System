import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from .models import UserInteraction

def get_recommendations(user_id):
    """
    Main Recommendation Engine using Pure User-Based Collaborative Filtering (ML).
    This function predicts product preferences by finding users with similar tastes.
    """
    from .models import Product
    
    # 1. Fetch all interaction data from the database
    data = list(UserInteraction.objects.all().values())
    if not data:
        # If no interaction data exists at all, we cannot run ML
        return []

    # 2. Pre-process data into a Pandas DataFrame
    df = pd.DataFrame(data)
    
    # 3. Create a User-Item Matrix (Pivot Table)
    # Rows = User IDs, Columns = Product IDs, Values = Rating (1-5)
    matrix = df.pivot_table(index='user_id', columns='product_id', values='rating').fillna(0)

    # 4. Cold Start Check: If current user has no history, they are not in the matrix
    if user_id not in matrix.index:
        return []

    # 5. Handle Single User Case: Collaborative Filtering requires at least 2 users to compare
    if len(matrix.index) <= 1:
        return []

    # 6. ML Core: Calculate Cosine Similarity Matrix between all users
    # This measures the 'angle' between user taste vectors in multi-dimensional space
    similarity = cosine_similarity(matrix)
    sim_df = pd.DataFrame(similarity, index=matrix.index, columns=matrix.index)

    # 7. Identify Neighbors: Find other users with a similarity score > 0
    # We drop the current user [index != user_id] so we don't compare a user with themselves
    neighbors = sim_df[user_id].drop(index=user_id)
    neighbors = neighbors[neighbors > 0].sort_values(ascending=False)

    if neighbors.empty:
        # If no users have shared interests, we cannot recommend anything via CF
        return []

    # 8. Filter: Identify products the user has already interacted with (to avoid repeats)
    user_interacted = set(df[df['user_id'] == user_id]['product_id'])
    cf_scores = {}

    # 9. Weighted Prediction Algorithm:
    # We predict a score for every product the user HASN'T seen yet.
    # Score = Sum(User_Similarity * Neighbor_Rating) / Sum(User_Similarity)
    unseen_products = [p for p in matrix.columns if p not in user_interacted]
    
    for p_id in unseen_products:
        weighted_sum = 0
        similarity_sum = 0
        
        for neighbor_id, score in neighbors.items():
            rating = matrix.loc[neighbor_id, p_id]
            if rating > 0:
                # Multiply neighbor's similarity by their rating for this specific product
                weighted_sum += score * rating
                similarity_sum += score
        
        if similarity_sum > 0:
            # The final predicted score is the weighted average
            cf_scores[p_id] = weighted_sum / similarity_sum

    # 10. Ranking & Selection:
    # Sort the products based on the highest predicted ML score and return the top results
    recommended_ids = [p[0] for p in sorted(cf_scores.items(), key=lambda x: x[1], reverse=True)]
    
    return recommended_ids[:8]