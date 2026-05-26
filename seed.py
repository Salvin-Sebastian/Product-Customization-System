import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from customizer.models import Product, ProductView
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw
import io

def seed_database():
    # 1. Create Superuser
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'adminpass123')
        print("Superuser 'admin' created successfully with password 'adminpass123'")
    else:
        print("Superuser 'admin' already exists")

    # 2. Check if a product already exists
    if Product.objects.count() == 0:
        product = Product.objects.create(
            name="Classic Grey T-Shirt",
            description="A premium heavyweight cotton grey t-shirt, perfect for custom designs."
        )

        # Generate a mock T-shirt image using PIL
        img = Image.new('RGB', (800, 800), color='#f1f5f9') # Very light slate canvas
        draw = ImageDraw.Draw(img)

        # Draw a premium mockup of a T-Shirt to show off visual mapping
        # Body
        draw.polygon([(220, 120), (580, 120), (580, 720), (220, 720)], fill='#cbd5e1')
        # Left sleeve
        draw.polygon([(220, 120), (100, 240), (170, 310), (220, 240)], fill='#cbd5e1')
        # Right sleeve
        draw.polygon([(580, 120), (700, 240), (630, 310), (580, 240)], fill='#cbd5e1')
        # Neck collar line
        draw.ellipse((340, 90, 460, 150), fill='#f1f5f9', outline='#94a3b8', width=3)
        # Inner collar shade
        draw.chord((340, 90, 460, 150), start=0, end=180, fill='#94a3b8')

        # Delineate print area guide with a subtle dashed outline
        # (This helps the admin/user see where the print area mapping boundary is!)
        draw.rectangle([250, 180, 550, 600], outline='#3b82f6', width=2)

        # Save to buffer
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        image_content = ContentFile(buf.getvalue(), name='sample_shirt.jpg')

        # Create ProductView
        ProductView.objects.create(
            product=product,
            view_name="Front View (Mockup)",
            base_image=image_content,
            print_area_x=250,
            print_area_y=180,
            print_area_width=300,
            print_area_height=420
        )
        print("Default product and product view seeded successfully!")
    else:
        print("Database already contains product data, skipping seed.")

if __name__ == "__main__":
    seed_database()
