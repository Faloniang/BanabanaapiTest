from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """
    Gerer les permissions selon la propriété de l'objet.
    """

    def has_object_permission(self, request, view, obj):
        # La lecture est permis à tout le monde,
        if request.method in permissions.SAFE_METHODS:
            return True

        # La modification est permi juste au créateur de l'objet.
        return obj.created_by == request.user