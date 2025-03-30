from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from graphene_django.views import GraphQLView
from blog.schema import schema
from users import views as user_views

urlpatterns = [
    # Admin and Jet URLs
    path('jet/', include('jet.urls')),
    path('admin/', admin.site.urls),
    
    # CKEditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    # GraphQL
    path('graphql/', GraphQLView.as_view(graphiql=True)),
    
    # User management
    path('register/', user_views.register, name='register'),
    path('login/', user_views.login, name='login'),
    path('logout/', user_views.logout, name='logout'),
    
    # App URLs
    path('', include('users.urls')),  # Add this for your user pages
    path('blog/', include('blogApp.urls')),  # Changed to prefix blog URLs with 'blog/'
]

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
