import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from .models import UserInteraction

def get_recommendations(user_id):
    from .models import Product
    all_product_ids = list(Product.objects.values_list('id', flat=True)[:4])
    
    data = list(UserInteraction.objects.all().values())
    if not data:
        return all_product_ids

    df = pd.DataFrame(data)
    matrix = df.pivot_table(index='user_id', columns='product_id', values='rating').fillna(0)

    if user_id not in matrix.index:
        popular = df['product_id'].value_counts().head(4).index.tolist()
        return popular if popular else all_product_ids

    # If only 1 user exists in the DB, CF similarity won't produce other users
    if len(matrix.index) <= 1:
        popular = df['product_id'].value_counts().head(4).index.tolist()
        # Remove what user already liked
        user_interacted = set(df[df['user_id'] == user_id]['product_id'])
        fallback = [p for p in popular if p not in user_interacted]
        return fallback if fallback else all_product_ids

    similarity = cosine_similarity(matrix)
    sim_df = pd.DataFrame(similarity, index=matrix.index, columns=matrix.index)

    similar_users = sim_df[user_id].sort_values(ascending=False)[1:3]
    recommended = set()

    for user in similar_users.index:
        products = df[df['user_id'] == user]['product_id']
        recommended.update(products)

    user_interacted = set(df[df['user_id'] == user_id]['product_id'])
    recommended = recommended - user_interacted

    res = list(recommended)
    if not res:
        popular = df['product_id'].value_counts().head(4).index.tolist()
        res = [p for p in popular if p not in user_interacted]
        
    return res if res else all_product_ids