from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    librarian = "librarian"
    student = "student"
