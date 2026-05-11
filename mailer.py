import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ── CONFIG ───────────────────────────────────────────────────
# Replace with your Gmail and App Password
# To get App Password:
#   Google Account → Security → 2-Step Verification → App Passwords
GMAIL_USER = "shainshafi1717@gmail.com"
GMAIL_PASS = "udtl xkel fgvu nwds"


def send_result_email(to_email: str, applicant: str, result: dict) -> bool:
    approved    = result.get('approved') == 1
    probability = result.get('probability', 0)
    status      = 'APPROVED' if approved else 'NOT APPROVED'
    s_color     = '#15803d'  if approved else '#b91c1c'
    bg_color    = '#f0fdf4'  if approved else '#fff5f5'
    border      = '#22c55e'  if approved else '#f05a5a'
    icon        = '✅'        if approved else '❌'

    tip_html = (
        '<p style="font-size:14px;color:#15803d;background:#f0fdf4;'
        'padding:14px;border-radius:9px;margin:0">'
        '🎉 Congratulations! Your loan application meets the eligibility '
        'criteria. Please visit your nearest branch to proceed.</p>'
        if approved else
        '<p style="font-size:14px;color:#b91c1c;background:#fff5f5;'
        'padding:14px;border-radius:9px;margin:0">'
        '💡 <b>Tips to improve:</b><br/>'
        '• Aim for a CIBIL score of 750+<br/>'
        '• Reduce existing EMIs below 40% of income<br/>'
        '• Resolve any loan defaults<br/>'
        '• Try again in 3–6 months</p>'
    )

    html = f"""
    <html>
    <body style="font-family:'Segoe UI',Arial,sans-serif;
                 background:#f0f6f1;padding:32px;margin:0">
      <div style="max-width:560px;margin:0 auto;background:#fff;
                  border-radius:16px;overflow:hidden;
                  box-shadow:0 4px 24px rgba(0,0,0,.10)">

        <!-- Header -->
        <div style="background:linear-gradient(135deg,#0a4d2e,#1a7a45);
                    padding:28px 32px;text-align:center">
          <h1 style="color:#fff;font-size:26px;margin:0;font-weight:800">
            🏠 CreditIQ Banking
          </h1>
          <p style="color:rgba(255,255,255,.75);margin:6px 0 0;font-size:14px">
            Loan Eligibility Prediction Result
          </p>
        </div>

        <!-- Body -->
        <div style="padding:32px">
          <p style="font-size:15px;color:#1a2e1e;margin:0 0 6px">
            Dear <b>{applicant}</b>,
          </p>
          <p style="font-size:14px;color:#4a8c5c;margin:0 0 24px">
            Your loan eligibility prediction result is ready.
          </p>

          <!-- Result card -->
          <div style="background:{bg_color};border:2px solid {border};
                      border-radius:12px;padding:24px;text-align:center;
                      margin-bottom:24px">
            <div style="font-size:38px;margin-bottom:6px">{icon}</div>
            <div style="font-size:28px;font-weight:900;color:{s_color}">
              {status}
            </div>
            <div style="font-size:48px;font-weight:900;color:{s_color};
                        margin:8px 0">{probability}%</div>
            <div style="font-size:13px;color:#6b9e77">ML Confidence Score</div>
          </div>

          <!-- Tips -->
          {tip_html}

          <hr style="border:none;border-top:1px solid #e0ede3;margin:24px 0"/>

          <p style="font-size:12px;color:#9ab89f;text-align:center;margin:0">
            This is an automated email from CreditIQ Banking System.<br/>
            Please do not reply to this email.
          </p>
        </div>
      </div>
    </body>
    </html>"""

    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'CreditIQ — Loan Result: {icon} {status}'
        msg['From']    = GMAIL_USER
        msg['To']      = to_email
        msg.attach(MIMEText(html, 'html'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_PASS)
            server.sendmail(GMAIL_USER, to_email, msg.as_string())

        print(f'Email sent to {to_email}')
        return True

    except Exception as e:
        print(f'Email error: {e}')
        return False