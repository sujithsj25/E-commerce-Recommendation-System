# Sj_Store Premium E-Commerce

A high-end, luxury e-commerce platform built with **Django**, featuring a modern "Glassmorphism" UI and a robust dynamic backend.

## 🌟 Key Features

- **Premium UI/UX**: 
    - Apple-inspired **Glassmorphism** navbar with real-time blur.
    - Sleek animations and a glowing hero section on the landing page.
    - Interactive product cards with "Like" and "Add to Cart" instant feedback.
- **Advanced Search**: Fully functional search bar that filters the 34-product catalog by name and category in real-time.
- **Dynamic-Manual Hybrid Catalog**: Combines hand-crafted category sections for maximum aesthetic control with a live database sync for images, prices, and inventory.
- **Toast Notifications**: JavaScript-driven real-time feedback system for user actions.
- **Corporate Infrastructure**: Dedicated informational pages for About Us, Careers, Support, and Legal.
- **Smart Cart**: Guarded removal logic (decrementing quantity one-by-one) with safety confirmation prompts.
- **Admin Integration**: Personalized brand identity with a unique 3D monogram logo and hidden admin portals for cleaner public UI.

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Django 6.0+
- Pillow (for image handling)

### Installation
1. Clone the repository locally.
2. Install dependencies:
   ```bash
   pip install django pillow
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Start the development server:
   ```bash
   python manage.py runserver
   ```

## 🛠️ Project Architecture

- **`store/templates/`**: Premium HTML5/CSS3 templates using a unified design system.
- **`store/views.py`**: Custom backend logic for search, categorization, and cart handling.
- **`store/models.py`**: SQLite database models for Products, User Interactions, and Carts.
- **`media/`**: Dynamically uploaded product images.
- **`static/images/`**: Fixed brand assets (Logo).

## 📄 Documentation & Workflows
Detailed planning and walkthroughs can be found in the `.brain` directory artifacts.

---
*Created by Antigravity AI for Sj_Store*
