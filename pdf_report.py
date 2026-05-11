from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER
from io import BytesIO
from datetime import datetime

# ── COLORS ───────────────────────────────────────────────────
GREEN       = colors.HexColor('#0a4d2e')
LIGHT_GREEN = colors.HexColor('#1a7a45')
GOLD        = colors.HexColor('#c9a84c')
BG_GREEN    = colors.HexColor('#f0fdf4')
BG_RED      = colors.HexColor('#fff5f5')
RED         = colors.HexColor('#b91c1c')
GRAY        = colors.HexColor('#6b9e77')
LIGHT_GRAY  = colors.HexColor('#f0f6f1')
WHITE       = colors.white
DARK        = colors.HexColor('#1a2e1e')


def generate_pdf(input_data: dict, result: dict) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=18*mm, bottomMargin=18*mm
    )
    story = []
    approved = result.get('approved') == 1
    prob     = result.get('probability', 0)
    status   = 'APPROVED' if approved else 'NOT APPROVED'
    s_color  = LIGHT_GREEN if approved else RED
    bg_color = BG_GREEN    if approved else BG_RED

    # ── HEADER ───────────────────────────────────────────────
    hdr = Table([['  CreditIQ Banking', 'Loan Eligibility Report  ']],
                colWidths=[95*mm, 85*mm])
    hdr.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), GREEN),
        ('TEXTCOLOR',     (0,0), (-1,-1), WHITE),
        ('FONTNAME',      (0,0), (0,0),   'Helvetica-Bold'),
        ('FONTSIZE',      (0,0), (0,0),   16),
        ('FONTNAME',      (1,0), (1,0),   'Helvetica'),
        ('FONTSIZE',      (1,0), (1,0),   11),
        ('ALIGN',         (0,0), (0,0),   'LEFT'),
        ('ALIGN',         (1,0), (1,0),   'RIGHT'),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',    (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LEFTPADDING',   (0,0), (0,0),   12),
        ('RIGHTPADDING',  (1,0), (1,0),   12),
    ]))
    story.append(hdr)
    story.append(Spacer(1, 7*mm))

    # ── RESULT BANNER ────────────────────────────────────────
    banner = Table([[f'  {status}  ', f'  Confidence: {prob}%  ']],
                   colWidths=[110*mm, 70*mm])
    banner.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), bg_color),
        ('TEXTCOLOR',     (0,0), (-1,-1), s_color),
        ('FONTNAME',      (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE',      (0,0), (0,0),   20),
        ('FONTSIZE',      (1,0), (1,0),   14),
        ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',    (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('BOX',           (0,0), (-1,-1), 1.5, s_color),
    ]))
    story.append(banner)
    story.append(Spacer(1, 7*mm))

    # ── HELPER: section title ────────────────────────────────
    def sec(title):
        story.append(Paragraph(
            f'<font color="#0a4d2e"><b>{title}</b></font>',
            ParagraphStyle('s', fontSize=12, spaceAfter=3, fontName='Helvetica-Bold')
        ))
        story.append(HRFlowable(width='100%', thickness=1.5,
                                color=LIGHT_GREEN, spaceAfter=4))

    # ── HELPER: info table ───────────────────────────────────
    def info(rows):
        t = Table(rows, colWidths=[68*mm, 112*mm])
        t.setStyle(TableStyle([
            ('FONTNAME',      (0,0), (0,-1),  'Helvetica-Bold'),
            ('FONTNAME',      (1,0), (1,-1),  'Helvetica'),
            ('FONTSIZE',      (0,0), (-1,-1), 10),
            ('TEXTCOLOR',     (0,0), (0,-1),  GRAY),
            ('TEXTCOLOR',     (1,0), (1,-1),  DARK),
            ('ROWBACKGROUNDS',(0,0), (-1,-1), [WHITE, LIGHT_GRAY]),
            ('TOPPADDING',    (0,0), (-1,-1), 7),
            ('BOTTOMPADDING', (0,0), (-1,-1), 7),
            ('LEFTPADDING',   (0,0), (-1,-1), 10),
            ('GRID',          (0,0), (-1,-1), 0.5, colors.HexColor('#e0ede3')),
        ]))
        story.append(t)
        story.append(Spacer(1, 5*mm))

    # ── PERSONAL ─────────────────────────────────────────────
    sec('Personal Details')
    info([
        ['Applicant Name', str(input_data.get('name', '—'))],
        ['Age',            str(input_data.get('age',  '—'))],
        ['Gender',         str(input_data.get('gender','—'))],
        ['Marital Status', str(input_data.get('married','—'))],
        ['Education',      str(input_data.get('edu',  '—'))],
    ])

    # ── INCOME ───────────────────────────────────────────────
    sec('Income & Employment')
    income   = float(input_data.get('income', 0))
    coincome = float(input_data.get('coincome', 0))
    info([
        ['Employment Type',    str(input_data.get('emp', '—'))],
        ['Monthly Income',     f'Rs.{int(income):,}'],
        ['Co-Applicant Income',f'Rs.{int(coincome):,}'],
        ['Work Experience',    f"{input_data.get('exp','—')} years"],
    ])

    # ── LOAN ─────────────────────────────────────────────────
    sec('Loan Details')
    lamt  = float(input_data.get('lamt', 0))
    lterm = int(input_data.get('lterm', 360))
    emi   = int(lamt / lterm) if lterm else 0
    info([
        ['Loan Amount',   f'Rs.{int(lamt):,}'],
        ['Loan Term',     f'{lterm} months'],
        ['Property Area', str(input_data.get('prop',   '—'))],
        ['Loan Purpose',  str(input_data.get('purpose','—'))],
        ['Est. Monthly EMI', f'Rs.{emi:,}'],
    ])

    # ── CREDIT ───────────────────────────────────────────────
    sec('Credit Information')
    ch = str(input_data.get('ch', '0'))
    info([
        ['CIBIL Score',    str(input_data.get('cibil', '—'))],
        ['Credit History', 'Good (No defaults)' if ch == '1' else 'Bad (Has defaults)'],
    ])

    # ── FEATURE IMPORTANCE ────────────────────────────────────
    fi = result.get('feature_importance', {})
    if fi:
        sec('Feature Importance (Top 5)')
        top5 = sorted(fi.items(), key=lambda x: x[1], reverse=True)[:5]
        fi_tbl = Table([[k, f'{v}%'] for k,v in top5],
                       colWidths=[120*mm, 60*mm])
        fi_tbl.setStyle(TableStyle([
            ('FONTNAME',      (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE',      (0,0), (-1,-1), 10),
            ('ROWBACKGROUNDS',(0,0), (-1,-1), [WHITE, LIGHT_GRAY]),
            ('GRID',          (0,0), (-1,-1), 0.5, colors.HexColor('#e0ede3')),
            ('TOPPADDING',    (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING',   (0,0), (-1,-1), 10),
            ('TEXTCOLOR',     (1,0), (1,-1),  LIGHT_GREEN),
            ('FONTNAME',      (1,0), (1,-1),  'Helvetica-Bold'),
        ]))
        story.append(fi_tbl)
        story.append(Spacer(1, 5*mm))

    # ── TIPS ─────────────────────────────────────────────────
    sec('Eligibility Tips & Suggestions')
    for tip in get_tips(input_data, result):
        story.append(Paragraph(
            f'• {tip}',
            ParagraphStyle('tip', fontSize=10, leftIndent=10,
                           spaceAfter=4, leading=14, textColor=DARK)
        ))
    story.append(Spacer(1, 6*mm))

    # ── FOOTER ───────────────────────────────────────────────
    ts = datetime.now().strftime('%d %b %Y, %I:%M %p')
    ftr = Table([[f'Generated: {ts}  |  CreditIQ Banking System  |  Confidential']],
                colWidths=[180*mm])
    ftr.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), GREEN),
        ('TEXTCOLOR',     (0,0), (-1,-1), colors.HexColor('#a0c8a8')),
        ('FONTNAME',      (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE',      (0,0), (-1,-1), 9),
        ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING',    (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(ftr)
    doc.build(story)
    return buffer.getvalue()


def get_tips(data: dict, result: dict) -> list:
    tips     = []
    cibil    = int(data.get('cibil', 0))
    income   = float(data.get('income', 0))
    lamt     = float(data.get('lamt', 0))
    lterm    = int(data.get('lterm', 360))
    ch       = str(data.get('ch', '0'))
    approved = result.get('approved') == 1

    if approved:
        tips.append('Congratulations! Your profile meets the loan eligibility criteria.')
        tips.append('Visit your nearest bank branch with valid KYC documents to proceed.')
        tips.append('Keep your CIBIL score above 750 for better interest rates.')
        tips.append('Ensure timely EMI payments to maintain a good credit history.')
    else:
        if cibil < 650:
            tips.append(f'Your CIBIL score is {cibil}. Aim for 750+ by paying all bills on time.')
        elif cibil < 750:
            tips.append(f'CIBIL score {cibil} is average. Improving to 750+ will boost approval chances.')
        if ch == '0':
            tips.append('Resolve any existing loan defaults or missed payments immediately.')
        monthly = lamt / lterm if lterm > 0 else 0
        if income > 0 and monthly / income > 0.4:
            tips.append('Your EMI exceeds 40% of income. Reduce the loan amount or extend the tenure.')
        lti = lamt / (income * 12) if income > 0 else 999
        if lti > 5:
            tips.append(f'Loan amount is {lti:.1f}x your annual income. Consider a lower amount.')
        tips.append('Try applying again in 3-6 months after improving your financial profile.')

    return tips