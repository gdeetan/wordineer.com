from fpdf import FPDF
from fpdf.enums import XPos, YPos

class PDF(FPDF):
    def header(self):
        self.set_fill_color(52, 52, 137)
        self.rect(0, 0, 210, 32, 'F')
        self.set_font('Helvetica', 'B', 17)
        self.set_text_color(255, 255, 255)
        self.set_xy(14, 11)
        self.cell(0, 10, 'Wordineer - New Tool Deployment Guide',
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def footer(self):
        self.set_y(-12)
        self.set_font('Helvetica', '', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 8, f'Page {self.page_no()}', align='C')

pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=16)
pdf.add_page()
pdf.set_margins(14, 36, 14)

PW = 182  # usable page width


def h1(text):
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(52, 52, 137)
    pdf.ln(6)
    pdf.cell(0, 8, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_draw_color(52, 52, 137)
    pdf.line(14, pdf.get_y(), 196, pdf.get_y())
    pdf.ln(3)

def body(text):
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(PW, 5.5, text)
    pdf.ln(1)

def code(text):
    pdf.set_fill_color(245, 245, 248)
    pdf.set_draw_color(210, 210, 220)
    pdf.set_font('Courier', '', 9)
    pdf.set_text_color(40, 40, 40)
    lines = text.strip().split('\n')
    pad = 4
    pdf.ln(2)
    x = pdf.get_x()
    y = pdf.get_y()
    h = len(lines) * 5.2 + pad * 2
    pdf.rect(x, y, PW, h, 'FD')
    pdf.set_xy(x + pad, y + pad)
    for line in lines:
        pdf.cell(PW - pad * 2, 5.2, line,
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_x(x + pad)
    pdf.ln(3)

def bullet(items):
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(60, 60, 60)
    for item in items:
        pdf.set_x(18)
        pdf.cell(5, 5.5, chr(149), new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.multi_cell(PW - 5, 5.5, item)
    pdf.ln(1)

def step(num, title, lines):
    pdf.ln(3)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(52, 52, 137)
    pdf.cell(8, 7, f'{num}.', new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(PW - 8, 7, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(80, 80, 80)
    for line in lines:
        pdf.set_x(22)
        pdf.multi_cell(PW - 8, 5.5, line)
    pdf.ln(2)


# Overview
h1('Overview')
body(
    'The template system lets you create new Wordineer tool pages without ever manually '
    'copying the nav, footer, or tool grids. You write tool-specific content in one source '
    'file, update tools.json with the new links, run one Python command, and get a finished '
    'HTML page ready to deploy to Netlify.'
)

# Folder Structure
h1('Folder Structure')
code(
    'template-deploy/\n'
    '  tools.json                   <- edit nav / footer / grid links here\n'
    '  build.py                     <- run this to build all pages\n'
    '  template/\n'
    '    head.html                  <- shared <head> boilerplate\n'
    '    nav.html                   <- shared nav + mega menu\n'
    '    more-tools.html            <- shared tool grids + content wrapper\n'
    '    footer.html                <- shared footer + script tags\n'
    '  tools-src/\n'
    '    random-word-generator.html <- tool-specific content (one file per tool)\n'
    '    your-new-tool.html         <- add new tools here\n'
    '  output/\n'
    '    index.html                 <- finished pages land here'
)

# Steps
h1('How to Add a New Tool (Step by Step)')

step('1', 'Duplicate a tool source file', [
    'Copy tools-src/random-word-generator.html and rename it for your new tool.',
    'Example:  tools-src/random-sentence-generator.html',
])

step('2', 'Update the CONFIG block at the top of the file', [
    'Change "url" and "output" to match the new page:',
    '  "url": "/random-sentence-generator.html"',
    '  "output": "random-sentence-generator.html"',
])

step('3', 'Replace the tool-specific slots with your content', [
    'Each <!-- SLOT:name --> section holds a different piece of the page:',
    '  meta       -> title, description, canonical URL, OG tags, JSON-LD schema',
    '  style      -> CSS unique to this tool\'s widget',
    '  hero       -> the h1 headline and subtitle',
    '  tool       -> the interactive widget HTML',
    '  ad_b       -> the 728x90 leaderboard ad zone (can reuse as-is)',
    '  explainer  -> 300+ words of unique copy about the tool (important for SEO)',
    '  faq        -> FAQ accordion items unique to this tool',
    '  who        -> the "Who uses Wordineer" cards',
    '  init       -> the WORDINEER.init() call + any page-specific JS',
])

step('4', 'Add the tool to tools.json', [
    'Open tools.json and add the new tool to every section where it should appear:',
    '  "mega"            -> shows in the hamburger nav menu',
    '  "more_word_tools" -> shows in the card grid below each tool',
    '  "footer_cols"     -> shows in the footer link columns',
    '  "other_tools"     -> use if it belongs in the Other Tools list',
])

step('5', 'Run the build script', [
    'Open Terminal and run:',
    '  cd "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/template-deploy"',
    '  python3 build.py',
    '',
    'Finished HTML files appear in the output/ folder.',
])

step('6', 'Deploy', [
    'Copy the file(s) from output/ into wordineer-deploy/.',
    'wordineer-deploy/ is the folder Netlify publishes. Never edit it by hand.',
])

# Slot Reference
h1('Slot Reference')
body(
    'Every tools-src file is divided into named slots. The build script reads each slot '
    'and places it in the correct position in the final HTML. You only ever edit the slots '
    'inside your tool source file, never the shared template files.'
)

slots = [
    ('meta',      'title, meta description, canonical URL, Open Graph tags, JSON-LD schema'),
    ('style',     'CSS specific to this tool\'s widget (goes inside <style> in <head>)'),
    ('hero',      'The badge, h1 headline, and subtitle paragraph at the top'),
    ('tool',      'The full interactive widget HTML (filters, word list, saved section)'),
    ('ad_b',      'The 728x90 leaderboard ad zone that appears below the widget'),
    ('explainer', 'Long-form copy explaining the tool (300+ unique words for SEO)'),
    ('faq',       'FAQ accordion items - use unique questions per tool page'),
    ('who',       'The "Who uses Wordineer" use-case cards at the bottom'),
    ('init',      'WORDINEER.init() call with element IDs + any page-specific JS'),
]

COL1 = 36
COL2 = PW - COL1

pdf.set_font('Helvetica', 'B', 10)
pdf.set_text_color(255, 255, 255)
pdf.set_fill_color(52, 52, 137)
pdf.cell(COL1, 7, '  Slot name', border=0, fill=True,
         new_x=XPos.RIGHT, new_y=YPos.TOP)
pdf.cell(COL2, 7, 'What goes here', border=0, fill=True,
         new_x=XPos.LMARGIN, new_y=YPos.NEXT)

alt = False
for name, desc in slots:
    row_fill = (245, 245, 248) if alt else (255, 255, 255)
    pdf.set_fill_color(*row_fill)

    # estimate row height
    lines_needed = max(1, len(desc) // 60 + 1)
    row_h = lines_needed * 6 + 2

    x = pdf.get_x()
    y = pdf.get_y()

    pdf.rect(x, y, COL1, row_h, 'F')
    pdf.rect(x + COL1, y, COL2, row_h, 'F')

    # name
    pdf.set_text_color(52, 52, 137)
    pdf.set_font('Courier', 'B', 9)
    pdf.set_xy(x + 2, y + 2)
    pdf.cell(COL1 - 2, row_h - 2, name, fill=False,
             new_x=XPos.RIGHT, new_y=YPos.TOP)

    # description
    pdf.set_font('Helvetica', '', 9.5)
    pdf.set_text_color(60, 60, 60)
    pdf.set_xy(x + COL1 + 2, y + 2)
    pdf.multi_cell(COL2 - 4, 6, desc, fill=False)

    pdf.set_xy(x, y + row_h)
    alt = not alt

pdf.ln(4)

# Editing shared parts
h1('Editing Shared Parts (Nav, Footer, Tool Grids)')
body(
    'To update the nav, footer, or tool grids across every page at once, '
    'edit tools.json then re-run build.py. You never need to touch '
    'the individual tool source files for this.'
)
bullet([
    'Add or rename a tool in the nav menu  ->  edit the "mega" array in tools.json',
    'Add a tool to the card grid           ->  edit "more_word_tools" in tools.json',
    'Add a tool to the footer columns      ->  edit "footer_cols" in tools.json',
    'Add a category to Other Tools         ->  edit "other_tools" in tools.json',
])

# Quick reference
h1('Run Command (Quick Reference)')
code(
    'cd "/Users/garrickdeetan/Documents/Random Word Generator Tool Site/template-deploy"\n'
    'python3 build.py'
)
body(
    'The output/ folder is safe to delete and rebuild at any time. '
    'It is always regenerated fresh when you run build.py.'
)

out = '/Users/garrickdeetan/Documents/Random Word Generator Tool Site/template-deploy/instructions - new tool deployment.pdf'
pdf.output(out)
print('Saved:', out)
