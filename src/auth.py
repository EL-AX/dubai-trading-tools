import json
import hashlib
import os
import random
import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime, timedelta

USERS_FILE = "data/users.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)

def generate_verification_code():
    return str(random.randint(100000, 999999))

def register_user(email, password, name):
    """Register a new user and send verification email immediately"""
    users = load_users()
    if email in users:
        return {"success": False, "message": "Email already registered"}
    
    # Generate verification code
    code = generate_verification_code()
    
    # Create user
    users[email] = {
        "name": name,
        "password": hash_password(password),
        "verified": False,
        "verification_code": code,
        "verification_sent_at": datetime.now().isoformat(),
        "created_at": datetime.now().isoformat(),
        "settings": {
            "theme": "system",  # Let system handle theme
            "alerts_enabled": True,
            "currency": "USD"
        }
    }
    save_users(users)
    
    # Send verification email
    sent, info = send_verification_email(email, code, name)
    
    if sent:
        return {
            "success": True,
            "message": f"Registration successful! Verification code sent to {email}",
            "code_sent": True
        }
    else:
        # Still register but warn about email failure
        return {
            "success": True,
            "message": f"Registration successful but email delivery failed: {info}. Contact support.",
            "code_sent": False,
            "info": info
        }

def login_user(email, password, verification_code=None):
    """Login user - must verify email first with code"""
    users = load_users()
    if email not in users:
        return {"success": False, "message": "Email not found"}
    
    user = users[email]
    
    # If not verified, require verification code
    if not user.get("verified"):
        if not verification_code:
            return {"success": False, "message": "Email not verified. Please enter verification code first."}
        
        # Verify the code
        if user.get("verification_code") != verification_code:
            return {"success": False, "message": "Invalid verification code"}
        
        # Check expiry (1 hour)
        sent_at = user.get("verification_sent_at")
        if sent_at:
            try:
                sent_dt = datetime.fromisoformat(sent_at)
                if datetime.now() > sent_dt + timedelta(hours=1):
                    return {"success": False, "message": "Verification code expired. Request a new one."}
            except:
                pass
        
        # Mark as verified
        user["verified"] = True
        user.pop("verification_code", None)
        user.pop("verification_sent_at", None)
        save_users(users)
    
    # Now check password
    if user["password"] != hash_password(password):
        return {"success": False, "message": "Wrong password"}
    
    return {"success": True, "message": "Login successful", "name": user["name"]}

def verify_user_email(email, code):
    users = load_users()
    if email not in users:
        return {"success": False, "message": "User not found"}

    user = users[email]
    # Check expiry (1 hour)
    sent_at = user.get("verification_sent_at")
    if sent_at:
        try:
            sent_dt = datetime.fromisoformat(sent_at)
            if datetime.now() > sent_dt + timedelta(hours=1):
                return {"success": False, "message": "Verification code expired. Request a new one."}
        except Exception:
            pass

    if user.get("verification_code") != code:
        return {"success": False, "message": "Wrong verification code"}

    user["verified"] = True
    # Remove verification code for security
    user.pop("verification_code", None)
    user.pop("verification_sent_at", None)
    save_users(users)
    return {"success": True, "message": "Email verified"}

def send_verification_email(recipient_email, code, name):
    """Send a verification email using SMTP. SMTP settings must be provided via environment variables:
    SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, EMAIL_FROM
    Returns (sent: bool, info: str)
    """
    host = os.getenv("SMTP_HOST")
    port = os.getenv("SMTP_PORT")
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASSWORD")
    email_from = os.getenv("EMAIL_FROM", user)

    if not host or not port or not user or not password:
        return False, "SMTP not configured (SMTP_HOST/SMTP_PORT/SMTP_USER/SMTP_PASSWORD)"

    try:
        port = int(port)
    except Exception:
        return False, "SMTP_PORT must be an integer"

    msg = EmailMessage()
    msg["Subject"] = "Votre code de vérification - Dubai Trading Tools"
    msg["From"] = email_from
    msg["To"] = recipient_email
    text = f"Bonjour {name},\n\nVotre code de vérification pour Dubai Trading Tools est: {code}\nIl expire dans 1 heure.\n\nSi vous n'avez pas demandé ce code, ignorez cet email.\n\nCordialement,\nL'équipe Dubai Trading Tools"
    html = f"<p>Bonjour {name},</p><p>Votre code de vérification pour <b>Dubai Trading Tools</b> est: <strong>{code}</strong></p><p>Il expire dans 1 heure.</p><p>Si vous n'avez pas demandé ce code, ignorez cet email.</p><p>Cordialement,<br/>L'équipe Dubai Trading Tools</p>"
    msg.set_content(text)
    msg.add_alternative(html, subtype='html')

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(user, password)
            server.send_message(msg)
        return True, "Email sent"
    except Exception as e:
        return False, str(e)

def resend_verification_code(email):
    users = load_users()
    if email not in users:
        return {"success": False, "message": "User not found"}
    user = users[email]
    if user.get("verified"):
        return {"success": False, "message": "User already verified"}

    code = generate_verification_code()
    user["verification_code"] = code
    user["verification_sent_at"] = datetime.now().isoformat()
    save_users(users)
    sent, info = send_verification_email(email, code, user.get("name", "Utilisateur"))
    if sent:
        return {"success": True, "message": "Verification email resent"}
    else:
        return {"success": False, "message": f"Failed to send email: {info}"}

def get_user_settings(email):
    users = load_users()
    if email in users:
        return users[email].get("settings", {})
    return {"theme": "light", "alerts_enabled": True, "currency": "USD"}

def save_user_settings(email, settings):
    users = load_users()
    if email in users:
        users[email]["settings"] = settings
        save_users(users)

def init_session_state(st):
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_email" not in st.session_state:
        st.session_state.user_email = None
    if "user_name" not in st.session_state:
        st.session_state.user_name = None
    if "theme" not in st.session_state:
        st.session_state.theme = "light"

def logout(st):
    st.session_state.authenticated = False
    st.session_state.user_email = None
    st.session_state.user_name = None
