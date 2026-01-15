from rest_framework.permissions import BasePermission


class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == "patient"
        )


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == "doctor"
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == "admin"
        )



















































# from rest_framework.permissions import BasePermission


# class IsPatient(BasePermission):
#     def has_permission(self, request, view):
#         # Support both naming conventions: `patient_profile` (current) and
#         # `patientprofile` (legacy) to be backwards compatible with tests.
#         return (
#             request.user.is_authenticated and
#             (
#                 hasattr(request.user, "patient_profile") or
#                 hasattr(request.user, "patientprofile")
#             )
#         )


# class IsDoctor(BasePermission):
#     def has_permission(self, request, view):
#         # Support both naming conventions: `doctor_profile` (current) and
#         # `doctorprofile` (legacy) to be backwards compatible with tests.
#         return (
#             request.user.is_authenticated and
#             (
#                 hasattr(request.user, "doctor_profile") or
#                 hasattr(request.user, "doctorprofile")
#             )
#         )


# class IsAdmin(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.is_staff


# class IsAdminUserForReports(BasePermission):
#     message = "You do not have permission to access system reports."

#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.is_staff










