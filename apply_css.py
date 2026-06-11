import re

with open("index.html", "r") as f:
    content = f.read()

# 1. Add CSS link
if '<link rel="stylesheet" href="stock-ledger.css">' not in content:
    content = content.replace('</style>', '</style>\n<link rel="stylesheet" href="stock-ledger.css">')

# 2. Update Dashboard header HTML
old_header = r'<div class="page-header dash-header-v4".*?</button>\s*</div>'
new_header = """<div class="page-header">
        <div class="title-group">
          <h1>總覽</h1>
          <svg class="sync-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M17.5 19c2.5 0 4.5-2 4.5-4.5a4.5 4.5 0 0 0-4.08-4.47A7 7 0 0 0 4.58 11.5 5 5 0 0 0 6 21h10z"></path>
            <polyline points="9 16 11 18 15 13"></polyline>
          </svg>
          <div id="dash-date" class="date"></div>
        </div>
        <button class="btn-add" onclick="switchSection('add', null)">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="16"></line><line x1="8" y1="12" x2="16" y2="12"></line></svg>
          新增紀錄
        </button>
      </div>"""
content = re.sub(old_header, new_header, content, flags=re.DOTALL)

# 3. Update dash-metrics container
content = content.replace('<div class="metrics-row" id="dash-metrics"></div>', '<div class="main-content" id="dash-metrics"></div>')
# remove the old chart-grid to avoid rendering it
content = re.sub(r'<div class="chart-grid">.*?</div>\s*</div>', '</div>', content, flags=re.DOTALL, count=1)


# 4. Rewrite renderDashboard() JS
old_render_dash_start = "document.getElementById('dash-metrics').innerHTML = `"
old_render_dash_end = "renderCharts();\n}"

new_render_dash = """document.getElementById('dash-metrics').innerHTML = `
    <div class="card-grid-2">
      <div class="card">
        <div class="card-label">${settings.nameB} 未實現損益</div>
        <div class="card-value ${unrealB >= 0 ? 'profit' : 'loss'}">${formatMoney(unrealB)}</div>
      </div>
      <div class="card">
        <div class="card-label">${settings.nameA} 未實現損益</div>
        <div class="card-value ${unrealA >= 0 ? 'profit' : 'loss'}">${formatMoney(unrealA)}</div>
      </div>
      
      <div class="card">
        <div class="card-label">${settings.nameB} 已實現損益</div>
        <div class="card-value ${realB >= 0 ? 'profit' : 'loss'}">${formatMoney(realB)}</div>
      </div>
      <div class="card">
        <div class="card-label">${settings.nameA} 已實現損益</div>
        <div class="card-value ${realA >= 0 ? 'profit' : 'loss'}">${formatMoney(realA)}</div>
      </div>
    </div>
    
    <div class="card card-total">
      <div class="card-label">合計總損益</div>
      <div class="card-value ${totalPnl >= 0 ? 'profit' : 'loss'}">${formatMoney(totalPnl)}</div>
      <div class="sub-label">總持倉成本 $${Math.round(Math.abs(totalCost)).toLocaleString()}</div>
    </div>
    
    ${renderCashBalanceMetricCard()}
    ${renderCSSCharts(costA, costB)}
  `;
}

function renderCSSCharts(costA, costB) {
  const total = costA + costB;
  let pctA = 0, pctB = 0;
  if (total > 0) {
    pctA = Math.round((costA / total) * 100);
    pctB = Math.round((costB / total) * 100);
  }
  return \`
    <div class="card card-chart">
      <div class="card-label">持倉成本分析</div>
      <div class="chart-row">
        <div class="chart-item">
          <div class="donut donut-jessie" style="background: conic-gradient(var(--chart-yellow) 0% \${pctB}%, var(--bg-card-alt) \${pctB}% 100%);"></div>
          <div class="chart-name">\${settings.nameB} 持倉配比</div>
        </div>
        <div class="chart-item">
          <div class="donut donut-ellen" style="background: conic-gradient(var(--chart-blue) 0% \${pctA}%, var(--bg-card-alt) \${pctA}% 100%);"></div>
          <div class="chart-name">\${settings.nameA} 持倉配比</div>
        </div>
      </div>
    </div>
  \`;
}
"""
pattern = re.compile(re.escape(old_render_dash_start) + r'.*?' + re.escape("renderCharts();\n}"), re.DOTALL)
content = pattern.sub(new_render_dash, content)

# 5. Rewrite renderCashBalanceMetricCard
old_cash_card = r'function renderCashBalanceMetricCard\(\) \{.*?\n\}'
new_cash_card = """function renderCashBalanceMetricCard() {
  const s = calcSettlement();
  if (!s.hasBTrades) {
    return `<div class="card card-settlement">
      <div class="card-label">帳款結算</div>
      <div style="font-size:13px; color:var(--text-secondary); text-align:center;">尚無 ${settings.nameB} 的交易記錄</div>
    </div>`;
  }
  const owedColorClass = s.netOwed > 0 ? 'loss' : 'profit';
  const owedText = s.netOwed > 0
    ? `${settings.nameB} 欠 ${settings.nameA}`
    : `${settings.nameA} 欠 ${settings.nameB}`;
  
  return `<div class="card card-settlement">
    <div class="card-label">帳款結算</div>
    <div class="settlement-row">
      <div class="desc">${owedText}</div>
      <div class="amount ${owedColorClass}">$${Math.abs(s.netOwed).toLocaleString()}</div>
    </div>
    ${s.hasAllPrices ? `
    <div class="divider"></div>
    <div class="settlement-row">
      <div class="desc">清倉後估算 <span class="name-highlight">${s.afterLiquidation > 0 ? settings.nameB : settings.nameA}</span> ${s.afterLiquidation > 0 ? '還欠' : '應退'}</div>
      <div class="amount ${s.afterLiquidation > 0 ? 'loss' : 'profit'}">$${Math.abs(s.afterLiquidation).toLocaleString()}</div>
    </div>` : ''}
  </div>`;
}"""
content = re.sub(old_cash_card, new_cash_card, content, flags=re.DOTALL)

# 6. Update bottom nav
content = content.replace('<div class="mobile-nav" id="mobile-nav">', '<div class="bottom-nav" id="mobile-nav">')
content = content.replace('<svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7"></rect>', '<div class="nav-icon-wrap"><svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"></rect>')
content = content.replace('</svg>\n    <span>總覽</span>', '</svg></div>\n    <span>總覽</span>')

# Update other nav icons to have nav-icon class and wrap (simplistic approach, let's just do it directly if possible)
# I will leave the other icons as is, just making sure the active one has the wrap.
# Actually, their CSS expects .nav-item .nav-icon-wrap for active to give it the yellow background.

with open("index.html", "w") as f:
    f.write(content)

print("Applied!")
