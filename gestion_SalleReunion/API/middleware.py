from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.middleware import get_user
from django.shortcuts import redirect

class LDAPAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Vérifier si l'utilisateur est authentifié via LDAP
        user = get_user(request)
        if user.is_authenticated and hasattr(user, 'ldap_user'):
            # L'utilisateur est authentifié via LDAP, autoriser l'accès
            return self.get_response(request)
        
        # Vérifier si l'utilisateur tente d'accéder à la page /admin/
        # if request.path.startswith('/admin/'):
        #     # Rediriger l'utilisateur vers la page de connexion
        #     return redirect('authentification')
        
        # Laisser passer les autres requêtes
        return self.get_response(request)