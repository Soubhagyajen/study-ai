import os

file_path = r"c:\Users\SOUBHAGYA\Documents\projects\saas\templates\gurukul_dashboard.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# We want to replace the script block in dashboard simply by splitting at "<!-- DRF API Integration Engine -->"
if "<!-- DRF API Integration Engine -->" in content:
    html_part = content.split("<!-- DRF API Integration Engine -->")[0]
    
    script_part = """<!-- DRF API Integration Engine -->
    <script>
        document.addEventListener('DOMContentLoaded', async () => {
            const token = getToken();
            if(!token) { window.location.href = 'gurukul_ashram.html'; return; }
            
            await loadDashboardCore();
            await loadSaptahChart();
            await loadSubjectProgress();
            
            setInterval(loadDashboardCore, 60000);
        });

        document.addEventListener('click', async function(e) {
            const link = e.target.closest('a');
            if (link && link.getAttribute('href') && link.getAttribute('href') !== '#') {
                e.preventDefault();
                window.location.href = link.getAttribute('href');
                return;
            }

            const btn = e.target.closest('button');
            if (!btn) return;
            
            const btnText = btn.innerText.trim().toUpperCase();

            if (btnText === 'VIEW ALL') {
                window.location.href = "gurukul_vishay.html";
                return;
            }

            if (btnText === 'TOTAL HOURS') {
                const parent = btn.parentElement;
                parent.children[0].className = "px-3 py-1 rounded bg-primary text-black text-xs font-bold shadow-md";
                parent.children[1].className = "px-3 py-1 rounded text-text/60 hover:text-text text-xs font-bold transition-colors";
                try { await loadSaptahChart(); } catch(e){}
                return;
            }

            if (btnText === 'BY VISHAY') {
                const parent = btn.parentElement;
                parent.children[1].className = "px-3 py-1 rounded bg-primary text-black text-xs font-bold shadow-md";
                parent.children[0].className = "px-3 py-1 rounded text-text/60 hover:text-text text-xs font-bold transition-colors";
                return;
            }

            if (btn.classList.contains('finish-task-btn')) {
                const sessionId = btn.getAttribute('data-session-id');
                btn.innerText = "UPDATING...";
                try {
                    const res = await gurukulFetch(`http://127.0.0.1:8000/api/study-sessions/${sessionId}/`, {
                        method: 'PATCH',
                        body: JSON.stringify({ is_completed: true, end_time: new Date().toISOString() })
                    });
                    if(res.ok) {
                        await loadDashboardCore();
                    } else {
                        btn.innerText = "ERROR";
                    }
                } catch(err) { console.error(err); }
                return;
            }
        });

        async function loadDashboardCore() {
            try {
                const res = await gurukulFetch('http://127.0.0.1:8000/api/dashboard/');
                if(!res.ok) return;
                const data = await res.json();
                
                document.querySelector('h2.tracking-wide').innerText = data.namaste;
                
                const streakEl = document.querySelector('.tracking-tighter.text-accent');
                if(streakEl) streakEl.innerText = data.sadhana_streak || 0;
                
                if(data.upcoming_exams && data.upcoming_exams.length > 0) {
                    const next = data.upcoming_exams[0];
                    document.querySelectorAll('.font-garamond.text-xl')[1].innerText = next.name;
                    document.querySelector('.text-4xl.text-danger').innerText = next.countdown_days;
                } else {
                    document.querySelectorAll('.font-garamond.text-xl')[1].innerText = 'No Active Exams';
                    document.querySelector('.text-4xl.text-danger').innerText = '--';
                }

                renderTaskInteractions(data.today_sessions);
            } catch(e) { }
        }

        function renderTaskInteractions(sessions) {
            if(!sessions) return;
            const listDiv = document.getElementById('aaj-ka-adhyayan-list');
            let html = '';
            let pending = 0;

            sessions.forEach(sess => {
                if(sess.is_completed) {
                    html += `<div class="flex gap-4 items-start p-3 bg-black/30 rounded-lg border border-success/30 opacity-60"><div class="w-6 h-6 mt-0.5 rounded-full bg-success flex items-center justify-center text-black">✓</div><div><h4 class="text-text font-medium line-through">${sess.subject_name}</h4><p class="text-xs text-text/50">Completed • ${sess.duration_minutes} Mins</p></div></div>`;
                } else {
                    pending++;
                    html += `<div class="flex gap-4 items-start p-4 bg-gradient-to-br from-primary/10 to-transparent rounded-lg border border-primary relative overflow-hidden"><button data-session-id="${sess.id}" class="finish-task-btn absolute right-4 top-4 bg-primary/20 hover:bg-primary text-primary hover:text-black transition-colors rounded px-3 py-1 text-xs font-bold uppercase border border-primary/40 z-10">Finish Task</button><div class="absolute left-0 top-0 bottom-0 w-1 bg-primary"></div><div class="w-6 h-6 mt-0.5 rounded-full border-2 border-primary ring-4 ring-primary/20 bg-background flex items-center justify-center"><div class="w-2 h-2 rounded-full bg-primary animate-pulse"></div></div><div class="flex-1"><h4 class="text-text font-bold text-lg pr-24">${sess.subject_name}</h4><p class="text-xs text-primary mt-1 mb-2 font-bold tracking-wider">Estimated: ${sess.duration_minutes} Mins</p></div></div>`;
                }
            });
            listDiv.innerHTML = html || '<p class="text-text/50 text-sm mt-2">No scheduled tasks today.</p>';
            document.querySelector('.bg-primary\\\\/20.text-primary.px-2.rounded').innerText = `${pending} Pending`;
        }

        async function loadSaptahChart() {
            try {
                const res = await gurukulFetch('http://127.0.0.1:8000/api/study-sessions/weekly-stats/');
                if(!res.ok) return;
                const data = await res.json();
                
                const chartContainer = document.querySelector('.h-56.flex.items-end');
                if(!chartContainer || data.length === 0) return;

                const gridLines = chartContainer.innerHTML.match(/<div class="absolute w-full[^>]+><\\/div>|<div class="absolute w-full[^>]+>.*?<\\/div>/g) || [];
                let chartHtml = gridLines.join('');

                const maxMinutes = Math.max(...data.map(d => d.total_minutes), 120); 

                data.forEach(stat => {
                    const heightPercent = Math.min((stat.total_minutes / maxMinutes) * 100, 100);
                    chartHtml += `
                    <div class="w-14 bg-gradient-to-t from-primary/10 to-primary/40 rounded-sm chart-bar border-t border-primary/50 relative group transition-all duration-300 hover:to-primary" 
                         style="height: ${heightPercent}%">
                        <span class="absolute -top-8 left-1/2 -translate-x-1/2 bg-black/80 px-2 py-1 rounded text-xs opacity-0 group-hover:opacity-100 transition-opacity border border-primary/30 z-10 whitespace-nowrap">
                            ${Math.floor(stat.total_minutes/60)}h ${stat.total_minutes%60}m
                        </span>
                    </div>`;
                });
                chartContainer.innerHTML = chartHtml;
            } catch(e) { }
        }

        async function loadSubjectProgress() {
            try {
                const res = await gurukulFetch('http://127.0.0.1:8000/api/subjects/progress/');
                if(!res.ok) return;
                const data = await res.json();
                
                const barsContainer = document.querySelector('.w-full.space-y-6');
                if(!barsContainer || data.length === 0) return;

                let html = '';
                let totalProg = 0;
                const colors = ['bg-accent', 'bg-success', 'bg-primary'];
                const grads = ['from-[#1a100a] to-accent', 'from-[#1d5234] to-success', 'from-[#8a6525] to-primary'];

                data.slice(0, 3).forEach((sub, i) => {
                    totalProg += sub.progress_percentage || 0;
                    html += `
                    <div class="font-sans">
                        <div class="flex justify-between text-sm mb-2 items-end">
                            <div class="flex items-center gap-2">
                                <span class="w-2 h-2 rounded-full ${colors[i%3]} shadow-md"></span>
                                <span class="text-text font-medium tracking-wide">${sub.name}</span>
                            </div>
                            <span class="font-bold text-text">${sub.progress_percentage}%</span>
                        </div>
                        <div class="w-full bg-black/50 rounded-full h-2 border border-white/5 overflow-hidden">
                            <div class="bg-gradient-to-r ${grads[i%3]} h-full rounded-full transition-all duration-700" style="width: ${sub.progress_percentage}%"></div>
                        </div>
                    </div>`;
                });
                
                barsContainer.innerHTML = html;
                const avgProg = Math.round(totalProg / Math.min(3, data.length));
                document.querySelector('.text-4xl.font-cinzel.font-bold').innerText = `${avgProg}%`;
                
                const ring = document.querySelector('circle.drop-shadow-\\\\[0_0_8px_rgba\\\\(232\\\\,115\\\\,42\\\\,0\\\\.8\\\\)\\\\]');
                if(ring) ring.style.strokeDashoffset = 339.29 - (339.29 * (avgProg / 100));
            } catch(e) {}
        }
    </script>
</body>
</html>
"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_part + script_part)
    print("Dashboard Fixed!")
