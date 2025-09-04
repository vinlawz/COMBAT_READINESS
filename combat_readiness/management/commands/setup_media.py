import os
import shutil
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Set up media directories and copy default avatar'

    def handle(self, *args, **options):
        # Create media directory if it doesn't exist
        media_root = Path(settings.MEDIA_ROOT)
        profile_images_dir = media_root / 'profile_images'
        
        try:
            # Create profile_images directory
            profile_images_dir.mkdir(parents=True, exist_ok=True)
            self.stdout.write(self.style.SUCCESS(f'Created directory: {profile_images_dir}'))
            
            # Copy default avatar if it doesn't exist
            default_avatar_src = Path(settings.BASE_DIR) / 'combat_readiness' / 'static' / 'img' / 'default-avatar.png'
            default_avatar_dest = profile_images_dir / 'default-avatar.png'
            
            if not default_avatar_dest.exists() and default_avatar_src.exists():
                shutil.copy2(default_avatar_src, default_avatar_dest)
                self.stdout.write(self.style.SUCCESS(f'Copied default avatar to {default_avatar_dest}'))
            
            # Set permissions (read/write for owner, read for others)
            os.chmod(profile_images_dir, 0o755)
            if default_avatar_dest.exists():
                os.chmod(default_avatar_dest, 0o644)
                
            self.stdout.write(self.style.SUCCESS('Media directory setup completed successfully!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error setting up media directory: {str(e)}'))
