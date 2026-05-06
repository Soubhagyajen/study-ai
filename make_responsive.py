import os
import re

TEMPLATE_DIR = r"c:\Users\SOUBHAGYA\Documents\projects\saas\templates"
files = ["gurukul_dashboard.html", "gurukul_vishay.html", "gurukul_pariksha.html", "gurukul_planner.html"]

topbar_html = """
    <!-- Mobile Topbar -->
    <div class="md:hidden flex items-center justify-between p-4 glass sticky top-0 z-[60] shadow-md border-b border-primary/20 bg-[#0a0804]">
        <h1 class="font-cinzel text-2xl font-bold text-primary tracking-widest drop-shadow-primary">GURUKUL</h1>
        <button onclick="document.getElementById('mobile-menu').classList.toggle('-translate-x-full')" class="text-primary hover:text-white transition-colors">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
        </button>
    </div>
"""

def update_aside(html):
    # Regex to find <aside ...>
    aside_pattern = re.compile(r'<aside[^>]*>')
    match = aside_pattern.search(html)
    if not match: return html
    
    # We will replace the entire aside class logic
    new_aside = r'''    <aside id="mobile-menu" class="w-64 glass border-r border-t-0 border-b-0 border-l-0 flex flex-col fixed md:sticky top-0 left-0 h-screen z-[100] transform -translate-x-full md:translate-x-0 transition-transform duration-300 bg-[#0a0804] md:bg-transparent shadow-[4px_0_24px_rgba(0,0,0,0.8)] md:shadow-none">
        <!-- Close Button (Mobile Only) -->
        <button onclick="document.getElementById('mobile-menu').classList.add('-translate-x-full')" class="md:hidden absolute top-6 right-6 text-text/50 hover:text-danger z-50">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>'''
    
    html = html[:match.start()] + new_aside + html[match.end():]
    return html

def make_responsive(html):
    original_html = html
    # 1. Inject Topbar after <body>
    if '<body' in html:
        body_end = html.find('>', html.find('<body')) + 1
        # only insert if not already there
        if "id=\"mobile-menu\"" not in html:
            html = html[:body_end] + topbar_html + html[body_end:]

    # 2. Update Aside
    if "id=\"mobile-menu\"" not in original_html:
        html = update_aside(html)
    
    # 3. Main padding padding fix
    html = html.replace('px-8 py-8', 'px-4 md:px-8 py-6 md:py-8')
    # Overflow tracking
    html = html.replace('overflow-y-auto', 'overflow-y-auto overflow-x-hidden')
    
    # 4. Text scaling
    html = html.replace('text-4xl', 'text-2xl md:text-4xl')
    html = html.replace('text-3xl', 'text-xl md:text-3xl')
    
    # 5. Adhyayan Pragati Horizontal Flex wrap to Grid or Flex wrap (Dashboard specific)
    html = html.replace('<div class="flex flex-col md:flex-row gap-10 items-center relative z-10">', 
                        '<div class="flex flex-col xl:flex-row gap-6 md:gap-10 items-center relative z-10 w-full overflow-hidden">')
    
    # 6. Saptah Chart Overflow
    html = html.replace('<div class="h-56 flex items-end', '<div class="h-56 flex items-end overflow-x-auto scrollbar-hide pb-2')
    
    # 7. Chart Bars min-width so they don't crush
    html = html.replace('w-14', 'w-10 md:w-14 flex-shrink-0')
    
    # 8. Ensure grid layouts behave
    html = html.replace('grid-cols-1 lg:grid-cols-12', 'grid-cols-1 lg:grid-cols-12')
    # Make Planner Grid responsive
    html = html.replace('grid-cols-1 lg:grid-cols-2', 'grid-cols-1 lg:grid-cols-2 gap-4 md:gap-8')
    
    # Header flex alignment responsive
    html = html.replace('flex justify-between items-end mb-10 pb-6', 'flex flex-col md:flex-row justify-between items-start md:items-end gap-4 mb-6 md:mb-10 pb-4 md:pb-6')
    # Pariksha Top bar
    html = html.replace('flex gap-2 bg-black/40 p-2', 'flex flex-wrap gap-2 w-full md:w-auto bg-black/40 p-2')
    html = html.replace('w-40', 'w-full md:w-40') # input widths in pariksha

    # Ashram mobile responsiveness
    html = html.replace('max-w-md rounded-2xl p-10', 'max-w-md w-[90%] md:w-full rounded-2xl p-6 md:p-10')

    return html

for filename in files:
    full_path = os.path.join(TEMPLATE_DIR, filename)
    if os.path.exists(full_path):
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        modified = make_responsive(content)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(modified)
        print(f"Responsive styling injected to {filename}")

# Fix Ashram explicitly
ashram_path = os.path.join(TEMPLATE_DIR, "gurukul_ashram.html")
if os.path.exists(ashram_path):
    with open(ashram_path, 'r', encoding='utf-8') as f:
            ashram_html = f.read()
    ashram_html = make_responsive(ashram_html)
    with open(ashram_path, 'w', encoding='utf-8') as f:
            f.write(ashram_html)
    print("Responsive styling injected to gurukul_ashram.html")
