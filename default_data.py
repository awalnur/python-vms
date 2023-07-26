from app.core.security import hash_password

DEFAULT_ROLES = [
    {'name': 'Admin'},
    {'name': 'User'},
    {'name': 'Guest'},
]


DEFAULT_USERS = [
    {
        'username': 'john_doe',
        'email': 'john@example.com',
        'password_hash': hash_password('hashed_password'),
        'is_active': True
    },
    {
        'username': 'jane_smith',
        'email': 'jane_smith@example.com',
        'password_hash': hash_password('hashed_password'),
        'is_active': True
    },
    {
        'username': 'admin',
        'email': 'admin@example.com',
        'password_hash': hash_password('hashed_password'),
        'is_active': True
    }
]

DEFAULT_USER_ROLES = [
    {
        'user_id': 1,
        'role_id': 1
    },
    {
        'user_id': 2,
        'role_id': 2
    },
    {
        'user_id': 3,
        'role_id': 3
    }

]

