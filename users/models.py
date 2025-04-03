from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.conf import settings
from taggit.managers import TaggableManager
from html import unescape
from django.utils.html import strip_tags
from shortuuid.django_fields import ShortUUIDField
from pyuploadcare.dj.models import ImageField
from ckeditor.fields import RichTextField


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(default='Edit your Bio!')
    website = models.CharField(max_length=40)

    def __str__(self):
        return self.user.get_username()
    
class Editpage(models.Model):
    SECTION_CHOICES = [
        ('hnew', 'Home | heading 1'),
        ('hneww', 'Home | Heading 2'),
        ('hnewww', 'Home | Heading 3'),
        ('Programme1', 'Home | Programme1'),
        ('Programme2', 'Home | Programme2'),
        ('Programme3', 'Home | Programme3'),

        ('about_us', 'Home | About Us'),
        ('mission', 'Home | Our Mission'),
        ('vision', 'Home | Our Vision'),
        ('Volunteer', 'Home | Volunteer'),
        ('footer', 'Home | Footer'),
        ('aboutUs', 'About Us | About Us'),
        ('our_Programs', 'Programs | Goddess Care Initiative'),
        ('reach', 'Programs | Our Reach '),
        ('team1', 'Our Team | Kelly'),
        ('team2', 'Our Team | Elsie'),
        ('team3', 'Our Team | Loise'),

    ]

    section_name = models.CharField(max_length=100, choices=SECTION_CHOICES, unique=True, blank=True)
    heading = RichTextField(blank=True) 
    content = RichTextField(blank=True)  
    slider_image = ImageField(blank=True, manual_crop="") 
    

    def __str__(self):
        return self.get_section_name_display()
    

class MainProgrames(models.Model):
    SECTION_CHOICES = [
        ('Programme1', 'Programe | Programme1'),
        ('Programme2', 'Programe | Programme2'),
        ('Programme3', 'Programe | Programme3'),
        ('Programme4', 'Programe | Programme4'),

    ]

    programe_name = models.CharField(max_length=100, choices=SECTION_CHOICES, unique=True)
    programe_description = RichTextField()
    programe_objective1 = RichTextField() 
    programe_objective2 = RichTextField()
    programe_objective3 = RichTextField()
    programe_objective4 = RichTextField()
    

    def __str__(self):
        return self.get_section_name_display()
    
    from ckeditor.fields import RichTextField  # Make sure this import is at the top

class SecondSection(models.Model):
    subtitle = RichTextField()  # Changed to RichTextField
    title = RichTextField()     # Changed to RichTextField
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return strip_tags(self.subtitle)  # Using strip_tags for clean string representation

    class Meta:
        verbose_name = "Second Section"
        verbose_name_plural = "Second Sections"

class SecondSectionIcon(models.Model):
    ICON_CHOICES = [
        ('icon-vegetable', 'Food Icon'),
        ('icon-water-1', 'Water Icon'),
        ('icon-stethoscope', 'Medical Icon'),
        # Add more icon choices as needed
    ]

    icon_class = models.CharField(max_length=50, choices=ICON_CHOICES)
    text = RichTextField()      # Changed to RichTextField
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{strip_tags(self.text)} - {self.icon_class}"

    class Meta:
        ordering = ['order']
        verbose_name = "Second Section Icon"
        verbose_name_plural = "Second Section Icons"

class SecondSectionBox(models.Model):
    text = RichTextField()      # Changed to RichTextField
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return strip_tags(self.text)

    class Meta:
        verbose_name = "Second Section Box"
        verbose_name_plural = "Second Section Boxes"
