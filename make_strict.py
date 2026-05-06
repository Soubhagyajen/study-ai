import os
import re

TEMPLATE_DIR = r"c:\Users\SOUBHAGYA\Documents\projects\saas\templates"
files = ["gurukul_dashboard.html", "gurukul_vishay.html", "gurukul_pariksha.html", "gurukul_planner.html", "gurukul_ashram.html"]

def enforce_strict_responsiveness(html):
    # 1. Body Flex Fix
    # Original body might just be "flex". On mobile, this shouldn't try to wrap left/right if not needed.
    # Actually, side-nav is fixed on mobile, so "flex" is fine, but forcing overflow-x-hidden prevents breaking.
    html = re.sub(r'<body class="([^"]*)"', r'<body class="\1 overflow-x-hidden flex-col md:flex-row"', html)
    # Deduplicate just in case
    html = html.replace('flex-col md:flex-row overflow-x-hidden flex-col md:flex-row', 'flex-col md:flex-row overflow-x-hidden')
    html = html.replace('flex overflow-x-hidden', 'flex w-full overflow-x-hidden')

    # 2. Main Padding constraints
    html = html.replace('p-8', 'p-4 md:p-8')
    html = html.replace('p-6', 'p-3 md:p-6')
    html = html.replace('gap-8', 'gap-4 md:gap-8')
    html = html.replace('gap-10', 'gap-5 md:gap-10')
    html = html.replace('mb-10', 'mb-5 md:mb-10')
    html = html.replace('mb-8', 'mb-4 md:mb-8')
    html = html.replace('mb-6', 'mb-3 md:mb-6')

    # 3. Card overflow containment
    # Any element with "glass" should not blowout horizontally
    html = html.replace('class="glass', 'class="glass max-w-full break-words')
    html = html.replace('class="grid', 'class="grid max-w-full')

    # 4. Text aggressive scaling
    html = html.replace('text-2xl md:text-4xl', 'text-xl md:text-4xl')
    html = html.replace('text-xl md:text-3xl', 'text-lg md:text-3xl')

    # 5. Pariksha specific Calendar container
    html = html.replace('<div id="calendar-grid"', '<div id="calendar-grid" class="overflow-x-auto min-w-full"')
    html = html.replace('<div class="grid grid-cols-7', '<div class="grid grid-cols-7 min-w-[300px] md:min-w-0')
    
    # 6. Saptah Chart fix
    # Add block level flex-wrap for chart bars
    html = html.replace('chart-bar', 'chart-bar flex-shrink-0')
    
    # 7. Button wrap
    html = html.replace('<div class="flex gap-3">', '<div class="flex flex-wrap gap-2 md:gap-3">')
    html = html.replace('<div class="flex items-center gap-5">', '<div class="flex items-center gap-2 md:gap-5 flex-wrap justify-end">')

    return html

for filename in files:
    full_path = os.path.join(TEMPLATE_DIR, filename)
    if os.path.exists(full_path):
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        modified = enforce_strict_responsiveness(content)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(modified)
        print(f"Strict Tailwind mobile classes applied to {filename}")
