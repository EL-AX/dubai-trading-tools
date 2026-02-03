import sys
from pathlib import Path
import json

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import src.auth as auth


def test_migrate_users_normalize_emails(tmp_path):
    # Use a temporary users file so we don't touch real data
    temp_users_file = tmp_path / "users.json"
    auth.USERS_FILE = str(temp_users_file)

    # Create users with mixed-case and spaces
    users = {
        " Alice@Example.COM ": {
            "name": "Alice",
            "password": auth.hash_password("password123"),
            "verified": False
        },
        "bob@Example.com": {
            "name": "Bob",
            "password": auth.hash_password("hunter2"),
            "verified": True
        }
    }
    auth.save_users(users)

    res = auth.migrate_users_normalize_emails(backup=True)
    assert res["success"] is True
    assert res["migrated"] == 2

    new_users = auth.load_users()
    assert "alice@example.com" in new_users
    assert "bob@example.com" in new_users


def test_register_and_login_normalization(tmp_path):
    temp_users_file = tmp_path / "users.json"
    auth.USERS_FILE = str(temp_users_file)

    # Register with spaced/capitalized email
    r = auth.register_user(" TestUser@Example.COM ", "safepass", "Tester")
    assert r["success"] is True

    # Attempt login with normalized email - pass verification code (registration creates one)
    u = auth.load_users().get("testuser@example.com")
    code = u.get("verification_code")
    assert code is not None
    login_res = auth.login_user("testuser@example.com", "safepass", verification_code=code)
    assert login_res["success"] is True
    assert login_res["name"] == "Tester"
