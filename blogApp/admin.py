from django.contrib import admin
from .models import Post, Categories, PostComment
from pyuploadcare.dj.forms import FileWidget, ImageField

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'post_date')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    
    formfield_overrides = {
        ImageField: {'widget': FileWidget(attrs={
            'data-cdn-base': 'https://ucarecdn.com/',
            'data-images-only': 'True',
            'data-crop': 'free',
            'data-preview-step': 'True',
            'data-clearable': 'True',
            'data-multiple': 'False',
        })},
    }

admin.site.register(Post, PostAdmin)
admin.site.register(Categories)
admin.site.register(PostComment)

