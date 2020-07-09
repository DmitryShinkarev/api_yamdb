from rest_framework.permissions import IsAdminUser, IsAuthenticated, SAFE_METHODS


class IsAdminOrReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or super().has_permission(request, view) and (
                                                          IsAdminUser().has_permission(request, view)
                                                          or request.user.role == 'admin')


class IsModeraorOrAdminOrReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or super().has_permission(request, view) and (
                                                          IsAdminUser().has_permission(request, view)
                                                          or request.user.role == 'admin'
                                                          or request.user.role == 'moderator')
