        function updateBudgetView(summary, totalSpent) {
            // 1. Update Top Cards
            const remaining = userBudget - totalSpent;
            const percent = userBudget > 0 ? (totalSpent / userBudget) * 100 : 0;
            
            document.getElementById('budgetTotalDisplay').innerText = `$${userBudget.toLocaleString()}`;
            document.getElementById('budgetSpentDisplay').innerText = `$${totalSpent.toLocaleString()}`;
            document.getElementById('budgetRemaining').innerText = `$${remaining.toLocaleString()}`;
            
            // Progress Bar Color Logic
            const bar = document.getElementById('totalProgressBar');
            bar.style.width = `${Math.min(percent, 100)}%`;
            if(percent > 100) {
                bar.style.background = '#ef4444'; // Red
                document.getElementById('budgetStatusText').innerText = "🚨 OVER BUDGET!";
                document.getElementById('budgetStatusText').style.color = '#fca5a5';
            } else if(percent > 85) {
                bar.style.background = '#f59e0b'; // Orange
                document.getElementById('budgetStatusText').innerText = "⚠️ Approaching limit";
            } else {
                bar.style.background = 'linear-gradient(90deg, #10b981, #3b82f6)';
                document.getElementById('budgetStatusText').innerText = "✅ Healthy spending";
            }

            // 2. Dynamic Categories
            const container = document.getElementById('budgetListContainer');
            container.innerHTML = '';
            
            const categories = ['Food', 'Transport', 'Entertainment', 'Shopping', 'Utilities', 'Uncategorized'];
            // Mock "Suggested Limit" as 20% of total budget per category for demo purposes
            const softLimit = userBudget * 0.2; 

            categories.forEach(cat => {
                const spent = summary[cat] || 0;
                const catPercent = softLimit > 0 ? (spent / softLimit) * 100 : 0;
                const color = catPercent > 100 ? '#ef4444' : (catPercent > 80 ? '#f59e0b' : '#6366f1');
                
                // Only show if there is spending or budget is set
                if(spent > 0 || userBudget > 0) {
                    container.innerHTML += `
                    <div class="budget-item" style="margin-bottom:20px;">
                        <div class="budget-meta">
                            <span style="display:flex; align-items:center; gap:8px;">
                                <div style="width:8px; height:8px; border-radius:50%; background:${color};"></div>
                                ${cat}
                            </span>
                            <span style="color:${color}; font-weight:600;">$${spent.toFixed(0)} <span style="font-weight:400; color:var(--text-muted); font-size:0.8em;">/ $${softLimit.toFixed(0)}</span></span>
                        </div>
                        <div class="budget-bar" style="background:rgba(255,255,255,0.05);">
                            <div class="budget-fill" style="width: ${Math.min(catPercent, 100)}%; background: ${color}; box-shadow: 0 0 10px ${color}66;"></div>
                        </div>
                    </div>
                    `;
                }
            });
        }
