"""
KalevioAI Mailer — Resend-powered email alerts
Sends NIS2 incident notifications and CSIRT early warnings.
"""
import logging
import httpx
from core.config import settings

logger = logging.getLogger(__name__)

async def send_email(to: str, subject: str, html: str) -> bool:
    """Send email via Resend API. Returns True on success."""
    if not settings.RESEND_API_KEY:
        logger.warning("RESEND_API_KEY not set — email not sent")
        return False
    try:
        async with httpx.AsyncClient() as client:
            r = await client.post(
                "https://api.resend.com/emails",
                headers={
                    "Authorization": f"Bearer {settings.RESEND_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "from": settings.RESEND_FROM_EMAIL,
                    "to": [to],
                    "subject": subject,
                    "html": html,
                },
                timeout=10.0,
            )
            r.raise_for_status()
            logger.info(f"Email sent to {to}: {subject}")
            return True
    except Exception as e:
        logger.error(f"Email failed to {to}: {e}")
        return False

async def send_nis2_incident_alert(
    to: str,
    reference_id: str,
    threat_type: str,
    severity: str,
    z_score: float,
    early_warning_due: str,
    notification_due: str,
    final_report_due: str,
) -> bool:
    """Send NIS2 incident alert email when a reportable incident is detected."""
    subject = f"⚠️ NIS2 Alert: {severity.upper()} incident detected — {reference_id}"
    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f5f5; margin: 0; padding: 20px; }}
  .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 8px; overflow: hidden; }}
  .header {{ background: #010308; color: white; padding: 24px 32px; }}
  .header h1 {{ margin: 0; font-size: 20px; font-weight: 600; }}
  .header p {{ margin: 4px 0 0; color: #888; font-size: 13px; }}
  .badge {{ display: inline-block; background: #dc2626; color: white; padding: 4px 12px; border-radius: 4px; font-size: 12px; font-weight: 700; letter-spacing: 0.05em; margin-bottom: 16px; }}
  .body {{ padding: 32px; }}
  .field {{ margin-bottom: 16px; }}
  .label {{ font-size: 11px; font-weight: 600; color: #888; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px; }}
  .value {{ font-size: 15px; color: #111; font-weight: 500; }}
  .deadlines {{ background: #fef2f2; border: 1px solid #fee2e2; border-radius: 6px; padding: 16px 20px; margin: 24px 0; }}
  .deadlines h3 {{ margin: 0 0 12px; font-size: 13px; color: #dc2626; text-transform: uppercase; letter-spacing: 0.05em; }}
  .deadline-row {{ display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 14px; }}
  .deadline-label {{ color: #555; }}
  .deadline-value {{ color: #111; font-weight: 600; font-family: monospace; }}
  .cta {{ text-align: center; margin: 24px 0; }}
  .btn {{ display: inline-block; background: #1d6fff; color: white; padding: 12px 28px; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 14px; }}
  .footer {{ padding: 16px 32px; background: #f9f9f9; border-top: 1px solid #eee; font-size: 12px; color: #888; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>KalevioAI — NIS2 Incident Alert</h1>
    <p>Automated regulatory notification</p>
  </div>
  <div class="body">
    <div class="badge">{severity.upper()} SEVERITY</div>
    <div class="field">
      <div class="label">Incident Reference</div>
      <div class="value">{reference_id}</div>
    </div>
    <div class="field">
      <div class="label">Threat Type</div>
      <div class="value">{threat_type}</div>
    </div>
    <div class="field">
      <div class="label">Anomaly Score (Z)</div>
      <div class="value">{z_score}</div>
    </div>
    <div class="deadlines">
      <h3>⏱ NIS2 Article 23 Reporting Deadlines</h3>
      <div class="deadline-row">
        <span class="deadline-label">Early Warning (Art. 23(1)(a))</span>
        <span class="deadline-value">{early_warning_due}</span>
      </div>
      <div class="deadline-row">
        <span class="deadline-label">Notification (Art. 23(1)(b))</span>
        <span class="deadline-value">{notification_due}</span>
      </div>
      <div class="deadline-row">
        <span class="deadline-label">Final Report (Art. 23(1)(c))</span>
        <span class="deadline-value">{final_report_due}</span>
      </div>
    </div>
    <div class="cta">
      <a href="https://kalevio.tinlance.com" class="btn">Generate NIS2 Report →</a>
    </div>
    <p style="font-size:13px;color:#555;">This incident has been classified as NIS2-reportable. 
    You must submit an early warning to your national CSIRT within 24 hours. 
    KalevioAI can generate the full Article 23 report automatically.</p>
  </div>
  <div class="footer">
    KalevioAI · Tinlance OÜ · Tallinn, Estonia · EU data residency
    <br>You received this because a significant incident was detected on your account.
  </div>
</div>
</body>
</html>
"""
    return await send_email(to, subject, html)
