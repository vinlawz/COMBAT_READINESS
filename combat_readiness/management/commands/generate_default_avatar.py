import os
from django.core.management.base import BaseCommand
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont

class Command(BaseCommand):
    help = 'Generate a default avatar image'

    def handle(self, *args, **options):
        # Create static/img directory if it doesn't exist
        img_dir = os.path.join(settings.BASE_DIR, 'static', 'img')
        os.makedirs(img_dir, exist_ok=True)
        
        # Define image properties
        size = (300, 300)
        bg_color = (40, 44, 52)  # Dark background
        text_color = (255, 193, 7)  # Yellow color to match the theme
        
        # Create a new image with the specified background color
        image = Image.new('RGB', size, bg_color)
        draw = ImageDraw.Draw(image)
        
        # Add text to the image
        try:
            # Try to load a font
            font_size = 100
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except IOError:
                # Fall back to default font if Arial is not available
                font = ImageFont.load_default()
            
            # Draw the text in the center of the image
            text = "USER"
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)
            draw.text(position, text, font=font, fill=text_color)
            
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error creating avatar: {e}'))
            return
        
        # Save the image
        output_path = os.path.join(img_dir, 'default-avatar.png')
        image.save(output_path)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created default avatar at {output_path}'))
