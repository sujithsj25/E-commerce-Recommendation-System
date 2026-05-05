# Sj_Store Project Documentation
**Date: 5/5/2026**

---

## 1. Django Architecture & Process Flow

Sj_Store is built on the **MVT (Model-View-Template)** architecture.

### Process Flow Summary:
- **Request**: User interacts with the UI (e.g., clicks a category).
- **URLs**: `urls.py` parses the address and routes it to a specific view function.
- **Views**: `views.py` handles the logic, fetches data from the models, and processes it (e.g., running the recommender).
- **Models**: `models.py` defines the database structure for Products, Carts, and AI Interactions.
- **Templates**: `.html` files in the templates folder define the visual layout.
- **HTMX**: Intercepts link clicks to update only the content area, preventing a full page reload.

---

## 2. File & Folder Deep Dive

### /ecommerce (Project Root)
*   **settings.py**: The global configuration file. It registers the `store` app, sets up the database, and configures static/media file paths.
*   **urls.py**: The master URL router that redirects traffic to the app-level URLs.

### /store (Main App)
*   **models.py**: Contains the data definitions. 
    *   `Product`: The core item data.
    *   `UserInteraction`: The "memory" of the AI, storing user likes/clicks.
    *   `Cart/CartItem`: Logic for the shopping basket.
*   **views.py**: The brain of the app. It calculates what products to show, handles "Add to Cart" actions, and renders the final pages.
*   **urls.py**: Maps specific store paths (like `/product/1/`) to view functions.
*   **recommender.py**: The ML engine. It uses `pandas` and `scikit-learn` to analyze user behavior and suggest items.
*   **context_processors.py**: A special utility that makes the "Cart Count" available to the navbar on every single page without repeating code.
*   **templates/**: 
    *   `base.html`: The skeleton of the site (Header, Footer, CSS).
    *   `landing.html`: The entry page with the smooth banner slider.
    *   `home.html`: The main product catalog.
    *   `cart.html`: The glassmorphic shopping bag.
    *   `product_detail.html`: Detailed information for a single product.

---

## 3. AI Recommendation System Logic

The system is a **Pure Collaborative Filtering Engine** (User-Based) using the following ML architecture:

### The Logic Steps:
1.  **Interaction Matrix**: It builds a matrix of `User IDs` vs `Product IDs` using the `UserInteraction` records.
2.  **Cosine Similarity (Scikit-Learn)**: 
    *   It calculates the similarity between the current user and all other users.
    *   Only users with a similarity score > 0 are considered "Neighbors".
3.  **Weighted-Average ML Prediction**: 
    *   The AI predicts a rating for every product you haven't interacted with yet.
    *   Formula: `Predicted Score = Sum(Similarity Score × Neighbor Rating) / Sum(Similarity Scores)`.
4.  **Ranking**: It sorts these predictions and returns the top products. 
    *   *Note: If no user interactions exist or no similar users are found, the system returns zero recommendations to maintain ML integrity.*

---

## 4. Premium Design Standards
*   **Glassmorphism**: Frosted glass effects for a high-end feel.
*   **HTMX SPA**: Seamless navigation without page refreshes.
*   **Responsive Grid**: A layout that adjusts perfectly from desktop to mobile.