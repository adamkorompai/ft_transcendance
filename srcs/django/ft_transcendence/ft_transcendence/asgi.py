"""
ASGI config for ft_transcendence project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chatapp.routing import websocket_urlpatterns as chat_websocket_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ft_transcendence.settings')
django.setup()

# Django ASGI application
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat_websocket_urlpatterns
        )
    ),
})

# Static files URL configuration for development
if settings.DEBUG:
    application = ProtocolTypeRouter({
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                chat_websocket_urlpatterns
            )
        ),
    })

    # Serve static files during development
    from django.urls import re_path
    from django.views.static import serve as static_serve
    static_url = re_path(r'^static/(?P<path>.*)$', static_serve)

    urlpatterns = [static_url]

# Static files URL configuration for production
else:
    application = ProtocolTypeRouter({
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                chat_websocket_urlpatterns
            )
        ),
        })
   
