from django.db import migrations

def populate_descriptions(apps, schema_editor):
    Product = apps.get_model('store', 'Product')
    
    # Description Map for common products
    description_map = {
        'iPhone': "The ultimate smartphone experience with a stunning Super Retina XDR display and advanced pro camera system for breathtaking photos and videos.",
        'MacBook': "A powerhouse of creativity and performance, featuring the revolutionary M-series chip and an ultra-thin design that redefines what's possible.",
        'Sony': "Industry-leading noise cancellation and immersive sound quality, designed for those who demand the absolute best in audio performance.",
        'Samsung': "Cutting-edge technology meets elegant design, featuring a vibrant AMOLED display and a versatile camera system for every moment.",
        'Watch': "Your essential companion for a healthy life, tracking your workouts, monitoring your health, and keeping you connected to what matters.",
        'iPad': "Versatile, powerful, and remarkably thin. Whether you're working, creating, or playing, it's the perfect canvas for your ideas.",
        'Dell': "Premium engineering and sleek aesthetics combined to deliver a high-performance computing experience for professionals and creators.",
        'Logitech': "Precision-engineered peripherals that enhance your productivity and gaming experience with ergonomic design and tactile feedback.",
        'Headphones': "Crystal-clear audio and all-day comfort, perfect for music lovers and professionals who need to stay focused on the go.",
        'Laptop': "Uncompromising performance and portability, designed to handle your most demanding tasks with ease and style.",
        'Smartphone': "Stay connected with the latest features and a sleek design that fits perfectly in your hand and your lifestyle.",
    }

    generic_descriptions = {
        'Mobiles': "A premium mobile experience featuring the latest in communication technology and a sleek, modern design.",
        'Laptops': "Engineered for excellence, this laptop delivers the perfect balance of power, portability, and premium design.",
        'Accessories': "Enhance your digital lifestyle with this high-quality accessory, crafted for durability and seamless integration.",
        'Electronics': "Experience the future of technology with this state-of-the-art electronic masterpiece, designed for peak performance.",
        'Fashion': "Timeless style meets modern elegance. Crafted from premium materials for a look that's as unique as you are.",
        'Home & Appliances': "Elevate your living space with intelligent design and superior functionality, built to make every day easier.",
    }

    for product in Product.objects.all():
        # Only update if description is empty or very short (likely a placeholder)
        if not product.description or len(product.description) < 10:
            found = False
            # Check name for keywords
            for key, desc in description_map.items():
                if key.lower() in product.name.lower():
                    product.description = desc
                    found = True
                    break
            
            # If no keyword match, use category
            if not found:
                product.description = generic_descriptions.get(product.category, "Experience the pinnacle of engineering and design with this premium selection. Crafted for those who demand excellence.")
            
            product.save()

def reverse_populate(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('store', '0005_product_image'), # Based on my earlier check of migrations
    ]

    operations = [
        migrations.RunPython(populate_descriptions, reverse_populate),
    ]
