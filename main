import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from dataclasses import dataclass, field
from typing import List

st.set_page_config(
    page_title="FacilityOS",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── GLOBAL CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=Outfit:wght@300;400;500;600;700&display=swap');

/* ── RESET / BASE ── */
html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif !important;
    background-color: #0a0c10 !important;
    color: #e8eaf0 !important;
}

/* Remove Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* Main block padding */
.block-container {
    padding: 28px 36px 60px !important;
    max-width: 1400px !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #111318 !important;
    border-right: 1px solid rgba(255,255,255,0.07) !important;
}
[data-testid="stSidebar"] * { color: #9ca3af !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #e8eaf0 !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #181b22 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #e8eaf0 !important;
    border-radius: 10px !important;
}
[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    background: #181b22 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #9ca3af !important;
    border-radius: 10px !important;
    font-size: 13px !important;
    padding: 8px 16px !important;
    transition: all 0.2s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    border-color: #00e5a0 !important;
    color: #00e5a0 !important;
}

/* ── METRICS ── */
[data-testid="metric-container"] {
    background: #111318 !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 14px !important;
    padding: 20px !important;
    transition: all 0.2s !important;
}
[data-testid="metric-container"]:hover {
    border-color: rgba(255,255,255,0.14) !important;
    transform: translateY(-2px);
}
[data-testid="stMetricLabel"] { color: #6b7280 !important; font-size: 11px !important; font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: 0.08em !important; }
[data-testid="stMetricValue"] { color: #e8eaf0 !important; font-family: 'DM Serif Display', serif !important; font-size: 36px !important; }
[data-testid="stMetricDelta"] { color: #00e5a0 !important; font-size: 12px !important; }

/* ── TABS ── */
[data-testid="stTabs"] [role="tablist"] {
    background: #111318 !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    padding: 4px !important;
    gap: 2px !important;
}
[data-testid="stTabs"] [role="tab"] {
    border-radius: 9px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #6b7280 !important;
    padding: 7px 16px !important;
    border: none !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: #181b22 !important;
    color: #00e5a0 !important;
    border: 1px solid rgba(0,229,160,0.2) !important;
}
[data-testid="stTabs"] [role="tabpanel"] {
    padding-top: 20px !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}
.dvn-scroller { background: #111318 !important; }

/* ── FORMS / INPUTS ── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stDateInput"] input {
    background: #181b22 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #e8eaf0 !important;
    font-family: 'Outfit', sans-serif !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: #00e5a0 !important;
    box-shadow: 0 0 0 2px rgba(0,229,160,0.1) !important;
}
[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiSelect"] > div > div {
    background: #181b22 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #e8eaf0 !important;
}
label { color: #9ca3af !important; font-size: 12px !important; font-weight: 500 !important; }

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #00e5a0, #00c485) !important;
    border: none !important;
    border-radius: 10px !important;
    color: #0a0c10 !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    padding: 10px 22px !important;
    transition: all 0.2s !important;
    font-family: 'Outfit', sans-serif !important;
}
.stButton > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 20px rgba(0,229,160,0.25) !important;
}

/* Form submit */
[data-testid="stForm"] .stButton > button {
    margin-top: 8px;
}

/* ── EXPANDER ── */
[data-testid="stExpander"] {
    background: #111318 !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
}
[data-testid="stExpander"] summary {
    color: #9ca3af !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}
[data-testid="stExpander"] summary:hover { color: #e8eaf0 !important; }

/* ── ALERTS ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    border-left: 3px solid !important;
    background: rgba(255,255,255,0.03) !important;
}
.stSuccess { border-color: #00e5a0 !important; color: #00e5a0 !important; }
.stError   { border-color: #ef4444 !important; color: #f87171 !important; }
.stWarning { border-color: #f59e0b !important; color: #f59e0b !important; }
.stInfo    { border-color: #3b82f6 !important; color: #60a5fa !important; }

/* ── PLOTLY CHARTS ── */
.js-plotly-plot { border-radius: 12px !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.08); border-radius: 10px; }

/* ── MULTISELECT TAGS ── */
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
    background: rgba(0,229,160,0.1) !important;
    color: #00e5a0 !important;
    border-radius: 6px !important;
}

/* ── DATE INPUT ── */
[data-testid="stDateInput"] > div { border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)


# ── DATA MODELS ─────────────────────────────────────────────────────────────
@dataclass
class Asset:
    id: str; name: str; type: str; location: str; status: str
    purchase_date: str; last_maintenance: str; next_maintenance: str
    manufacturer: str; model: str; serial_number: str
    warranty_expiry: str; notes: str = ""

@dataclass
class WorkOrder:
    id: str; title: str; description: str; asset_id: str
    priority: str; status: str; created_date: str; due_date: str
    assigned_to: str; estimated_hours: float
    actual_hours: float = 0; cost: float = 0; notes: str = ""

@dataclass
class Staff:
    id: str; name: str; role: str; department: str
    email: str; phone: str; skills: List[str]
    availability: str; hourly_rate: float

@dataclass
class Inventory:
    id: str; name: str; category: str; quantity: int
    unit: str; reorder_level: int; supplier: str
    unit_cost: float; location: str; last_ordered: str


# ── SAMPLE DATA ─────────────────────────────────────────────────────────────
def load_assets():
    return [
        Asset("AST001","HVAC System – Building A","HVAC","Building A, Floor 1","Operational","2022-01-15","2024-01-15","2024-04-15","Carrier","XRS-2000","HV2022001","2025-01-15"),
        Asset("AST002","Elevator – Main Lobby","Elevator","Building A, Lobby","Maintenance Required","2021-06-20","2024-02-01","2024-03-01","Otis","Elev-500","EL2021005","2024-06-20","Strange noise during operation"),
        Asset("AST003","Generator – Backup","Electrical","Building B, Basement","Operational","2023-03-10","2024-02-10","2024-05-10","Kohler","GEN-1000","GN2023010","2026-03-10"),
        Asset("AST004","Fire Suppression System","Fire Safety","Building A, All Floors","Operational","2022-09-01","2024-01-20","2024-07-20","Kidde","FS-Pro","FS2022009","2025-09-01"),
        Asset("AST005","Chiller Unit – Roof","HVAC","Building A, Rooftop","Out of Service","2020-04-15","2023-12-01","2024-02-01","Trane","CH-800","TR2020004","2023-04-15","Compressor failure – awaiting parts"),
    ]

def load_work_orders():
    return [
        WorkOrder("WO001","HVAC Filter Replacement","Replace air filters in Building A","AST001","Medium","In Progress","2024-02-15","2024-02-20","John Smith",2,1.5,150),
        WorkOrder("WO002","Elevator Emergency Maintenance","Emergency maintenance – strange noise","AST002","High","Open","2024-02-18","2024-02-19","Mike Johnson",4,0,0,"Strange noise during operation"),
        WorkOrder("WO003","Generator Monthly Test","Monthly generator test run","AST003","Low","Completed","2024-02-10","2024-02-11","Sarah Williams",1,0.8,80),
        WorkOrder("WO004","Chiller Compressor Repair","Replace failed compressor","AST005","High","Open","2024-02-12","2024-02-25","Mike Johnson",16,0,0,"Awaiting parts from Trane"),
        WorkOrder("WO005","Fire System Inspection","Annual fire suppression inspection","AST004","Medium","Completed","2024-02-05","2024-02-08","Sarah Williams",3,3.2,200),
    ]

def load_staff():
    return [
        Staff("STF001","John Smith","Maintenance Technician","HVAC","john.smith@facility.com","555-0101",["HVAC","Electrical","Plumbing"],"Available",35),
        Staff("STF002","Mike Johnson","Senior Technician","Elevators","mike.johnson@facility.com","555-0102",["Elevators","Mechanical","Hydraulics"],"Busy",45),
        Staff("STF003","Sarah Williams","Technician","Electrical","sarah.williams@facility.com","555-0103",["Electrical","Generators","BMS"],"Available",38),
        Staff("STF004","Carlos Reyes","Plumber","Plumbing","carlos.reyes@facility.com","555-0104",["Plumbing","HVAC"],"Off",32),
    ]

def load_inventory():
    return [
        Inventory("INV001","Air Filters 20x20x1","HVAC",50,"pcs",20,"HVAC Supply Co",15.50,"Warehouse A – Shelf 3","2024-02-01"),
        Inventory("INV002","LED Bulbs 60W Equivalent","Electrical",200,"pcs",50,"Lighting World",4.25,"Warehouse B – Shelf 1","2024-02-15"),
        Inventory("INV003","Elevator Lubricant","Elevator",12,"gallons",10,"Elevator Parts Inc",45.00,"Warehouse A – Shelf 5","2024-01-20"),
        Inventory("INV004","HVAC Refrigerant R-410A","HVAC",8,"lbs",15,"CoolTech Supply",28.00,"Warehouse A – Shelf 2","2024-01-10"),
        Inventory("INV005","Circuit Breakers 20A","Electrical",35,"pcs",10,"Electrical Depot",12.75,"Warehouse B – Shelf 4","2024-02-10"),
    ]


# ── SESSION STATE ────────────────────────────────────────────────────────────
def init():
    if 'assets'      not in st.session_state: st.session_state.assets      = load_assets()
    if 'work_orders' not in st.session_state: st.session_state.work_orders = load_work_orders()
    if 'staff'       not in st.session_state: st.session_state.staff       = load_staff()
    if 'inventory'   not in st.session_state: st.session_state.inventory   = load_inventory()
    if 'notifs'      not in st.session_state: st.session_state.notifs      = []

def add_notif(msg, t="info"):
    st.session_state.notifs.insert(0, {"msg": msg, "type": t, "ts": datetime.now().strftime("%H:%M")})
    st.session_state.notifs = st.session_state.notifs[:10]


# ── HELPERS ─────────────────────────────────────────────────────────────────
def maintenance_alerts():
    alerts = []
    today = datetime.now().date()
    for a in st.session_state.assets:
        d = datetime.strptime(a.next_maintenance, "%Y-%m-%d").date()
        diff = (d - today).days
        if diff < 0:   alerts.append(("🔴", f"OVERDUE: {a.name}", f"{abs(diff)} days past due", "error"))
        elif diff <= 7: alerts.append(("🟡", f"URGENT: {a.name}", f"Due in {diff} days", "warning"))
        elif diff <= 30: alerts.append(("🔵", f"UPCOMING: {a.name}", f"Due in {diff} days", "info"))
    return alerts

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Outfit", color="#9ca3af", size=12),
    margin=dict(t=40, b=20, l=10, r=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(255,255,255,0.08)"),
)
COLORS = ["#00e5a0", "#3b82f6", "#f59e0b", "#ef4444", "#a855f7", "#14b8a6"]


def section_header(eyebrow, title, subtitle=""):
    st.markdown(f"""
    <div style="margin-bottom:24px">
      <div style="font-size:11px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;
                  color:#00e5a0;font-family:'DM Mono',monospace;margin-bottom:4px">{eyebrow}</div>
      <div style="font-family:'DM Serif Display',serif;font-size:28px;letter-spacing:-.4px;
                  color:#e8eaf0;line-height:1.2">{title}</div>
      {"<div style='font-size:13px;color:#6b7280;margin-top:6px'>"+subtitle+"</div>" if subtitle else ""}
    </div>""", unsafe_allow_html=True)


def priority_badge(p):
    colors = {"High": ("#ef4444","rgba(239,68,68,.12)"), "Medium": ("#f59e0b","rgba(245,158,11,.12)"), "Low": ("#00e5a0","rgba(0,229,160,.1)")}
    c, bg = colors.get(p, ("#9ca3af","rgba(255,255,255,.05)"))
    return f'<span style="background:{bg};color:{c};border-radius:20px;padding:3px 10px;font-size:11px;font-family:\'DM Mono\',monospace;font-weight:600">● {p}</span>'

def status_badge(s):
    colors = {"Open": ("#60a5fa","rgba(59,130,246,.12)"), "In Progress": ("#f59e0b","rgba(245,158,11,.12)"),
              "Completed": ("#00e5a0","rgba(0,229,160,.1)"), "Cancelled": ("#6b7280","rgba(255,255,255,.05)")}
    c, bg = colors.get(s, ("#9ca3af","rgba(255,255,255,.05)"))
    return f'<span style="background:{bg};color:{c};border-radius:20px;padding:3px 10px;font-size:11px;font-family:\'DM Mono\',monospace;font-weight:600">{s}</span>'

def avail_badge(a):
    if a == "Available": return '<span style="background:rgba(0,229,160,.1);color:#00e5a0;border-radius:20px;padding:2px 10px;font-size:11px;font-family:\'DM Mono\',monospace">● Available</span>'
    if a == "Busy":      return '<span style="background:rgba(245,158,11,.1);color:#f59e0b;border-radius:20px;padding:2px 10px;font-size:11px;font-family:\'DM Mono\',monospace">● Busy</span>'
    return '<span style="background:rgba(255,255,255,.05);color:#6b7280;border-radius:20px;padding:2px 10px;font-size:11px;font-family:\'DM Mono\',monospace">● Off</span>'


# ── PAGES ────────────────────────────────────────────────────────────────────

def page_dashboard():
    section_header("Overview", "Facility Dashboard", "Real-time visibility across assets, work orders, staff & inventory.")

    # Metrics
    open_wo    = sum(1 for w in st.session_state.work_orders if w.status in ("Open","In Progress"))
    avail_staff = sum(1 for s in st.session_state.staff if s.availability == "Available")
    low_inv    = sum(1 for i in st.session_state.inventory if i.quantity <= i.reorder_level)
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Assets",     len(st.session_state.assets),     "Tracked")
    c2.metric("Open Work Orders", open_wo,                          "Require attention")
    c3.metric("Available Staff",  avail_staff,                      f"of {len(st.session_state.staff)} total")
    c4.metric("Low Inventory",    low_inv,                          "Need reorder")

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # Alerts
    alerts = maintenance_alerts()
    if alerts:
        st.markdown('<div style="font-size:13px;font-weight:600;color:#9ca3af;text-transform:uppercase;letter-spacing:.08em;margin-bottom:10px">⚠️ Maintenance Alerts</div>', unsafe_allow_html=True)
        for icon, title, sub, atype in alerts:
            if atype == "error":   st.error(f"{icon} **{title}** — {sub}")
            elif atype == "warning": st.warning(f"{icon} **{title}** — {sub}")
            else:                  st.info(f"{icon} **{title}** — {sub}")
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown('<div style="font-size:13px;font-weight:600;color:#e8eaf0;margin-bottom:12px">📋 Recent Work Orders</div>', unsafe_allow_html=True)
        rows = []
        for wo in sorted(st.session_state.work_orders, key=lambda x: x.created_date, reverse=True)[:5]:
            rows.append(f"""
            <tr>
              <td style="padding:11px 14px;font-family:'DM Mono',monospace;font-size:11px;color:#6b7280;border-bottom:1px solid rgba(255,255,255,.05)">{wo.id}</td>
              <td style="padding:11px 14px;font-size:13px;color:#e8eaf0;font-weight:500;border-bottom:1px solid rgba(255,255,255,.05)">{wo.title}</td>
              <td style="padding:11px 14px;border-bottom:1px solid rgba(255,255,255,.05)">{priority_badge(wo.priority)}</td>
              <td style="padding:11px 14px;border-bottom:1px solid rgba(255,255,255,.05)">{status_badge(wo.status)}</td>
              <td style="padding:11px 14px;font-size:12px;color:#6b7280;border-bottom:1px solid rgba(255,255,255,.05)">{wo.assigned_to.split()[0]}</td>
            </tr>""")
        st.markdown(f"""
        <div style="background:#111318;border:1px solid rgba(255,255,255,.07);border-radius:14px;overflow:hidden">
          <table style="width:100%;border-collapse:collapse">
            <thead>
              <tr style="background:rgba(255,255,255,.02)">
                <th style="padding:10px 14px;font-size:10px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#6b7280;text-align:left">ID</th>
                <th style="padding:10px 14px;font-size:10px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#6b7280;text-align:left">Title</th>
                <th style="padding:10px 14px;font-size:10px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#6b7280;text-align:left">Priority</th>
                <th style="padding:10px 14px;font-size:10px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#6b7280;text-align:left">Status</th>
                <th style="padding:10px 14px;font-size:10px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#6b7280;text-align:left">Assigned</th>
              </tr>
            </thead>
            <tbody>{''.join(rows)}</tbody>
          </table>
        </div>""", unsafe_allow_html=True)

    with col_right:
        st.markdown('<div style="font-size:13px;font-weight:600;color:#e8eaf0;margin-bottom:12px">📦 Inventory Levels</div>', unsafe_allow_html=True)
        inv_html = '<div style="background:#111318;border:1px solid rgba(255,255,255,.07);border-radius:14px;padding:16px 20px">'
        for item in st.session_state.inventory:
            pct = min(100, int(item.quantity / max(item.reorder_level*2, 1) * 100))
            color = "#00e5a0" if pct > 60 else ("#f59e0b" if pct > 30 else "#ef4444")
            inv_html += f"""
            <div style="margin-bottom:14px">
              <div style="display:flex;justify-content:space-between;margin-bottom:5px">
                <span style="font-size:12px;color:#e8eaf0;font-weight:500">{item.name[:28]}</span>
                <span style="font-size:11px;font-family:'DM Mono',monospace;color:#6b7280">{item.quantity} {item.unit}</span>
              </div>
              <div style="height:4px;background:rgba(255,255,255,.06);border-radius:4px;overflow:hidden">
                <div style="height:100%;width:{pct}%;background:{color};border-radius:4px"></div>
              </div>
            </div>"""
        inv_html += '</div>'
        st.markdown(inv_html, unsafe_allow_html=True)

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        st.markdown('<div style="font-size:13px;font-weight:600;color:#e8eaf0;margin-bottom:12px">👥 Staff Availability</div>', unsafe_allow_html=True)
        staff_html = '<div style="background:#111318;border:1px solid rgba(255,255,255,.07);border-radius:14px;padding:10px 20px">'
        initials_colors = {"John Smith":"#059669","Mike Johnson":"#b45309","Sarah Williams":"#1d4ed8","Carlos Reyes":"#7c3aed"}
        for s in st.session_state.staff:
            ic = initials_colors.get(s.name,"#374151")
            ini = "".join([n[0] for n in s.name.split()][:2])
            staff_html += f"""
            <div style="display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,.05)">
              <div style="width:36px;height:36px;border-radius:50%;background:{ic};display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:#fff;flex-shrink:0">{ini}</div>
              <div style="flex:1">
                <div style="font-size:13px;color:#e8eaf0;font-weight:500">{s.name}</div>
                <div style="font-size:11px;color:#6b7280;margin-top:1px">{s.role} · ${s.hourly_rate}/hr</div>
              </div>
              {avail_badge(s.availability)}
            </div>"""
        staff_html = staff_html.rstrip('<div') + '</div>'  # close last border but keep simplicity
        staff_html += '</div>'
        st.markdown(staff_html, unsafe_allow_html=True)


def page_assets():
    section_header("Assets", "Asset Management", "Track, maintain, and analyse all facility equipment.")
    tab1, tab2, tab3 = st.tabs(["📋  Asset Registry", "➕  Add New Asset", "📊  Analytics"])

    with tab1:
        c1, c2 = st.columns(2)
        status_f = c1.multiselect("Filter by Status", ["Operational","Maintenance Required","Out of Service","Retired"])
        type_f   = c2.multiselect("Filter by Type",   ["HVAC","Elevator","Electrical","Plumbing","Fire Safety"])

        assets = st.session_state.assets
        if status_f: assets = [a for a in assets if a.status in status_f]
        if type_f:   assets = [a for a in assets if a.type in type_f]

        rows = []
        for a in assets:
            sc = {"Operational":"#00e5a0","Maintenance Required":"#f59e0b","Out of Service":"#ef4444","Retired":"#6b7280"}.get(a.status,"#9ca3af")
            sbg = {"Operational":"rgba(0,229,160,.1)","Maintenance Required":"rgba(245,158,11,.1)","Out of Service":"rgba(239,68,68,.1)","Retired":"rgba(255,255,255,.05)"}.get(a.status,"rgba(255,255,255,.05)")
            rows.append(f"""
            <tr>
              <td style="padding:12px 14px;font-family:'DM Mono',monospace;font-size:11px;color:#6b7280;border-bottom:1px solid rgba(255,255,255,.04)">{a.id}</td>
              <td style="padding:12px 14px;font-size:13px;color:#e8eaf0;font-weight:500;border-bottom:1px solid rgba(255,255,255,.04)">{a.name}</td>
              <td style="padding:12px 14px;font-size:12px;color:#9ca3af;border-bottom:1px solid rgba(255,255,255,.04)">{a.type}</td>
              <td style="padding:12px 14px;font-size:12px;color:#6b7280;border-bottom:1px solid rgba(255,255,255,.04)">{a.location}</td>
              <td style="padding:12px 14px;border-bottom:1px solid rgba(255,255,255,.04)"><span style="background:{sbg};color:{sc};border-radius:20px;padding:3px 10px;font-size:11px;font-family:'DM Mono',monospace">{a.status}</span></td>
              <td style="padding:12px 14px;font-size:12px;font-family:'DM Mono',monospace;color:#6b7280;border-bottom:1px solid rgba(255,255,255,.04)">{a.last_maintenance}</td>
              <td style="padding:12px 14px;font-size:12px;font-family:'DM Mono',monospace;color:#9ca3af;border-bottom:1px solid rgba(255,255,255,.04)">{a.next_maintenance}</td>
            </tr>""")

        st.markdown(f"""
        <div style="background:#111318;border:1px solid rgba(255,255,255,.07);border-radius:14px;overflow:hidden;margin-bottom:20px">
          <table style="width:100%;border-collapse:collapse">
            <thead><tr style="background:rgba(255,255,255,.02)">
              {''.join(f'<th style="padding:10px 14px;font-size:10px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#6b7280;text-align:left">{h}</th>' for h in ["ID","Name","Type","Location","Status","Last Maint.","Next Maint."])}
            </tr></thead>
            <tbody>{''.join(rows)}</tbody>
          </table>
        </div>""", unsafe_allow_html=True)

        with st.expander("🔍 Asset Detail View"):
            sel = st.selectbox("Select Asset", [a.id for a in st.session_state.assets],
                               format_func=lambda x: next((a.name for a in st.session_state.assets if a.id==x), x))
            asset = next(a for a in st.session_state.assets if a.id==sel)
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""
                <div style="background:#181b22;border:1px solid rgba(255,255,255,.06);border-radius:12px;padding:18px">
                  <div style="font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#6b7280;margin-bottom:12px">Basic Info</div>
                  {''.join(f'<div style="display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid rgba(255,255,255,.04)"><span style="font-size:12px;color:#6b7280">{k}</span><span style="font-size:12px;color:#e8eaf0;font-weight:500">{v}</span></div>' for k,v in [("Manufacturer",asset.manufacturer),("Model",asset.model),("Serial",asset.serial_number),("Type",asset.type),("Location",asset.location)])}
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div style="background:#181b22;border:1px solid rgba(255,255,255,.06);border-radius:12px;padding:18px">
                  <div style="font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#6b7280;margin-bottom:12px">Maintenance</div>
                  {''.join(f'<div style="display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid rgba(255,255,255,.04)"><span style="font-size:12px;color:#6b7280">{k}</span><span style="font-size:12px;color:#e8eaf0;font-family:\'DM Mono\',monospace">{v}</span></div>' for k,v in [("Purchased",asset.purchase_date),("Last Maint.",asset.last_maintenance),("Next Maint.",asset.next_maintenance),("Warranty",asset.warranty_expiry)])}
                  {"<div style='margin-top:10px;font-size:12px;color:#6b7280'>"+asset.notes+"</div>" if asset.notes else ""}
                </div>""", unsafe_allow_html=True)

    with tab2:
        with st.form("add_asset"):
            c1, c2 = st.columns(2)
            with c1:
                aid   = st.text_input("Asset ID",    value=f"AST{len(st.session_state.assets)+1:03d}")
                name  = st.text_input("Asset Name")
                atype = st.selectbox("Type", ["HVAC","Elevator","Electrical","Plumbing","Fire Safety"])
                loc   = st.text_input("Location")
                stat  = st.selectbox("Status", ["Operational","Maintenance Required","Out of Service","Retired"])
                mfr   = st.text_input("Manufacturer")
            with c2:
                model = st.text_input("Model")
                sn    = st.text_input("Serial Number")
                pd_   = st.date_input("Purchase Date",    datetime.now())
                lm    = st.date_input("Last Maintenance", datetime.now())
                nm    = st.date_input("Next Maintenance", datetime.now()+timedelta(days=90))
                we    = st.date_input("Warranty Expiry",  datetime.now()+timedelta(days=365))
            notes = st.text_area("Notes")
            if st.form_submit_button("Add Asset"):
                st.session_state.assets.append(Asset(aid,name,atype,loc,stat,
                    pd_.strftime("%Y-%m-%d"),lm.strftime("%Y-%m-%d"),
                    nm.strftime("%Y-%m-%d"),mfr,model,sn,we.strftime("%Y-%m-%d"),notes))
                add_notif(f"Asset '{name}' added", "success")
                st.success(f"✅ Asset **{name}** added successfully!")
                st.rerun()

    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            sc = pd.DataFrame([{"Status":a.status,"Count":1} for a in st.session_state.assets]).groupby("Status").sum().reset_index()
            fig = px.pie(sc, values="Count", names="Status", title="Asset Status Distribution",
                         color_discrete_sequence=COLORS, hole=0.4)
            fig.update_layout(**PLOTLY_LAYOUT, title_font=dict(size=14,color="#e8eaf0"))
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            tc = pd.DataFrame([{"Type":a.type,"Count":1} for a in st.session_state.assets]).groupby("Type").sum().reset_index()
            fig2 = px.bar(tc, x="Type", y="Count", title="Assets by Type",
                          color="Type", color_discrete_sequence=COLORS)
            fig2.update_layout(**PLOTLY_LAYOUT, title_font=dict(size=14,color="#e8eaf0"),
                               xaxis=dict(gridcolor="rgba(255,255,255,.05)"),
                               yaxis=dict(gridcolor="rgba(255,255,255,.05)"))
            st.plotly_chart(fig2, use_container_width=True)

        # Maintenance timeline
        fig3 = go.Figure()
        for a in st.session_state.assets:
            fig3.add_trace(go.Scatter(
                x=[a.last_maintenance, a.next_maintenance], y=[a.name, a.name],
                mode="lines+markers", name=a.name, line=dict(width=3),
                marker=dict(size=10, symbol="circle")))
        fig3.update_layout(**PLOTLY_LAYOUT, title="Maintenance Timeline",
                           title_font=dict(size=14,color="#e8eaf0"), height=300,
                           xaxis=dict(gridcolor="rgba(255,255,255,.05)"),
                           yaxis=dict(gridcolor="rgba(255,255,255,.05)"))
        st.plotly_chart(fig3, use_container_width=True)


def page_work_orders():
    section_header("Work Orders", "Work Order Management", "Create, assign, and track maintenance tasks.")
    tab1, tab2, tab3 = st.tabs(["📋  All Orders", "➕  Create Order", "📊  Analytics"])

    with tab1:
        c1, c2 = st.columns(2)
        sf = c1.multiselect("Status", ["Open","In Progress","Completed","Cancelled"], default=["Open","In Progress"])
        pf = c2.multiselect("Priority", ["High","Medium","Low"])

        wos = st.session_state.work_orders
        if sf: wos = [w for w in wos if w.status in sf]
        if pf: wos = [w for w in wos if w.priority in pf]

        rows = []
        for w in wos:
            rows.append(f"""
            <tr>
              <td style="padding:12px 14px;font-family:'DM Mono',monospace;font-size:11px;color:#6b7280;border-bottom:1px solid rgba(255,255,255,.04)">{w.id}</td>
              <td style="padding:12px 14px;font-size:13px;color:#e8eaf0;font-weight:500;border-bottom:1px solid rgba(255,255,255,.04)">{w.title}</td>
              <td style="padding:12px 14px;border-bottom:1px solid rgba(255,255,255,.04)">{priority_badge(w.priority)}</td>
              <td style="padding:12px 14px;border-bottom:1px solid rgba(255,255,255,.04)">{status_badge(w.status)}</td>
              <td style="padding:12px 14px;font-size:12px;color:#9ca3af;border-bottom:1px solid rgba(255,255,255,.04)">{w.assigned_to}</td>
              <td style="padding:12px 14px;font-size:12px;font-family:'DM Mono',monospace;color:#6b7280;border-bottom:1px solid rgba(255,255,255,.04)">{w.due_date}</td>
              <td style="padding:12px 14px;font-size:12px;font-family:'DM Mono',monospace;color:#6b7280;border-bottom:1px solid rgba(255,255,255,.04)">{w.estimated_hours}h est / {w.actual_hours}h act</td>
            </tr>""")

        st.markdown(f"""
        <div style="background:#111318;border:1px solid rgba(255,255,255,.07);border-radius:14px;overflow:hidden;margin-bottom:20px">
          <table style="width:100%;border-collapse:collapse">
            <thead><tr style="background:rgba(255,255,255,.02)">
              {''.join(f'<th style="padding:10px 14px;font-size:10px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#6b7280;text-align:left">{h}</th>' for h in ["ID","Title","Priority","Status","Assigned To","Due Date","Hours"])}
            </tr></thead>
            <tbody>{''.join(rows)}</tbody>
          </table>
        </div>""", unsafe_allow_html=True)

        with st.expander("✏️ Update Work Order"):
            sel = st.selectbox("Select Work Order", [w.id for w in st.session_state.work_orders],
                               format_func=lambda x: next((w.title for w in st.session_state.work_orders if w.id==x),x))
            wo = next(w for w in st.session_state.work_orders if w.id==sel)
            c1, c2, c3 = st.columns(3)
            ns = c1.selectbox("Status", ["Open","In Progress","Completed","Cancelled"],
                              index=["Open","In Progress","Completed","Cancelled"].index(wo.status))
            ah = c2.number_input("Actual Hours", 0.0, 200.0, float(wo.actual_hours), 0.5)
            co = c3.number_input("Cost ($)",    0.0, 99999.0, float(wo.cost), 10.0)
            nt = st.text_area("Notes", value=wo.notes)
            if st.button("Update Work Order"):
                wo.status = ns; wo.actual_hours = ah; wo.cost = co; wo.notes = nt
                add_notif(f"Work Order {wo.id} updated to '{ns}'", "info")
                st.success(f"✅ Work Order **{wo.id}** updated!")
                st.rerun()

    with tab2:
        with st.form("create_wo"):
            c1, c2 = st.columns(2)
            with c1:
                wid  = st.text_input("Work Order ID", value=f"WO{len(st.session_state.work_orders)+1:03d}")
                title= st.text_input("Title")
                asel = st.selectbox("Asset", [a.id for a in st.session_state.assets],
                                    format_func=lambda x: next((a.name for a in st.session_state.assets if a.id==x),x))
                prio = st.selectbox("Priority", ["High","Medium","Low"])
            with c2:
                avail_names = [s.name for s in st.session_state.staff if s.availability=="Available"]
                asgn = st.selectbox("Assign To", avail_names if avail_names else ["No staff available"])
                due  = st.date_input("Due Date", datetime.now()+timedelta(days=7))
                ehr  = st.number_input("Estimated Hours", 0.5, 200.0, 2.0, 0.5)
            desc = st.text_area("Description")
            nt   = st.text_area("Notes")
            if st.form_submit_button("Create Work Order"):
                st.session_state.work_orders.append(WorkOrder(
                    wid,title,desc,asel,prio,"Open",
                    datetime.now().strftime("%Y-%m-%d"),due.strftime("%Y-%m-%d"),asgn,ehr,notes=nt))
                add_notif(f"Work Order '{title}' created", "success")
                st.success(f"✅ Work Order **{wid}** created!")
                st.rerun()

    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            sc = pd.DataFrame([{"Status":w.status,"Count":1} for w in st.session_state.work_orders]).groupby("Status").sum().reset_index()
            fig = px.bar(sc, x="Status", y="Count", title="Orders by Status", color="Status", color_discrete_sequence=COLORS)
            fig.update_layout(**PLOTLY_LAYOUT, title_font=dict(size=14,color="#e8eaf0"),
                              xaxis=dict(gridcolor="rgba(255,255,255,.05)"),
                              yaxis=dict(gridcolor="rgba(255,255,255,.05)"))
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            pc = pd.DataFrame([{"Priority":w.priority,"Count":1} for w in st.session_state.work_orders]).groupby("Priority").sum().reset_index()
            fig2 = px.pie(pc, values="Count", names="Priority", title="Orders by Priority",
                          color_discrete_sequence=["#ef4444","#f59e0b","#00e5a0"], hole=0.4)
            fig2.update_layout(**PLOTLY_LAYOUT, title_font=dict(size=14,color="#e8eaf0"))
            st.plotly_chart(fig2, use_container_width=True)

        done = [w for w in st.session_state.work_orders if w.status=="Completed" and w.actual_hours>0]
        if done:
            df = pd.DataFrame([{"ID":w.id,"Estimated":w.estimated_hours,"Actual":w.actual_hours} for w in done])
            fig3 = go.Figure()
            fig3.add_trace(go.Bar(name="Estimated", x=df["ID"], y=df["Estimated"], marker_color=COLORS[1]))
            fig3.add_trace(go.Bar(name="Actual",    x=df["ID"], y=df["Actual"],    marker_color=COLORS[0]))
            fig3.update_layout(**PLOTLY_LAYOUT, title="Estimated vs Actual Hours",
                               title_font=dict(size=14,color="#e8eaf0"), barmode="group",
                               xaxis=dict(gridcolor="rgba(255,255,255,.05)"),
                               yaxis=dict(gridcolor="rgba(255,255,255,.05)"))
            st.plotly_chart(fig3, use_container_width=True)


def page_staff():
    section_header("Staff", "Staff Management", "Manage technicians, skills, and availability.")
    tab1, tab2 = st.tabs(["👥  Team Directory", "➕  Add Staff Member"])

    with tab1:
        initials_colors = {"John Smith":"#059669","Mike Johnson":"#b45309","Sarah Williams":"#1d4ed8","Carlos Reyes":"#7c3aed"}
        cols = st.columns(2)
        for i, s in enumerate(st.session_state.staff):
            ic = initials_colors.get(s.name,"#374151")
            ini = "".join([n[0] for n in s.name.split()][:2])
            skills_html = "".join(f'<span style="background:rgba(255,255,255,.05);color:#9ca3af;border-radius:6px;padding:2px 8px;font-size:10.5px;margin-right:4px;font-family:\'DM Mono\',monospace">{sk}</span>' for sk in s.skills)
            with cols[i % 2]:
                st.markdown(f"""
                <div style="background:#111318;border:1px solid rgba(255,255,255,.07);border-radius:14px;padding:20px;margin-bottom:16px">
                  <div style="display:flex;align-items:center;gap:14px;margin-bottom:14px">
                    <div style="width:46px;height:46px;border-radius:50%;background:{ic};display:flex;align-items:center;justify-content:center;font-size:16px;font-weight:700;color:#fff;flex-shrink:0">{ini}</div>
                    <div>
                      <div style="font-size:15px;font-weight:600;color:#e8eaf0">{s.name}</div>
                      <div style="font-size:12px;color:#6b7280;margin-top:2px">{s.role} · {s.department}</div>
                    </div>
                    <div style="margin-left:auto">{avail_badge(s.availability)}</div>
                  </div>
                  <div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px">{skills_html}</div>
                  <div style="display:flex;gap:20px">
                    <div style="font-size:11px;color:#6b7280">📧 {s.email}</div>
                    <div style="font-size:11px;color:#6b7280">📞 {s.phone}</div>
                    <div style="font-size:11px;color:#00e5a0;font-family:'DM Mono',monospace;margin-left:auto">${s.hourly_rate}/hr</div>
                  </div>
                </div>""", unsafe_allow_html=True)

        # Availability chart
        ac = pd.DataFrame([{"Availability":s.availability,"Count":1} for s in st.session_state.staff]).groupby("Availability").sum().reset_index()
        fig = px.pie(ac, values="Count", names="Availability", title="Team Availability",
                     color_discrete_sequence=["#00e5a0","#f59e0b","#6b7280"], hole=0.4)
        fig.update_layout(**PLOTLY_LAYOUT, title_font=dict(size=14,color="#e8eaf0"))
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        with st.form("add_staff"):
            c1, c2 = st.columns(2)
            with c1:
                sid   = st.text_input("Staff ID", value=f"STF{len(st.session_state.staff)+1:03d}")
                name  = st.text_input("Full Name")
                role  = st.text_input("Role")
                dept  = st.selectbox("Department", ["HVAC","Elevator","Electrical","Plumbing","General"])
            with c2:
                email = st.text_input("Email")
                phone = st.text_input("Phone")
                rate  = st.number_input("Hourly Rate ($)", 15.0, 150.0, 35.0, 5.0)
                avail = st.selectbox("Availability", ["Available","Busy","Off"])
            skills = st.multiselect("Skills", ["HVAC","Electrical","Plumbing","Elevators","Generators","BMS","Fire Safety","Carpentry"])
            if st.form_submit_button("Add Staff Member"):
                st.session_state.staff.append(Staff(sid,name,role,dept,email,phone,skills,avail,rate))
                add_notif(f"Staff member '{name}' added", "success")
                st.success(f"✅ **{name}** added to the team!")
                st.rerun()


def page_inventory():
    section_header("Inventory", "Inventory Management", "Track parts, supplies, and reorder levels.")
    tab1, tab2, tab3 = st.tabs(["📦  Stock Levels", "➕  Add Item", "📊  Analytics"])

    with tab1:
        low = [i for i in st.session_state.inventory if i.quantity <= i.reorder_level]
        if low:
            st.warning(f"⚠️ **{len(low)} item(s)** are at or below reorder level and need restocking.")

        rows = []
        for item in st.session_state.inventory:
            at_low = item.quantity <= item.reorder_level
            pct = min(100, int(item.quantity / max(item.reorder_level*2,1)*100))
            bar_c = "#00e5a0" if pct>60 else ("#f59e0b" if pct>30 else "#ef4444")
            row_bg = "rgba(239,68,68,.04)" if at_low else ""
            bar_html = f'<div style="height:4px;background:rgba(255,255,255,.06);border-radius:4px;overflow:hidden;margin-top:4px"><div style="height:100%;width:{pct}%;background:{bar_c};border-radius:4px"></div></div>'
            rows.append(f"""
            <tr style="background:{row_bg}">
              <td style="padding:12px 14px;font-family:'DM Mono',monospace;font-size:11px;color:#6b7280;border-bottom:1px solid rgba(255,255,255,.04)">{item.id}</td>
              <td style="padding:12px 14px;border-bottom:1px solid rgba(255,255,255,.04)">
                <div style="font-size:13px;color:#e8eaf0;font-weight:500">{item.name}</div>
                {bar_html}
              </td>
              <td style="padding:12px 14px;font-size:12px;color:#9ca3af;border-bottom:1px solid rgba(255,255,255,.04)">{item.category}</td>
              <td style="padding:12px 14px;font-size:13px;font-family:'DM Mono',monospace;color:{bar_c};font-weight:600;border-bottom:1px solid rgba(255,255,255,.04)">{item.quantity} {item.unit}</td>
              <td style="padding:12px 14px;font-size:12px;font-family:'DM Mono',monospace;color:#6b7280;border-bottom:1px solid rgba(255,255,255,.04)">{item.reorder_level}</td>
              <td style="padding:12px 14px;font-size:12px;color:#9ca3af;border-bottom:1px solid rgba(255,255,255,.04)">{item.supplier}</td>
              <td style="padding:12px 14px;font-size:12px;font-family:'DM Mono',monospace;color:#00e5a0;border-bottom:1px solid rgba(255,255,255,.04)">${item.unit_cost}</td>
              <td style="padding:12px 14px;font-size:11px;color:#6b7280;border-bottom:1px solid rgba(255,255,255,.04)">{item.location}</td>
            </tr>""")

        st.markdown(f"""
        <div style="background:#111318;border:1px solid rgba(255,255,255,.07);border-radius:14px;overflow:hidden;margin-bottom:20px">
          <table style="width:100%;border-collapse:collapse">
            <thead><tr style="background:rgba(255,255,255,.02)">
              {''.join(f'<th style="padding:10px 14px;font-size:10px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#6b7280;text-align:left">{h}</th>' for h in ["ID","Item","Category","Quantity","Reorder","Supplier","Unit Cost","Location"])}
            </tr></thead>
            <tbody>{''.join(rows)}</tbody>
          </table>
        </div>""", unsafe_allow_html=True)

    with tab2:
        with st.form("add_inv"):
            c1, c2 = st.columns(2)
            with c1:
                iid  = st.text_input("Item ID", value=f"INV{len(st.session_state.inventory)+1:03d}")
                name = st.text_input("Item Name")
                cat  = st.selectbox("Category", ["HVAC","Electrical","Plumbing","Elevator","General"])
                qty  = st.number_input("Quantity", 0, 99999, 0)
                unit = st.text_input("Unit (e.g. pcs, gallons, boxes)")
            with c2:
                rl   = st.number_input("Reorder Level", 0, 99999, 10)
                sup  = st.text_input("Supplier")
                uc   = st.number_input("Unit Cost ($)", 0.0, 99999.0, 0.0, 0.5)
                loc  = st.text_input("Storage Location")
            lo = st.date_input("Last Ordered", datetime.now())
            if st.form_submit_button("Add Item"):
                st.session_state.inventory.append(Inventory(iid,name,cat,qty,unit,rl,sup,uc,loc,lo.strftime("%Y-%m-%d")))
                add_notif(f"Inventory item '{name}' added","success")
                st.success(f"✅ **{name}** added to inventory!")
                st.rerun()

    with tab3:
        c1, c2 = st.columns(2)
        with c1:
            df = pd.DataFrame([{"Category":i.category,"Value":i.quantity*i.unit_cost} for i in st.session_state.inventory]).groupby("Category").sum().reset_index()
            fig = px.pie(df,values="Value",names="Category",title="Inventory Value by Category",
                         color_discrete_sequence=COLORS,hole=0.4)
            fig.update_layout(**PLOTLY_LAYOUT,title_font=dict(size=14,color="#e8eaf0"))
            st.plotly_chart(fig,use_container_width=True)
        with c2:
            df2 = pd.DataFrame([{"Item":i.name.split()[0],"Quantity":i.quantity,"Reorder":i.reorder_level} for i in st.session_state.inventory])
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(name="Quantity",    x=df2["Item"],y=df2["Quantity"],marker_color=COLORS[0]))
            fig2.add_trace(go.Bar(name="Reorder Lvl", x=df2["Item"],y=df2["Reorder"], marker_color=COLORS[3]))
            fig2.update_layout(**PLOTLY_LAYOUT,title="Stock vs Reorder Level",barmode="group",
                               title_font=dict(size=14,color="#e8eaf0"),
                               xaxis=dict(gridcolor="rgba(255,255,255,.05)"),
                               yaxis=dict(gridcolor="rgba(255,255,255,.05)"))
            st.plotly_chart(fig2,use_container_width=True)


def page_reports():
    section_header("Analytics", "Reports & Analytics", "Data-driven insights across all facility operations.")

    rtype = st.selectbox("Report Type", ["Executive Summary","Maintenance Report","Cost Analysis","Asset Performance"])

    if rtype == "Executive Summary":
        op  = sum(1 for a in st.session_state.assets if a.status=="Operational")
        tot = len(st.session_state.assets)
        done_pct = len([w for w in st.session_state.work_orders if w.status=="Completed"]) / max(len(st.session_state.work_orders),1) * 100
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Asset Health",       f"{int(op/tot*100)}%",   f"{op}/{tot} operational")
        c2.metric("Completion Rate",    f"{done_pct:.0f}%",      "Work orders completed")
        c3.metric("Total Inv. Value",   f"${sum(i.quantity*i.unit_cost for i in st.session_state.inventory):,.0f}", "Current stock")
        c4.metric("Total Labor Cost",   f"${sum(w.actual_hours*next((s.hourly_rate for s in st.session_state.staff if s.name==w.assigned_to),35) for w in st.session_state.work_orders if w.actual_hours>0):,.0f}", "Billed hours")

        c1, c2 = st.columns(2)
        with c1:
            sc = pd.DataFrame([{"Status":a.status,"n":1} for a in st.session_state.assets]).groupby("Status").sum().reset_index()
            fig = px.pie(sc,values="n",names="Status",title="Asset Health",color_discrete_sequence=COLORS,hole=0.4)
            fig.update_layout(**PLOTLY_LAYOUT,title_font=dict(size=14,color="#e8eaf0"))
            st.plotly_chart(fig,use_container_width=True)
        with c2:
            wsc = pd.DataFrame([{"Status":w.status,"n":1} for w in st.session_state.work_orders]).groupby("Status").sum().reset_index()
            fig2 = px.bar(wsc,x="Status",y="n",title="Work Order Summary",color="Status",color_discrete_sequence=COLORS)
            fig2.update_layout(**PLOTLY_LAYOUT,title_font=dict(size=14,color="#e8eaf0"),
                               xaxis=dict(gridcolor="rgba(255,255,255,.05)"),
                               yaxis=dict(gridcolor="rgba(255,255,255,.05)"))
            st.plotly_chart(fig2,use_container_width=True)

    elif rtype == "Maintenance Report":
        today = datetime.now().date()
        upcoming = [a for a in st.session_state.assets
                    if today <= datetime.strptime(a.next_maintenance,"%Y-%m-%d").date() <= today+timedelta(days=30)]
        st.markdown('<div style="font-size:14px;font-weight:600;color:#e8eaf0;margin-bottom:12px">Scheduled in next 30 days</div>',unsafe_allow_html=True)
        if upcoming:
            for a in upcoming:
                d = datetime.strptime(a.next_maintenance,"%Y-%m-%d").date()
                st.info(f"📅 **{a.name}** — Due {a.next_maintenance} ({(d-today).days} days)")
        else:
            st.info("No maintenance scheduled in the next 30 days.")

        completed = [w for w in st.session_state.work_orders if w.status=="Completed"]
        if completed:
            st.markdown('<div style="font-size:14px;font-weight:600;color:#e8eaf0;margin:20px 0 12px">Completed Work Orders</div>',unsafe_allow_html=True)
            df = pd.DataFrame([{"WO":w.id,"Title":w.title,"Asset":w.asset_id,"Hours":w.actual_hours,"Cost":f"${w.cost:.0f}"} for w in completed])
            st.dataframe(df,use_container_width=True,hide_index=True)

    elif rtype == "Cost Analysis":
        labor = sum(w.actual_hours * next((s.hourly_rate for s in st.session_state.staff if s.name==w.assigned_to),35)
                    for w in st.session_state.work_orders if w.actual_hours>0)
        parts = sum(w.cost for w in st.session_state.work_orders)
        inv_v = sum(i.quantity*i.unit_cost for i in st.session_state.inventory)

        c1,c2,c3 = st.columns(3)
        c1.metric("Labor Costs",    f"${labor:,.2f}")
        c2.metric("Parts & Materials", f"${parts:,.2f}")
        c3.metric("Inventory Value",f"${inv_v:,.2f}")

        asset_cost = {}
        for w in st.session_state.work_orders:
            asset_cost[w.asset_id] = asset_cost.get(w.asset_id,0) + w.cost
        df = pd.DataFrame([{"Asset":k,"Cost":v} for k,v in asset_cost.items()])
        fig = px.bar(df,x="Asset",y="Cost",title="Maintenance Costs by Asset",color="Cost",
                     color_continuous_scale=["#111318","#00e5a0"])
        fig.update_layout(**PLOTLY_LAYOUT,title_font=dict(size=14,color="#e8eaf0"),
                          xaxis=dict(gridcolor="rgba(255,255,255,.05)"),
                          yaxis=dict(gridcolor="rgba(255,255,255,.05)"))
        st.plotly_chart(fig,use_container_width=True)

    elif rtype == "Asset Performance":
        df = pd.DataFrame([{
            "Asset": a.name[:20],
            "Days Since Maint.": (datetime.now().date()-datetime.strptime(a.last_maintenance,"%Y-%m-%d").date()).days,
            "Status": a.status
        } for a in st.session_state.assets])
        fig = px.bar(df,x="Asset",y="Days Since Maint.",title="Days Since Last Maintenance",
                     color="Status",color_discrete_map={"Operational":"#00e5a0","Maintenance Required":"#f59e0b","Out of Service":"#ef4444","Retired":"#6b7280"})
        fig.update_layout(**PLOTLY_LAYOUT,title_font=dict(size=14,color="#e8eaf0"),
                          xaxis=dict(gridcolor="rgba(255,255,255,.05)"),
                          yaxis=dict(gridcolor="rgba(255,255,255,.05)"))
        st.plotly_chart(fig,use_container_width=True)


# ── SIDEBAR ──────────────────────────────────────────────────────────────────
def sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="padding:0 4px 20px">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px">
            <div style="width:32px;height:32px;background:linear-gradient(135deg,#00e5a0,#3b82f6);border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:16px">🏢</div>
            <div style="font-family:'DM Serif Display',serif;font-size:20px;color:#e8eaf0 !important">FacilityOS</div>
          </div>
          <div style="display:flex;align-items:center;gap:6px;margin-left:42px">
            <div style="width:6px;height:6px;border-radius:50%;background:#00e5a0;box-shadow:0 0 6px #00e5a0;animation:pulse 2s infinite"></div>
            <div style="font-size:11px;color:#6b7280;font-family:'DM Mono',monospace">System Online</div>
          </div>
        </div>
        <style>@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}</style>
        """, unsafe_allow_html=True)

        page = st.selectbox("Navigation", [
            "🏠  Dashboard",
            "🏭  Assets",
            "📋  Work Orders",
            "👥  Staff",
            "📦  Inventory",
            "📊  Reports"
        ])

        st.markdown("---")

        # Alerts
        alerts = maintenance_alerts()
        if alerts:
            st.markdown('<div style="font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#6b7280;margin-bottom:8px">⚠️ Alerts</div>', unsafe_allow_html=True)
            for _, title, sub, atype in alerts[:4]:
                if atype=="error":   st.error(f"**{title.split(':')[0]}**\n{sub}",   icon="🔴")
                elif atype=="warning": st.warning(f"**{title.split(':')[0]}**\n{sub}", icon="🟡")
                else:                st.info(f"**{title.split(':')[0]}**\n{sub}",    icon="🔵")

        # Quick actions
        st.markdown("---")
        st.markdown('<div style="font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#6b7280;margin-bottom:8px">⚡ Quick Stats</div>', unsafe_allow_html=True)
        inv_val = sum(i.quantity*i.unit_cost for i in st.session_state.inventory)
        st.markdown(f"""
        <div style="background:#181b22;border:1px solid rgba(255,255,255,.06);border-radius:10px;padding:12px 14px;margin-bottom:8px">
          <div style="font-size:10px;color:#6b7280;text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px">Inventory Value</div>
          <div style="font-family:'DM Mono',monospace;font-size:18px;color:#00e5a0">${inv_val:,.0f}</div>
        </div>""", unsafe_allow_html=True)

        # Notifications
        if st.session_state.notifs:
            st.markdown("---")
            st.markdown('<div style="font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#6b7280;margin-bottom:8px">🔔 Activity</div>', unsafe_allow_html=True)
            for n in st.session_state.notifs[:5]:
                icon = "✅" if n["type"]=="success" else "ℹ️"
                st.markdown(f'<div style="font-size:11px;color:#9ca3af;padding:5px 0;border-bottom:1px solid rgba(255,255,255,.04)">{icon} {n["msg"]} <span style="color:#4b5563;font-family:\'DM Mono\',monospace">{n["ts"]}</span></div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(f'<div style="font-size:10px;color:#374151;font-family:\'DM Mono\',monospace">FacilityOS v2.0 · {datetime.now().strftime("%b %d, %Y")}</div>', unsafe_allow_html=True)
        return page


# ── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    init()
    page = sidebar()
    if   "Dashboard"   in page: page_dashboard()
    elif "Assets"      in page: page_assets()
    elif "Work Orders" in page: page_work_orders()
    elif "Staff"       in page: page_staff()
    elif "Inventory"   in page: page_inventory()
    elif "Reports"     in page: page_reports()

if __name__ == "__main__":
    main()
