import frappe
import sys

def enable_features():
    try:
        # Initialize site context
        if len(sys.argv) > 1:
            site_name = sys.argv[1]
        else:
            site_name = "erpnext.homelab.local"
            
        frappe.init(site=site_name, sites_path='sites')
        frappe.connect()

        print(f"Starting ERPNext Feature Enablement for site: {site_name}")
        

        # 1. Complete Setup & Fix Missing Defaults
        system_settings = frappe.get_single('System Settings')
        
        # Set defaults if missing to pass validation
        if not system_settings.language:
            system_settings.language = "en"
        if not system_settings.time_zone:
            system_settings.time_zone = "Europe/Berlin" # Defaulting for homelab
        if not system_settings.country:
            system_settings.country = "United States" # Generic default
        
        system_settings.save(ignore_permissions=True)
        print("System Settings saved successfully.")


        # Enable Global Signups (Corrected)
        web_settings = frappe.get_doc("Website Settings")
        if web_settings.disable_signup:
            web_settings.disable_signup = 0
            web_settings.save(ignore_permissions=True)
            print("Enabled Auto Signup in Website Settings.")

        # 2. Enable Domains
        # These are standard domains. Validated against V15/V16 common domains.
        target_domains = [
            'Manufacturing', 
            'Retail', 
            'Distribution', 
            'Services', 
            'Education', 
            'Agriculture', 
            'Non Profit', 
            'Hospitality', 
            'Healthcare'
        ]

        domain_settings = frappe.get_doc('Domain Settings')
        
        # Explicitly delete child rows from DB to clear ghosts
        frappe.db.delete("Has Domain", {"parent": "Domain Settings"})
        
        # Reload doc to reflect DB state
        domain_settings.reload()
        
        # Now append target domains via SQL to bypass ORM validation issues
        values = []
        for domain in target_domains:
             name = frappe.generate_hash(length=10)
             idx = len(values) + 1
             values.append(f"('{name}', NOW(), NOW(), 'Administrator', 'Administrator', 0, 'Domain Settings', 'active_domains', 'Domain Settings', {idx}, '{domain}')")
             print(f"Queueing domain: {domain}")
        
        if values:
            query = f"INSERT INTO `tabHas Domain` (`name`, `creation`, `modified`, `modified_by`, `owner`, `docstatus`, `parent`, `parentfield`, `parenttype`, `idx`, `domain`) VALUES {', '.join(values)}"
            frappe.db.sql(query)
            print(f"Inserted {len(values)} domains via SQL.")

        # 3. Pre-provision Authentik Admin Users
        # Authentik might be sending akadmin@homelab.local or similar.
        # We ensure they exist and have System Manager role.
        targets = ['akadmin@homelab.local', 'admin@homelab.local', 'citrullin@homelab.local', 'root@example.com', '0x918c30482462C8024ba6Cf34a18ba1f8bBdb755F@ens.eth']
        
        for email in targets:
            if not frappe.db.exists("User", email):
                user = frappe.new_doc("User")
                user.email = email
                user.first_name = email.split("@")[0].capitalize()
                user.enabled = 1
                user.user_type = "System User"
                user.send_welcome_email = 0
                user.save(ignore_permissions=True)
                print(f"Created user: {email}")
            else:
                print(f"User exists: {email}")
                
            # Assign Administrative Roles
            user_doc = frappe.get_doc("User", email)
            
            # Ensure System User type
            if user_doc.user_type != "System User":
                 user_doc.user_type = "System User"
                 user_doc.save(ignore_permissions=True)
                 print(f"Promoted {email} to System User")

            # Assign a very broad set of roles to ensure full access
            all_roles = frappe.get_all("Role", pluck="name")
            roles_to_add = [r for r in all_roles if r not in ["Guest", "All"]]
            
            user_doc.add_roles(*roles_to_add)
            
            print(f"Assigned all available roles to {email}")

        # 4. Set site configuration for correct link generation and CORS
        from frappe.installer import update_site_config
        print("Updating site configuration for HTTPS and CORS...")
        update_site_config("host_name", "https://erpnext.homelab.local")
        update_site_config("http_port", 443)
        update_site_config("allow_cors", "https://erpnext.homelab.local")
        print("Updated host_name, http_port, and allow_cors in site_config.json")


        frappe.db.commit()
        print("Successfully updated ERPNext settings and users.")
        
    except Exception as e:
        print(f"Error configuring ERPNext settings: {e}")
        try:
            frappe.db.rollback()
        except:
            pass
        sys.exit(1)
    finally:
        try:
            frappe.destroy()
        except:
            pass

if __name__ == "__main__":
    enable_features()
