from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm

path = "./thesis_print_sheets_A4.pdf"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="H", fontSize=14, spaceAfter=6, spaceBefore=6, leading=16))

doc = SimpleDocTemplate(
    path,
    pagesize=A4,
    rightMargin=40,
    leftMargin=40,
    topMargin=20,
    bottomMargin=20,
)

elements = []

from reportlab.platypus import Spacer

def vspace(h=8):
    elements.append(Spacer(1, h))

def header(text):
    elements.append(Paragraph(f"<b>{text}</b>", styles["H"]))

# improved grid function with top-left alignment and reduced padding
def grid(rows, cols, row_height, col_widths=None):
    if col_widths is None:
        col_widths = [(A4[0] - 60) / cols] * cols

    tbl = Table(
        [["" for _ in range(cols)] for _ in range(rows)],
        colWidths=col_widths,
        rowHeights=[row_height] * rows
    )

    tbl.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.7, colors.black),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 4),
        ("RIGHTPADDING", (0,0), (-1,-1), 4),
        ("TOPPADDING", (0,0), (-1,-1), 2),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2),
    ]))

    elements.append(tbl)

def pct_cols(*pcts):
    usable = A4[0] - 60
    return [usable * p for p in pcts]



def footer(canvas, doc):
    canvas.saveState()

    canvas.setFont("Times-Italic", 10)
    canvas.setFillColor(colors.grey)

    canvas.drawCentredString(
        A4[0] / 2,
        10 * mm,          # distance from bottom
        "Master's Thesis planner — Ravisankar Selvaraju"
    )

    canvas.restoreState()


# # Weekly Block Planner — PORTRAIT OPTIMIZED
# header("WEEKLY THESIS PLANNER (BLOCK-BASED SCHEDULING)")
# vspace(6)

# elements.append(Paragraph(
#     "Month: ____________     Week #: _____/29 &nbsp;&nbsp;&nbsp;     Planned on: ___/____/2026",
#     styles["Normal"]
# ))
# vspace(6)


# elements.append(Paragraph(
#     "Weekly Outcome (what must exist by end of week):",
#     styles["Normal"]
# ))
# grid(2, 1, 40)
# vspace(6)
# elements.append(Paragraph(
#     "Available Work Blocks (tick):  [ ]1  [ ]2  [ ]3  [ ]4  [ ]5",
#     styles["Normal"]
# ))
# vspace(6)   
# elements.append(Paragraph(
#     "Block Plan (one block per row):",
#     styles["Normal"]
# ))
# grid(5, 1, 40)
  
# vspace(6)   
# elements.append(Paragraph(
#     "Minimum Viable Week (if only 1–2 blocks happen):",
#     styles["Normal"]
# ))
# grid(2, 1, 40)
# vspace(6)
    
# elements.append(Paragraph(
#     "End-of-Week Review (facts only):",
#     styles["Normal"]
# ))
# grid(2, 1, 35)
# vspace(6)

# elements.append(Paragraph(
#     "Remarks / Scratch / Overflow:",
#     styles["Normal"]
# ))
# grid(1, 1, 180)


# elements.append(PageBreak())
# ----------------------------------------------------------------------------------------------------------

# # Daily Focus Sheet
# header("DAILY FOCUS SHEET &nbsp;&nbsp;&nbsp;&nbsp; [Make a plan, Follow the plan]")
# vspace(6)

# week_header = Table(
#     [[
#         Paragraph(
#             "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Week #: ______/29&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Date: ___/____/2026",
#             styles["Normal"]
#         ),
#         Paragraph(
#             "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
#             "<font size=18>✓</font> Done&nbsp;&nbsp;"
#             "<font size=18>✗</font> Not Done&nbsp;&nbsp;"
#             "<font size=25>→</font> Moved Forward",
#             styles["Normal"]
#         )
#     ]],
#     colWidths=pct_cols(0.5, 0.5),  # left text, right legend
# )
# week_header.setStyle(TableStyle([
#     ("ALIGN", (0,0), (0,0), "LEFT"),     # Week/Date left
#     ("ALIGN", (1,0), (1,0), "RIGHT"),    # Legend right
#     ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
#     ("LEFTPADDING", (0,0), (-1,-1), 0),
#     ("RIGHTPADDING", (0,0), (-1,-1), 0),
#     ("TOPPADDING", (0,0), (-1,-1), 2),
#     ("BOTTOMPADDING", (0,0), (-1,-1), 2),
# ]))

# elements.append(week_header)
# vspace(6)

# elements.append(Paragraph("Primary Task (ONE):", styles["Normal"]))
# grid(1, 2, 40, col_widths=pct_cols(0.92, 0.08))
# vspace(6)
# elements.append(Paragraph("Secondary Tasks (max 5):", styles["Normal"]))
# grid(5, 2, 30, col_widths=pct_cols(0.92, 0.08))
# vspace(6)
# elements.append(Paragraph("Notes / Equations / Sketches:", styles["Normal"]))
# grid(4, 1, 28)
# vspace(6)
# elements.append(Paragraph("End-of-Day Review (facts only):", styles["Normal"]))
# grid(2, 2, 30)
# vspace(6)
# elements.append(Paragraph(
#     "Remarks / Scratch / Overflow:",
#     styles["Normal"]
# ))

# grid(1, 1, 265)


# elements.append(PageBreak())
# ----------------------------------------------------------------------------------------------------------


# # Experiment Log
# header("EXPERIMENT LOG")
# elements.append(Paragraph("Hypothesis / Question:", styles["Normal"]))
# grid(1, 1, 40)

# elements.append(Paragraph("Setup (robot, sensors, params, code version):", styles["Normal"]))
# grid(2, 2, 35)

# elements.append(Paragraph("Results (what actually happened):", styles["Normal"]))
# grid(2, 2, 35)

# elements.append(Paragraph("Insights / Next Action:", styles["Normal"]))
# grid(2, 1, 35)

# elements.append(PageBreak())

# ------------------------------------------------------------------------------------------

# Paper Reading Sheet — THINKING-ORIENTED
header("LITERATURE READING SHEET")
vspace(6)

elements.append(Paragraph(
    "Read on: ___/____/2026",
    styles["Normal"]
))
vspace(6)


elements.append(Paragraph("<b>Citation</b> (authors, year, venue):"))
grid(1, 1, 45)
vspace(6)

elements.append(Paragraph(
    "<b>Problem</b> (what exactly are they solving?):",
    styles["Normal"]
))
grid(1, 1, 60)
vspace(6)

elements.append(Paragraph(
    "<b>Core Idea / Method</b> (in my own words):",
    styles["Normal"]
))
grid(5, 1, 25)
vspace(6)

elements.append(Paragraph(
    "<b>Key Result / Claim</b> (what did they show?):",
    styles["Normal"]
))
grid(3, 1, 25)
vspace(6)

elements.append(Paragraph(
    "<b>Assumptions / Limitations</b> (what must be true?):",
    styles["Normal"]
))
grid(2, 1, 30)
vspace(6)

elements.append(Paragraph(
    "<b>Connection to My Thesis</b> (USE / IGNORE / QUESTION):",
    styles["Normal"]
))
grid(2, 1, 32)
vspace(6)

elements.append(Paragraph(
    "<b>Action After Reading</b> (one concrete next step):",
    styles["Normal"]
))
grid(1, 1, 28)
vspace(6)

elements.append(Paragraph(
    "<b>Remarks</b>:",
    styles["Normal"]
))
grid(1, 1, 120)
vspace(6)

elements.append(PageBreak())


# -------------------------------------------------------------------------------------------

# # Chapter Progress Tracker
# header("CHAPTER / SECTION PROGRESS TRACKER")
# elements.append(Paragraph("Rows = chapters or sections | Columns = stages", styles["Normal"]))
# grid(8, 6, 30)


doc.build(
    elements,
    onFirstPage=footer,
    onLaterPages=footer
)

print(f"Planner PDF generated at: {path}")
