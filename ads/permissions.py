from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Разрешает доступ, если пользователь является владельцем объекта или админом (is_staff=True).
    """

    def has_object_permission(self, request, view, obj):
        # Чтение разрешено всем (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Редактирование/удаление только владельцу или админу
        return obj.author == request.user or request.user.is_staff