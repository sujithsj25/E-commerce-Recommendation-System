# Sj_Store Premium E-Commerce

A high-end, luxury e-commerce platform built with **Django**, featuring a modern "Glassmorphism" UI and an **AI-driven Recommendation Engine**.

## 🌟 Key Features

- **AI-Powered Recommendations**: 
    - Pure ML-based **Collaborative Filtering** engine (`recommender.py`).
    - Personalized product suggestions based on user interaction data and community behavior.
    - Dynamic recommendation rows integrated into the Homepage and Product Detail views.
- **Premium UI/UX**: 
    - Apple-inspired **Glassmorphism** navbar with real-time blur.
    - Sleek animations and a glowing hero section on the landing page.
    - Interactive product cards with "Like" and "Add to Cart" instant feedback.
- **Advanced Search**: Fully functional search bar that filters the product catalog by name and category in real-time.
- **Smart Cart**: Guarded removal logic (decrementing quantity one-by-one) with safety confirmation prompts.
- **Corporate Infrastructure**: Dedicated informational pages for About Us, Careers, Support, and Legal.

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Pip (Python Package Manager)

### Installation
1. Clone the repository locally:
   ```bash
   git clone https://github.com/your-username/Sj-Store-Ecommerce.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations and set up the database:
   ```bash
   python manage.py migrate
   ```
4. Start the development server:
   ```bash
   python manage.py runserver
   ```

## 🛠️ Project Architecture

- **`store/recommender.py`**: ML core for Collaborative Filtering using Scikit-Learn and Pandas.
- **`store/templates/`**: Premium HTML5/CSS3 templates using a unified design system.
- **`store/views.py`**: Custom backend logic for search, categorization, and cart handling.
- **`store/models.py`**: SQLite database models for Products, User Interactions, and Carts.

---
*Developed as a premium e-commerce solution for Sj_Store*

