import re

with open("index.html", "r") as f:
    content = f.read()

# 1. Update root CSS variables
content = content.replace("--bg: #020617;", "--bg: #000000;")
content = content.replace("--surface: #0F172A;", "--surface: #1C1C1E;")
content = content.replace("--surface2: #1E293B;", "--surface2: #2C2C2E;")
content = content.replace("--border: #1E293B;", "--border: #2C2C2E;")
content = content.replace("--border2: #334155;", "--border2: #3A3A3C;")

# 2. Update btn-add-record
old_btn_css = """.btn-add-record {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  border: 1px solid var(--a-color);
  background: rgba(212,168,83,0.12);
  color: var(--a-color);
  font-family: 'Noto Sans TC', sans-serif;
  transition: all 0.15s;
  white-space: nowrap;
  flex-shrink: 0;
}
.btn-add-record:hover { background: rgba(212,168,83,0.22); }"""

new_btn_css = """.btn-add-record {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  background: #FFCC00;
  color: #000000;
  font-family: 'Noto Sans TC', sans-serif;
  transition: all 0.15s;
  white-space: nowrap;
  flex-shrink: 0;
}
.btn-add-record:hover { background: #E6B800; }"""
content = content.replace(old_btn_css, new_btn_css)

# 3. Update mobile-nav active
old_mobile_active = """.mobile-nav .nav-item.active { background: transparent; color: var(--text-primary); font-weight: 600; }
.mobile-nav .nav-item.active > svg { stroke: var(--text-primary); stroke-width: 2.5; }
/* active 狀態內的 icon 變黑 */
.mobile-nav .nav-item.active .nav-icon-wrap svg { fill: #000000; stroke: none; }"""

new_mobile_active = """.mobile-nav .nav-item.active { background: #000000; color: #FFCC00; font-weight: 600; border: 1px solid #FFCC00; border-radius: 12px; }
.mobile-nav .nav-item.active > svg { stroke: #FFCC00; stroke-width: 2.5; }
/* active 狀態內的 icon 變黑 */
.mobile-nav .nav-item.active .nav-icon-wrap svg { stroke: #FFCC00; fill: none; }"""
content = content.replace(old_mobile_active, new_mobile_active)

# 4. Pie chart colors
old_pie_colors = """  const colorsA = ['#10B981', 'rgba(16, 185, 129, 0.2)'];
  const colorsB = ['#3B82F6', 'rgba(59, 130, 246, 0.2)'];"""
new_pie_colors = """  const colorsA = ['#FFCC00', 'rgba(255, 204, 0, 0.2)'];
  const colorsB = ['#00C7FF', 'rgba(0, 199, 255, 0.2)'];"""
content = content.replace(old_pie_colors, new_pie_colors)

# Also fix the chart borderWidth
content = content.replace("elements: { arc: { borderWidth: 1, borderColor: '#1E293B' } }", "elements: { arc: { borderWidth: 0 } }")

with open("index.html", "w") as f:
    f.write(content)

print("Done python edits!")
