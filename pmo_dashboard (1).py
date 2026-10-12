import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np

# ------------------------------------------------------------------ data (same plan as the Excel file)
tasks = [  # id, task, phase, duration (working days), % complete at status date
    ("1.1", "Kickoff and charter approval", "Planning", 2, 1.0),
    ("1.2", "Assess current databases", "Planning", 5, 1.0),
    ("1.3", "Prepare migration plan", "Planning", 4, 1.0),
    ("2.1", "Set up new servers", "Setup", 5, 1.0),
    ("2.2", "Install Oracle 21c", "Setup", 3, 1.0),
    ("2.3", "Configure backup and recovery", "Setup", 4, 1.0),
    ("3.1", "Migrate test database", "Migration", 5, 1.0),
    ("3.2", "Validate data integrity", "Migration", 4, 1.0),
    ("3.3", "Migrate user access and roles", "Migration", 3, 1.0),
    ("4.1", "Performance testing", "Testing", 5, 1.0),
    ("4.2", "User acceptance testing (UAT)", "Testing", 5, 0.4),
    ("4.3", "Fix defects and retest", "Testing", 4, 0.0),
    ("5.1", "Go-live cutover", "Go-Live", 2, 0.0),
    ("5.2", "Post go-live monitoring", "Go-Live", 4, 0.0),
    ("6.1", "Handover and documentation", "Handover", 3, 0.0),
    ("6.2", "Project closure and lessons learned", "Handover", 2, 0.0),
]
milestones = [("Plan approved", "1.3"), ("Environment ready", "2.3"), ("UAT sign-off", "4.3"),
              ("Go-live", "5.1"), ("Project closed", "6.2")]
colors = {"Planning": "#1F4E79", "Setup": "#2E75B6", "Migration": "#548235",
          "Testing": "#BF8F00", "Go-Live": "#C00000", "Handover": "#7F7F7F"}
phases = list(colors)

BAC = 25.0                       # budget at completion, INR lakh (assumption: INR 25,00,000)
STATUS_DAY = 43                  # working days elapsed at status date (end of Wednesday, Week 9)
actual_cost = {"Planning": 4.70, "Setup": 5.10, "Migration": 5.05,   # INR lakh spent to date (simulated)
               "Testing": 3.10, "Go-Live": 0.0, "Handover": 0.0}

# ------------------------------------------------------------------ derived metrics
total_days = sum(t[3] for t in tasks)
rate = BAC / total_days                                  # budget per working day (lakh)
starts, day = [], 0
for t in tasks:
    starts.append(day)
    day += t[3]
phase_days = {p: sum(t[3] for t in tasks if t[2] == p) for p in phases}
phase_done = {p: sum(t[3] * t[4] for t in tasks if t[2] == p) for p in phases}
phase_pct = {p: phase_done[p] / phase_days[p] * 100 for p in phases}
phase_budget = {p: phase_days[p] * rate for p in phases}

earned_days = sum(t[3] * t[4] for t in tasks)
progress = earned_days / total_days
EV = earned_days * rate
PV = STATUS_DAY * rate
AC = sum(actual_cost.values())
SPI, CPI = EV / PV, EV / AC
EAC = BAC / CPI
overrun_pct = (EAC / BAC - 1) * 100
ms_done = sum(1 for _, tid in milestones
              if next(t for t in tasks if t[0] == tid)[4] >= 1)


def rag(v):
    return ("#2E9E4F", "GREEN") if v >= 0.95 else (("#E0A800", "AMBER") if v >= 0.85 else ("#C00000", "RED"))


def week_of(day_index):          # 0-based working day -> project week
    return day_index // 5 + 1


# ------------------------------------------------------------------ figure
plt.rcParams["font.family"] = "DejaVu Sans"
NAVY = "#1F3864"
fig = plt.figure(figsize=(16, 9.6), dpi=150, facecolor="white")

# title bar
tb = fig.add_axes([0, 0.915, 1, 0.085]); tb.axis("off")
tb.add_patch(Rectangle((0, 0), 1, 1, color=NAVY))
tb.text(0.02, 0.62, "PMO DASHBOARD  |  Oracle 21c Database Migration & Upgrade Program",
        color="white", fontsize=20, fontweight="bold", va="center")
tb.text(0.02, 0.18, f"Project status as of Week 9 of 12   |   Budget INR {BAC:.0f} lakh   |   "
        f"Tools: Excel, Python (matplotlib)   |   Simulated portfolio project",
        color="#D9E2F3", fontsize=10.5, va="center")
sc, st = rag(min(SPI, CPI))
tb.add_patch(FancyBboxPatch((0.865, 0.2), 0.115, 0.6, boxstyle="round,pad=0.005,rounding_size=0.01",
                            color=sc, transform=tb.transAxes))
tb.text(0.9225, 0.5, f"OVERALL: {st}", color="white", fontsize=12, fontweight="bold", ha="center", va="center")

# KPI cards
cards = [
    ("OVERALL PROGRESS", f"{progress * 100:.0f}%", f"{earned_days:.0f} of {total_days} working days", NAVY),
    ("BUDGET USED", f"INR {AC:.2f}L", f"{AC / BAC * 100:.0f}% of INR {BAC:.0f}L budget", NAVY),
    ("SCHEDULE INDEX (SPI)", f"{SPI:.2f}", f"{rag(SPI)[1]}  |  EV / PV", rag(SPI)[0]),
    ("COST INDEX (CPI)", f"{CPI:.2f}", f"{rag(CPI)[1]}  |  EV / AC", rag(CPI)[0]),
    ("MILESTONES ACHIEVED", f"{ms_done} of {len(milestones)}", "Next: UAT sign-off", NAVY),
]
cw, gap, x0 = 0.18, 0.0125, 0.0125
for i, (lab, val, sub, col) in enumerate(cards):
    ax = fig.add_axes([x0 + i * (cw + gap), 0.775, cw, 0.115]); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0,rounding_size=0.06",
                                facecolor="#F2F5FA", edgecolor="#C9D3E6", transform=ax.transAxes))
    ax.add_patch(Rectangle((0, 0.05), 0.022, 0.9, color=col, transform=ax.transAxes))
    ax.text(0.07, 0.80, lab, fontsize=9, color="#595959", fontweight="bold", va="center")
    ax.text(0.07, 0.46, val, fontsize=22, color=col, fontweight="bold", va="center")
    ax.text(0.07, 0.14, sub, fontsize=8.5, color="#595959", va="center")

# ---- Gantt
ga = fig.add_axes([0.20, 0.335, 0.38, 0.40])
n = len(tasks)
for i, (tid, name, ph, d, pc) in enumerate(tasks):
    y = n - 1 - i
    ga.barh(y, d, left=starts[i], color=colors[ph], alpha=0.30, height=0.62, edgecolor="none")
    if pc > 0:
        ga.barh(y, d * pc, left=starts[i], color=colors[ph], height=0.62, edgecolor="none")
    for mname, mid in milestones:
        if mid == tid:
            ga.plot(starts[i] + d, y, marker="D", color="black", markersize=5.5, zorder=5)
ga.set_yticks(range(n))
ga.set_yticklabels([f"{t[0]}  {t[1]}" for t in tasks][::-1], fontsize=8)
ga.set_xlim(0, total_days)
wk_ticks = np.arange(0, total_days + 1, 5)
ga.set_xticks(wk_ticks[:-1] + 2.5)
ga.set_xticklabels([f"W{k + 1}" for k in range(len(wk_ticks) - 1)], fontsize=8)
for x in wk_ticks:
    ga.axvline(x, color="#E3E3E3", lw=0.6, zorder=0)
ga.axvline(STATUS_DAY, color="#C00000", lw=1.6, ls="--", zorder=6)
ga.text(STATUS_DAY, n - 0.35, " Status\n date", color="#C00000", fontsize=7.5, fontweight="bold", va="bottom")
ga.set_ylim(-0.6, n + 0.9)
ga.tick_params(length=0)
for s in ("top", "right", "left"):
    ga.spines[s].set_visible(False)
ga.set_title("Project Schedule (Gantt): solid = completed work, diamond = milestone",
             fontsize=11, fontweight="bold", color=NAVY, loc="left", x=-0.50)
# phase legend
for i, p in enumerate(phases):
    ga.add_patch(Rectangle((0.0 + i * 0.165, -0.13), 0.02, 0.025, color=colors[p], transform=ga.transAxes,
                           clip_on=False))
    ga.text(0.025 + i * 0.165, -0.1175, p, fontsize=7.5, transform=ga.transAxes, va="center")

# ---- Progress by phase
pa = fig.add_axes([0.70, 0.545, 0.27, 0.19])
vals = [phase_pct[p] for p in phases][::-1]
ps = phases[::-1]
pa.barh(ps, [100] * len(ps), color="#ECECEC", height=0.62)
pa.barh(ps, vals, color=[colors[p] for p in ps], height=0.62)
for y, v in enumerate(vals):
    pa.text(min(v, 100) + 2, y, f"{v:.0f}%", va="center", fontsize=8.5, fontweight="bold")
pa.set_xlim(0, 112)
pa.set_xticks([])
pa.tick_params(axis="y", labelsize=8.5, length=0)
for s in pa.spines.values():
    s.set_visible(False)
pa.set_title("% Complete by Phase", fontsize=11, fontweight="bold", color=NAVY, loc="left")

# ---- Budget by phase
ba = fig.add_axes([0.70, 0.345, 0.27, 0.15])
x = np.arange(len(phases))
bw = 0.38
ba.bar(x - bw / 2, [phase_budget[p] for p in phases], bw, color="#BFC9DA", label="Planned budget")
ba.bar(x + bw / 2, [actual_cost[p] for p in phases], bw, color=NAVY, label="Actual spend to date")
ba.set_xticks(x)
ba.set_xticklabels(phases, fontsize=7.5)
ba.tick_params(axis="y", labelsize=8, length=0)
ba.tick_params(axis="x", length=0)
ba.set_ylabel("INR lakh", fontsize=8)
for s in ("top", "right"):
    ba.spines[s].set_visible(False)
ba.legend(fontsize=7.5, frameon=False, loc="upper right", ncol=1)
ba.set_ylim(0, max(phase_budget.values()) * 1.45)
ba.set_title("Budget vs Actual Spend by Phase", fontsize=11, fontweight="bold", color=NAVY, loc="left")

# ---- Milestone table
ma = fig.add_axes([0.02, 0.045, 0.46, 0.21]); ma.axis("off")
ma.text(0, 1.0, "Milestone Tracker", fontsize=11, fontweight="bold", color=NAVY, va="top")
cols_x = [0.0, 0.27, 0.63, 0.82]
heads = ["Milestone", "Linked task", "Target", "Status"]
y0 = 0.76
for cx, h in zip(cols_x, heads):
    ma.text(cx + 0.01, y0, h, fontsize=8.5, fontweight="bold", color="white", va="center")
ma.add_patch(Rectangle((0, y0 - 0.065), 1, 0.13, color=NAVY, zorder=0))
for i, (mname, tid) in enumerate(milestones):
    ti = next(k for k, t in enumerate(tasks) if t[0] == tid)
    t = tasks[ti]
    end_week = week_of(starts[ti] + t[3] - 1)
    done = t[4] >= 1
    yy = y0 - 0.14 * (i + 1)
    if i % 2 == 0:
        ma.add_patch(Rectangle((0, yy - 0.065), 1, 0.13, color="#F2F5FA", zorder=0))
    ma.text(cols_x[0] + 0.01, yy, mname, fontsize=8.5, va="center", fontweight="bold")
    ma.text(cols_x[1] + 0.01, yy, f"{tid} {t[1]}", fontsize=8, va="center")
    ma.text(cols_x[2] + 0.01, yy, f"Week {end_week}", fontsize=8.5, va="center")
    ma.text(cols_x[3] + 0.01, yy, "Achieved" if done else "Pending", fontsize=8.5, va="center",
            fontweight="bold", color="#2E9E4F" if done else "#7F7F7F")
ma.set_xlim(0, 1)
ma.set_ylim(0, 1)

# ---- Key insights
ia = fig.add_axes([0.51, 0.045, 0.47, 0.21]); ia.axis("off")
ia.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0,rounding_size=0.03",
                            facecolor="#F2F5FA", edgecolor="#C9D3E6", transform=ia.transAxes))
ia.text(0.03, 0.88, "Key Insights & Actions", fontsize=11, fontweight="bold", color=NAVY, va="center")
behind = (PV - EV) / rate
insights = [
    f"Project is {progress * 100:.0f}% complete, about {behind:.0f} working day behind plan (SPI {SPI:.2f}).",
    f"Spend is INR {AC:.2f}L of {BAC:.0f}L ({AC / BAC * 100:.0f}%); CPI {CPI:.2f} forecasts INR {EAC:.1f}L at "
    f"completion ({overrun_pct:+.1f}%), inside the 5% budget limit.",
    f"UAT is {tasks[10][4] * 100:.0f}% complete. Every task is on the critical path, so any UAT slip moves Go-live.",
    "Action: confirm test-team availability for UAT and track Testing-phase cost weekly.",
]
import textwrap
ypos = 0.72
for line in insights:
    wrapped = textwrap.wrap(line, 88)
    ia.text(0.03, ypos, "\u2022", fontsize=11, color=NAVY, va="top")
    ia.text(0.055, ypos, "\n".join(wrapped), fontsize=8.8, va="top", linespacing=1.25)
    ypos -= 0.085 + 0.095 * len(wrapped)
ia.set_xlim(0, 1)
ia.set_ylim(0, 1)

fig.text(0.5, 0.008, "Simulated project built for portfolio purposes. Figures are illustrative. "
         "SPI = EV/PV, CPI = EV/AC, EAC = Budget/CPI.", fontsize=7.5, color="#7F7F7F", ha="center")

fig.savefig("PMO_Dashboard.png", dpi=150, facecolor="white")
print("progress", progress, "SPI", SPI, "CPI", CPI, "EAC", EAC, "AC", AC, "EV", EV, "PV", PV, "ms", ms_done)
print({p: round(phase_pct[p]) for p in phases}, {p: round(phase_budget[p], 2) for p in phases})
