from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class IsStaffForMutationOrOwnerRead(BasePermission):
    """
    Borrow:
      - читать: владелец записи или staff
      - создавать/изменять/закрывать: только staff
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return obj.user_id == getattr(request.user, "id", None) or (
                request.user and request.user.is_staff
            )
        return bool(request.user and request.user.is_staff)
