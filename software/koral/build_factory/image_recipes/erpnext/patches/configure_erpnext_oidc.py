import frappe
import traceback
import json
import os
import sys

def configure_authentik():
    # Initialize Frappe
    frappe.init(site="erpnext.homelab.local", sites_path="sites")
    frappe.connect()

    # Configuration from Environment
    PROVIDER_NAME = "authentik" # Must be unique and match URL path
    LABEL_NAME = "Authentik"    # Display Name
    
    CLIENT_ID = os.environ.get("ERPNEXT_CLIENT_ID")
    CLIENT_SECRET = os.environ.get("ERPNEXT_CLIENT_SECRET")
    AUTHENTIK_URL = os.environ.get("AUTHENTIK_URL")
    ERPNEXT_URL = os.environ.get("ERPNEXT_URL")

    if not all([CLIENT_ID, CLIENT_SECRET, AUTHENTIK_URL, ERPNEXT_URL]):
        print("Error: Missing required environment variables (ERPNEXT_CLIENT_ID, ERPNEXT_CLIENT_SECRET, AUTHENTIK_URL, ERPNEXT_URL)")
        sys.exit(1)

    BASE_URL = AUTHENTIK_URL
    AUTHORIZE_URL = f"{BASE_URL}/application/o/authorize/"
    ACCESS_TOKEN_URL = f"{BASE_URL}/application/o/token/"
    REDIRECT_URL = f"{ERPNEXT_URL}/api/method/frappe.integrations.oauth2_logins.custom/authentik"
    API_ENDPOINT = f"{BASE_URL}/application/o/userinfo/"
    
    # Required parameters for Authentik PKCE/OAuth2
    AUTH_URL_DATA = json.dumps({
        "response_type": "code",
        "scope": "openid profile email"
    })

    print(f"Configuring OIDC for provider: {PROVIDER_NAME}")

    # 1. Enable Global Signups (Required for first-time OIDC user creation via Web)
    print("Enabling Global Signups in Website Settings...")
    # Use db.set_value to avoid loading the controller which might be missing/broken in this context
    # This bypasses: ModuleNotFoundError: No module named 'frappe.core.doctype.website_settings'
    try:
        frappe.db.set_value("Website Settings", "Website Settings", "disable_signup", 0)
        frappe.db.commit()
    except Exception as e:
        print(f"Warning: Failed to enable global signups via set_value: {e}")

    # Cleanup old uppercase provider if it exists
    if frappe.db.exists("Social Login Key", "Authentik"):
        frappe.delete_doc("Social Login Key", "Authentik", ignore_permissions=True, force=True)
        frappe.db.commit()
        print("Deleted old 'Authentik' (uppercase) provider.")

    # Create or Update Social Login Key
    if not frappe.db.exists("Social Login Key", PROVIDER_NAME):
        print(f"Creating new provider '{PROVIDER_NAME}'...")
        doc = frappe.new_doc("Social Login Key")
        doc.name = PROVIDER_NAME
        doc.social_login_provider = "Custom"
    else:
        print(f"Updating existing provider '{PROVIDER_NAME}'...")
        doc = frappe.get_doc("Social Login Key", PROVIDER_NAME)

    # Update Fields
    doc.provider_name = LABEL_NAME
    doc.enable_social_login = 1
    doc.client_id = CLIENT_ID
    doc.client_secret = CLIENT_SECRET
    doc.base_url = BASE_URL
    doc.authorize_url = AUTHORIZE_URL
    doc.access_token_url = ACCESS_TOKEN_URL
    doc.redirect_url = REDIRECT_URL
    doc.api_endpoint = API_ENDPOINT
    doc.auth_url_data = AUTH_URL_DATA
    doc.icon = "fa fa-lock" 
    doc.custom_base_url = 1 
    
    # Vital for mapping user
    doc.user_id_property = "email"
    
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    print(f"Successfully configured and enabled '{PROVIDER_NAME}' OIDC.")

if __name__ == "__main__":
    try:
        configure_authentik()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
