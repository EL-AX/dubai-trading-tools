"""© 2025-2026 ELOADXFAMILY - Tous droits réservés
Debug Auth Script - Authentication troubleshooting"""
from pathlib import Path
import src.auth as auth
from tempfile import TemporaryDirectory

tmp_dir = TemporaryDirectory()
auth.USERS_FILE = str(Path(tmp_dir.name)/"users.json")
print('USERS_FILE:', auth.USERS_FILE)
res = auth.register_user(' TestUser@Example.COM ', 'safepass', 'Tester')
print('register res:', res)
users = auth.load_users()
print('users keys:', list(users.keys()))
login_res = auth.login_user('testuser@example.com', 'safepass')
print('login_res:', login_res)
