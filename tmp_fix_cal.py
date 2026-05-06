import os

html_code = """<!DOCTYPE html>
<html lang="en">
<!-- Layout identical tailored for Pariksha -->
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pariksha - Gurukul AI</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=DM+Sans:wght@400;500;700&family=EB+Garamond:wght@400;600;700&display=swap" rel="stylesheet">
    <script>
        tailwind.config = { theme: { extend: { colors: { background: '#0a0804', primary: '#c9963a', accent: '#e8732a', text: '#f0ddb0', success: '#2d7a4f', danger: '#c0392b' }, fontFamily: { cinzel: ['Cinzel', 'serif'], garamond: ['EB Garamond', 'serif'], sans: ['DM Sans', 'sans-serif']} } } }
    </script>
    <style>
        body { background-color: #0a0804; color: #f0ddb0; background-image: radial-gradient(circle at top right, rgba(201, 150, 58, 0.15) 0%, transparent 40%), radial-gradient(circle at bottom left, rgba(232, 115, 42, 0.1) 0%, transparent 50%); background-attachment: fixed; }
        .glass { background: rgba(10, 8, 4, 0.4); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border: 1px solid rgba(201, 150, 58, 0.15); box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37); }
        .calendar-cell { min-height: 80px; position: relative; transition: all 0.2s ease; border-radius: 4px; border: 1px solid rgba(255,255,255,0.05); }
        .calendar-cell:hover { background: rgba(201, 150, 58, 0.1) !important; border-color: rgba(201, 150, 58, 0.3); }
        .has-exam { background: rgba(192, 57, 43, 0.15); border: 1px solid rgba(192, 57, 43, 0.4); box-shadow: inset 0 0 15px rgba(192,57,43,0.1); }
    </style>
</head>
<body class="font-sans antialiased min-h-screen flex selection:bg-primary/30 text-text">
    <aside class="w-64 glass border-r border-t-0 border-b-0 border-l-0 hidden md:flex flex-col sticky top-0 h-screen z-50">
        <div class="p-8"><h1 class="font-cinzel text-3xl font-bold text-primary">GURUKUL</h1></div>
        <nav class="flex-1 px-4 space-y-3 mt-4 text-sm font-sans tracking-wide">
            <a href="gurukul_dashboard.html" class="flex items-center gap-3 px-4 py-3 rounded-lg text-text/70 hover:text-primary transition-all font-medium border-l-2 border-transparent">Dashboard</a>
            <a href="gurukul_vishay.html" class="flex items-center gap-3 px-4 py-3 rounded-lg text-text/70 hover:text-primary transition-all font-medium border-l-2 border-transparent">Vishay</a>
            <a href="#" class="flex items-center gap-3 px-4 py-3 rounded-lg bg-gradient-to-r from-danger/20 to-transparent border-l-2 border-danger text-danger transition-all font-bold">Pariksha</a>
            <a href="gurukul_planner.html" class="flex items-center gap-3 px-4 py-3 rounded-lg text-text/70 hover:text-primary transition-all font-medium border-l-2 border-transparent">Study Planner</a>
        </nav>
        <div class="p-6"><a href="gurukul_ashram.html" class="flex items-center gap-3 px-4 py-3 rounded-lg text-text/70 hover:text-primary hover:bg-primary/10 transition-all font-medium border border-text/10">Ashram</a></div>
    </aside>

    <main class="flex-1 px-8 py-8 overflow-y-auto w-full">
        <header class="flex justify-between items-end mb-10 pb-6 border-b border-danger/20">
            <div>
                <h2 class="font-cinzel text-4xl font-bold tracking-wide text-danger drop-shadow-md">Pariksha Tracking</h2>
                <p class="font-garamond text-primary/80 text-xl mt-2 italic">Prepare for the ultimate trials.</p>
            </div>
            <div class="flex gap-2 bg-black/40 p-2 rounded-xl border border-danger/20">
                <input type="text" id="new-exam-name" placeholder="Exam Name" class="bg-black/60 border border-danger/30 rounded-lg px-3 py-2 text-sm text-text w-40 focus:outline-none focus:border-danger">
                <input type="date" id="new-exam-date" class="bg-black/60 border border-danger/30 rounded-lg px-3 py-2 text-sm text-text/50 focus:outline-none focus:border-danger" title="Simulation Pariksha Date">
                <button class="glass px-5 py-2 rounded-lg text-danger font-bold hover:bg-danger hover:text-white border-danger/30 transition-all shadow-[0_0_10px_rgba(192,57,43,0.2)]" onclick="addExam()">+ Schedule</button>
            </div>
        </header>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
            
            <!-- EXAM LIST PANEL -->
            <div class="lg:col-span-5 flex flex-col gap-6" id="exams-container">
                <!-- Populated via API -->
            </div>

            <!-- EXAM CALENDAR GRID -->
            <div class="lg:col-span-7 glass rounded-2xl p-6">
                <div class="flex justify-between items-center mb-6">
                    <h3 class="font-cinzel text-2xl text-primary font-bold" id="cal-month-title">Month</h3>
                    <div class="flex gap-2">
                        <button class="bg-black/50 border border-primary/20 rounded px-3 py-1 hover:border-primary text-text/70 hover:text-primary" onclick="shiftMonth(-1)">&lt;</button>
                        <button class="bg-black/50 border border-primary/20 rounded px-3 py-1 hover:border-primary text-text/70 hover:text-primary" onclick="shiftMonth(1)">&gt;</button>
                    </div>
                </div>

                <div class="grid grid-cols-7 gap-2 text-center text-xs uppercase tracking-widest font-bold text-text/50 mb-2">
                    <div>Sun</div><div>Mon</div><div>Tue</div><div>Wed</div><div>Thu</div><div>Fri</div><div>Sat</div>
                </div>
                
                <div id="calendar-grid" class="grid grid-cols-7 gap-2">
                    <!-- Populated via JS -->
                </div>
            </div>

        </div>
    </main>

    <script src="/static/js/gurukul_api.js"></script>
    <script>
        let currentExams = [];
        let viewDate = new Date();

        async function loadExams() {
            const container = document.getElementById('exams-container');
            container.innerHTML = '<p class="text-center animate-pulse text-danger">Querying Parikshas...</p>';
            
            try {
                const token = getToken();
                const res = await gurukulFetch('http://127.0.0.1:8000/api/exams/', {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                
                if (!res.ok) throw new Error("Offline");
                currentExams = await res.json();
                
                container.innerHTML = currentExams.map(exam => `
                    <div class="glass flex items-center justify-between p-6 rounded-xl border-l-4 border-b border-t border-r border-danger shadow-[0_0_20px_rgba(192,57,43,0.1)] hover:scale-[1.02] transition-transform">
                        <div>
                            <span class="font-sans text-xs uppercase tracking-widest text-text/50">${exam.subject_name}</span>
                            <h3 class="font-cinzel text-xl font-bold text-white mb-2">${exam.name}</h3>
                            <div class="flex items-center gap-4 text-xs font-sans">
                                <span>Target: <span class="text-primary font-bold">${exam.target_score}%</span></span>
                                <span class="text-danger font-bold">${new Date(exam.exam_date).toLocaleDateString()}</span>
                            </div>
                        </div>
                        <div class="text-center p-3 bg-black/40 rounded-lg min-w-[80px]">
                            <span class="block text-3xl font-bold ${exam.countdown_days < 7 ? 'text-danger animate-pulse' : 'text-primary'}">${exam.countdown_days}</span>
                            <span class="text-[10px] uppercase tracking-widest text-text/60">Days</span>
                        </div>
                    </div>
                `).join('');

                if(currentExams.length === 0) {
                    container.innerHTML = `<div class="glass rounded-xl p-10 text-center"><p class="text-text/70">No Exams Scheduled. Your mind rests.</p></div>`;
                }

                renderCalendar();
            } catch(e) {
                container.innerHTML = `<div class="glass border-danger/50 p-6 text-danger">Connection Error. Is the backend running?</div>`;
            }
        }

        function shiftMonth(offset) {
            viewDate.setMonth(viewDate.getMonth() + offset);
            renderCalendar();
        }

        function renderCalendar() {
            const year = viewDate.getFullYear();
            const month = viewDate.getMonth();
            const firstDay = new Date(year, month, 1).getDay();
            const daysInMonth = new Date(year, month + 1, 0).getDate();
            
            const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
            document.getElementById('cal-month-title').innerText = `${monthNames[month]} ${year}`;

            let html = '';
            
            // Empty slots for start offset
            for(let i = 0; i < firstDay; i++) {
                html += `<div class="calendar-cell bg-white/5 opacity-50"></div>`;
            }

            // Days of the month
            for(let d = 1; d <= daysInMonth; d++) {
                const currentDate = new Date(year, month, d);
                // Force local date string matching by stripping time
                const dateStr = `${year}-${String(month+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
                
                // Find matching exams
                const dayExams = currentExams.filter(ex => ex.exam_date.startsWith(dateStr));
                
                const isToday = new Date().toDateString() === currentDate.toDateString();
                const todayClass = isToday ? 'ring-2 ring-primary bg-primary/10' : 'bg-black/30';
                const examClass = dayExams.length > 0 ? 'has-exam' : '';

                let innerHtml = `<span class="absolute top-1 left-2 text-sm font-bold ${isToday ? 'text-primary' : 'text-text/50'}">${d}</span>`;
                
                if (dayExams.length > 0) {
                    dayExams.forEach(ex => {
                        innerHtml += `<div class="absolute bottom-1 left-1 right-1 bg-danger text-[9px] text-white font-bold px-1 py-0.5 rounded truncate" title="${ex.name}">${ex.name}</div>`;
                    });
                }

                html += `<div class="calendar-cell ${todayClass} ${examClass}">${innerHtml}</div>`;
            }

            document.getElementById('calendar-grid').innerHTML = html;
        }

        async function addExam() {
            const name = document.getElementById('new-exam-name').value;
            const date = document.getElementById('new-exam-date').value;
            if(!name || !date) return alert("Fill in Exam details!");
            try {
                const token = getToken();
                
                const subRes = await gurukulFetch('http://127.0.0.1:8000/api/subjects/', { headers: { 'Authorization': `Bearer ${token}` } });
                const subjects = await subRes.json();
                if(subjects.length === 0) return alert("You must create a Vishay (Subject) first before scheduling an exam!");
                
                const res = await gurukulFetch('http://127.0.0.1:8000/api/exams/', {
                    method: 'POST',
                    headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name: name, exam_date: date, subject: subjects[0].id, target_score: 95 })
                });
                
                if(res.ok) {
                    document.getElementById('new-exam-name').value = '';
                    document.getElementById('new-exam-date').value = '';
                    loadExams(); // Refresh DB dynamically
                }
            } catch(e) { console.error("Error scheduling exam", e); }
        }

        document.addEventListener('DOMContentLoaded', loadExams);
    </script>
</body>
</html>
"""

file_path = r"c:\Users\SOUBHAGYA\Documents\projects\saas\templates\gurukul_pariksha.html"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(html_code)
print("Calendar Fully Rewritten")
