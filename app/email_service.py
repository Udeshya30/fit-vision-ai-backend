import smtplib
from email.message import EmailMessage
from app.config import (
    SMTP_HOST,
    SMTP_PORT,
    SMTP_USER,
    SMTP_PASSWORD,
    ADMIN_EMAIL,
    FRONTEND_BASE_URL,
)

# =========================
# CONTACT EMAIL (ADMIN)
# =========================
def send_contact_email(name: str, email: str, message: str):
    msg = EmailMessage()
    msg["Subject"] = "New Contact Form Submission"
    msg["From"] = f"FitVisionAI <{SMTP_USER}>"
    msg["To"] = ADMIN_EMAIL

    msg.set_content("New contact form submission.")
    msg.add_alternative(
        f"""
<!DOCTYPE html>
<html>
  <body style="background:#F8FAFC;font-family:Arial,sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0">
      <tr>
        <td align="center" style="padding:40px;">
          <table width="600" style="background:#ffffff;border-radius:16px;border:1px solid #E2E8F0;padding:32px;">
            <tr>
              <td>
                <h2 style="color:#0F172A;">New Contact Message</h2>

                <p><strong>Name:</strong> {name}</p>
                <p><strong>Email:</strong> {email}</p>

                <div style="margin-top:20px;padding:16px;background:#F1F5F9;border-radius:8px;">
                  <p style="margin:0;color:#0F172A;">{message}</p>
                </div>

              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
        """,
        subtype="html",
    )

    _send(msg)


# =========================
# WELCOME EMAIL
# =========================
def send_welcome_email(email: str, name: str):
    msg = EmailMessage()
    msg["Subject"] = "Welcome to FitVisionAI 👋"
    msg["From"] = f"FitVisionAI <{SMTP_USER}>"
    msg["To"] = email

    msg.set_content("Welcome to FitVisionAI.")
    msg.add_alternative(
        f"""
<!DOCTYPE html>
<html>
  <body style="background:#F8FAFC;font-family:Arial,sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0">
      <tr>
        <td align="center" style="padding:40px;">
          <table width="600" style="background:#ffffff;border-radius:16px;border:1px solid #E2E8F0;padding:32px;">
            <tr>
              <td align="center">
                <h1 style="color:#0F172A;">FitVisionAI</h1>
                <p style="color:#64748B;">Your personal health & fitness guide</p>
              </td>
            </tr>

            <tr>
              <td style="padding-top:24px;color:#0F172A;">
                <p>Hi <strong>{name}</strong>,</p>

                <p>Your account has been created successfully.</p>

                <div style="text-align:center;margin:32px 0;">
                  <a
                    href="{FRONTEND_BASE_URL}/onboarding"
                    style="background:#14B8A6;color:#ffffff;padding:14px 24px;border-radius:10px;text-decoration:none;font-weight:600;"
                  >
                    Complete Onboarding
                  </a>
                </div>

                <p>We’re excited to help you build healthier habits.</p>

                <p>– Team FitVisionAI</p>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
        """,
        subtype="html",
    )

    _send(msg)


# =========================
# RESET PASSWORD EMAIL
# =========================
def send_reset_password_email(email: str, reset_link: str):
    msg = EmailMessage()
    msg["Subject"] = "Reset your FitVisionAI password"
    msg["From"] = f"FitVisionAI <{SMTP_USER}>"
    msg["To"] = email

    msg.set_content("Reset your password.")
    msg.add_alternative(
        f"""
<!DOCTYPE html>
<html>
  <body style="background:#F8FAFC;font-family:Arial,sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0">
      <tr>
        <td align="center" style="padding:40px;">
          <table width="600" style="background:#ffffff;border-radius:16px;border:1px solid #E2E8F0;padding:32px;">
            <tr>
              <td align="center">
                <h2 style="color:#0F172A;">Reset your password</h2>
                <p style="color:#64748B;">This link expires in 15 minutes.</p>

                <div style="margin:32px 0;">
                  <a
                    href="{reset_link}"
                    style="background:#14B8A6;color:#ffffff;padding:14px 24px;border-radius:10px;text-decoration:none;font-weight:600;"
                  >
                    Reset Password
                  </a>
                </div>

                <p style="font-size:13px;color:#94A3B8;">
                  If you didn’t request this, you can safely ignore this email.
                </p>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
        """,
        subtype="html",
    )

    _send(msg)


# =========================
# PASSWORD CHANGED EMAIL
# =========================
def send_password_changed_email(email: str, name: str):
    msg = EmailMessage()
    msg["Subject"] = "Your FitVisionAI password was changed"
    msg["From"] = f"FitVisionAI <{SMTP_USER}>"
    msg["To"] = email

    msg.set_content("Your password has been changed.")
    msg.add_alternative(
        f"""
<!DOCTYPE html>
<html>
  <body style="background:#F8FAFC;font-family:Arial,sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0">
      <tr>
        <td align="center" style="padding:40px;">
          <table width="600" style="background:#ffffff;border-radius:16px;border:1px solid #E2E8F0;padding:32px;">
            <tr>
              <td>
                <h2 style="color:#0F172A;">Password Changed</h2>

                <p>Hi <strong>{name}</strong>,</p>

                <p>Your FitVisionAI password was changed successfully.</p>

                <p style="background:#F1F5F9;padding:12px;border-radius:8px;">
                  If this wasn’t you, please secure your account immediately.
                </p>

                <div style="margin-top:24px;">
                  <a
                    href="{FRONTEND_BASE_URL}/forgot-password"
                    style="background:#14B8A6;color:#ffffff;padding:12px 22px;border-radius:10px;text-decoration:none;font-weight:600;"
                  >
                    Secure My Account
                  </a>
                </div>

                <p style="margin-top:24px;">– Team FitVisionAI</p>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
        """,
        subtype="html",
    )

    _send(msg)


# =========================
# INTERNAL SMTP SENDER
# =========================
def _send(msg: EmailMessage):
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
