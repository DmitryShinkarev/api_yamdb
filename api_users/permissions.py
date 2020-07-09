from rest_framework.permissions import IsAdminUser, IsAuthenticated


class IsOwnProfileOrAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and (view.kwargs.get('username') == 'me'
                                                          or IsAdminUser().has_permission(request, view)
                                                          or request.user.role == 'admin')
