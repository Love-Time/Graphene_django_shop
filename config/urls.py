from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.decorators.csrf import csrf_exempt

from graphene_file_upload.django import FileUploadGraphQLView

from config import settings
from .schema import schema


urlpatterns = [
    path('admin/', admin.site.urls),
    path("graphql", csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True, schema=schema)))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns.append(path("", include(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))))

