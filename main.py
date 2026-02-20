import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from dataclasses import dataclass
from typing import List
import io, csv

st.set_page_config(page_title="FacilityOS", page_icon="\U0001f3e2", layout="wide", initial_sidebar_state="expanded")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Mono:wght@400;500&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

/* ── BASE ── */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background-color: #f0f2f5 !important;
    color: #1a1d23 !important;
}
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
.block-container { padding: 32px 40px 60px !important; max-width: 1440px !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #1e2433 !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * { color: #8b95a8 !important; }
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #262d3d !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    color: #e2e8f0 !important;
    border-radius: 10px !important;
}
[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    background: #262d3d !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    color: #8b95a8 !important;
    border-radius: 10px !important;
    font-size: 13px !important;
    padding: 8px 16px !important;
    transition: all 0.2s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    border-color: #3b82f6 !important;
    color: #3b82f6 !important;
    background: rgba(59,130,246,0.08) !important;
}

/* ── METRICS ── */
[data-testid="metric-container"] {
    background: #ffffff !important;
    border: 1px solid #e8ecf0 !important;
    border-radius: 16px !important;
    padding: 22px !important;
    transition: all 0.2s !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
}
[data-testid="metric-container"]:hover {
    border-color: #c7d2fe !important;
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.1) !important;
}
[data-testid="stMetricLabel"] {
    color: #64748b !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.09em !important;
}
[data-testid="stMetricValue"] {
    color: #0f172a !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 34px !important;
}
[data-testid="stMetricDelta"] { font-size: 12px !important; }

/* ── TABS ── */
[data-testid="stTabs"] [role="tablist"] {
    background: #e8ecf0 !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 4px !important;
    gap: 2px !important;
}
[data-testid="stTabs"] [role="tab"] {
    border-radius: 9px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #64748b !important;
    padding: 7px 18px !important;
    border: none !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: #ffffff !important;
    color: #3b82f6 !important;
    border: none !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.12) !important;
}
[data-testid="stTabs"] [role="tabpanel"] { padding-top: 20px !important; }

/* ── INPUTS ── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stDateInput"] input {
    background: #ffffff !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 10px !important;
    color: #0f172a !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04) !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.12) !important;
}
[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiSelect"] > div > div {
    background: #ffffff !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 10px !important;
    color: #0f172a !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04) !important;
}
label { color: #64748b !important; font-size: 12px !important; font-weight: 600 !important; letter-spacing: 0.02em !important; }

/* ── BUTTONS ── */
.stButton > button {
    background: #3b82f6 !important;
    border: none !important;
    border-radius: 10px !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    padding: 10px 22px !important;
    transition: all 0.2s !important;
    letter-spacing: 0.01em !important;
    box-shadow: 0 2px 8px rgba(59,130,246,0.3) !important;
}
.stButton > button:hover {
    background: #2563eb !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 16px rgba(59,130,246,0.4) !important;
}
.danger-btn .stButton > button {
    background: #ef4444 !important;
    box-shadow: 0 2px 8px rgba(239,68,68,0.3) !important;
}
.danger-btn .stButton > button:hover {
    background: #dc2626 !important;
    box-shadow: 0 6px 16px rgba(239,68,68,0.4) !important;
}

/* ── EXPANDER ── */
[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 14px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05) !important;
}
[data-testid="stExpander"] summary { color: #475569 !important; font-size: 13px !important; font-weight: 600 !important; }

/* ── ALERTS ── */
[data-testid="stAlert"] { border-radius: 12px !important; }

/* ── DOWNLOAD BUTTON ── */
[data-testid="stDownloadButton"] > button {
    background: #f1f5f9 !important;
    border: 1.5px solid #e2e8f0 !important;
    color: #475569 !important;
    border-radius: 10px !important;
    font-size: 12px !important;
    padding: 7px 16px !important;
    font-weight: 600 !important;
    box-shadow: none !important;
}
[data-testid="stDownloadButton"] > button:hover {
    border-color: #3b82f6 !important;
    color: #3b82f6 !important;
    background: #eff6ff !important;
}

/* ── TAGS ── */
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
    background: #eff6ff !important;
    color: #3b82f6 !important;
    border-radius: 6px !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    border: 1px solid #e2e8f0 !important;
    border-radius: 14px !important;
    overflow: hidden !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05) !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #f1f5f9; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }

@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.5} }
@keyframes fadeUp { from{opacity:0;transform:translateY(14px)} to{opacity:1;transform:translateY(0)} }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ── MODELS ──────────────────────────────────────────────────────────────────
@dataclass
class Asset:
    id:str; name:str; type:str; location:str; status:str
    purchase_date:str; last_maintenance:str; next_maintenance:str
    manufacturer:str; model:str; serial_number:str; warranty_expiry:str
    purchase_cost:float=0.0; notes:str=""

@dataclass
class WorkOrder:
    id:str; title:str; description:str; asset_id:str
    priority:str; status:str; created_date:str; due_date:str
    assigned_to:str; estimated_hours:float
    actual_hours:float=0; cost:float=0; notes:str=""

@dataclass
class Staff:
    id:str; name:str; role:str; department:str
    email:str; phone:str; skills:List[str]
    availability:str; hourly_rate:float

@dataclass
class Inventory:
    id:str; name:str; category:str; quantity:int
    unit:str; reorder_level:int; supplier:str
    unit_cost:float; location:str; last_ordered:str

@dataclass
class Vendor:
    id:str; name:str; category:str; contact_name:str
    email:str; phone:str; address:str
    rating:float; contract_end:str; notes:str=""

@dataclass
class Budget:
    id:str; category:str; year:int; month:int
    allocated:float; spent:float=0.0

# ── SAMPLE DATA ──────────────────────────────────────────────────────────────
def load_assets():
    return [
        Asset("AST001","HVAC System - Building A","HVAC","Building A, Floor 1","Operational","2022-01-15","2024-01-15","2024-04-15","Carrier","XRS-2000","HV2022001","2025-01-15",45000),
        Asset("AST002","Elevator - Main Lobby","Elevator","Building A, Lobby","Maintenance Required","2021-06-20","2024-02-01","2024-03-01","Otis","Elev-500","EL2021005","2024-06-20",120000,"Strange noise during operation"),
        Asset("AST003","Generator - Backup","Electrical","Building B, Basement","Operational","2023-03-10","2024-02-10","2024-05-10","Kohler","GEN-1000","GN2023010","2026-03-10",28000),
        Asset("AST004","Fire Suppression System","Fire Safety","Building A, All Floors","Operational","2022-09-01","2024-01-20","2024-07-20","Kidde","FS-Pro","FS2022009","2025-09-01",35000),
        Asset("AST005","Chiller Unit - Roof","HVAC","Building A, Rooftop","Out of Service","2020-04-15","2023-12-01","2024-02-01","Trane","CH-800","TR2020004","2023-04-15",95000,"Compressor failure"),
        Asset("AST006","Parking Lot Lights","Electrical","External Parking","Operational","2023-07-01","2024-01-10","2024-06-10","GE","LED-400","GE2023007","2026-07-01",12000),
    ]

def load_work_orders():
    return [
        WorkOrder("WO001","HVAC Filter Replacement","Replace air filters in Building A","AST001","Medium","In Progress","2024-02-15","2024-02-20","John Smith",2,1.5,150),
        WorkOrder("WO002","Elevator Emergency Maintenance","Emergency maintenance - strange noise","AST002","High","Open","2024-02-18","2024-02-19","Mike Johnson",4,0,0,"Strange noise"),
        WorkOrder("WO003","Generator Monthly Test","Monthly generator test run","AST003","Low","Completed","2024-02-10","2024-02-11","Sarah Williams",1,0.8,80),
        WorkOrder("WO004","Chiller Compressor Repair","Replace failed compressor","AST005","High","Open","2024-02-12","2024-02-25","Mike Johnson",16,0,0,"Awaiting parts"),
        WorkOrder("WO005","Fire System Inspection","Annual fire suppression inspection","AST004","Medium","Completed","2024-02-05","2024-02-08","Sarah Williams",3,3.2,200),
        WorkOrder("WO006","Parking Light Replacement","Replace 4 burned-out LEDs","AST006","Low","Completed","2024-02-01","2024-02-03","John Smith",2,1.8,95),
        WorkOrder("WO007","Elevator Cable Inspection","Routine cable tension check","AST002","Medium","Cancelled","2024-01-20","2024-01-25","Mike Johnson",3,0,0),
    ]

def load_staff():
    return [
        Staff("STF001","John Smith","Maintenance Technician","HVAC","john.smith@facility.com","555-0101",["HVAC","Electrical","Plumbing"],"Available",35),
        Staff("STF002","Mike Johnson","Senior Technician","Elevators","mike.johnson@facility.com","555-0102",["Elevators","Mechanical","Hydraulics"],"Busy",45),
        Staff("STF003","Sarah Williams","Technician","Electrical","sarah.williams@facility.com","555-0103",["Electrical","Generators","BMS"],"Available",38),
        Staff("STF004","Carlos Reyes","Plumber","Plumbing","carlos.reyes@facility.com","555-0104",["Plumbing","HVAC"],"Off",32),
        Staff("STF005","Amara Osei","Fire Safety Specialist","Fire Safety","amara.osei@facility.com","555-0105",["Fire Safety","Electrical","BMS"],"Available",42),
    ]

def load_inventory():
    return [
        Inventory("INV001","Air Filters 20x20x1","HVAC",50,"pcs",20,"HVAC Supply Co",15.50,"Warehouse A - Shelf 3","2024-02-01"),
        Inventory("INV002","LED Bulbs 60W","Electrical",200,"pcs",50,"Lighting World",4.25,"Warehouse B - Shelf 1","2024-02-15"),
        Inventory("INV003","Elevator Lubricant","Elevator",12,"gallons",10,"Elevator Parts Inc",45.00,"Warehouse A - Shelf 5","2024-01-20"),
        Inventory("INV004","HVAC Refrigerant R-410A","HVAC",8,"lbs",15,"CoolTech Supply",28.00,"Warehouse A - Shelf 2","2024-01-10"),
        Inventory("INV005","Circuit Breakers 20A","Electrical",35,"pcs",10,"Electrical Depot",12.75,"Warehouse B - Shelf 4","2024-02-10"),
        Inventory("INV006","Fire Extinguisher Refill","Fire Safety",22,"units",8,"Safety First Co",55.00,"Warehouse B - Shelf 6","2024-01-28"),
        Inventory("INV007","Hydraulic Fluid ISO 46","Elevator",5,"gallons",6,"Elevator Parts Inc",38.00,"Warehouse A - Shelf 5","2024-01-15"),
    ]

def load_vendors():
    return [
        Vendor("VEN001","HVAC Supply Co","HVAC","Tom Bradley","tom@hvacsupply.com","555-1001","123 Industrial Blvd",4.5,"2025-12-31","Primary HVAC supplier"),
        Vendor("VEN002","Elevator Parts Inc","Elevator","Lisa Chen","lisa@elevparts.com","555-1002","456 Mechanical Way",4.8,"2026-06-30","Certified Otis reseller"),
        Vendor("VEN003","Lighting World","Electrical","James Park","james@lightingworld.com","555-1003","789 Commerce St",4.2,"2025-09-30"),
        Vendor("VEN004","CoolTech Supply","HVAC","Maria Santos","maria@cooltech.com","555-1004","321 Refrigeration Ave",3.9,"2025-03-31"),
        Vendor("VEN005","Safety First Co","Fire Safety","David Kim","david@safetyfirst.com","555-1005","654 Protection Ln",4.7,"2026-01-31"),
        Vendor("VEN006","Electrical Depot","Electrical","Anna Torres","anna@elecdepot.com","555-1006","987 Power St",4.3,"2025-11-30"),
    ]

def load_budgets():
    cats = {"HVAC":8000,"Elevator":12000,"Electrical":5000,"Plumbing":3000,"Fire Safety":4000,"General":6000}
    budgets = []
    idx = 1
    rng = np.random.default_rng(42)
    for cat, alloc in cats.items():
        for m in range(1, 7):
            spent = alloc * rng.uniform(0.3, 1.1) if m < 3 else alloc * rng.uniform(0, 0.6)
            budgets.append(Budget(f"BUD{idx:03d}", cat, 2024, m, alloc, round(min(spent, alloc*1.15), 2)))
            idx += 1
    return budgets

# ── SESSION STATE ────────────────────────────────────────────────────────────
def init():
    for key, fn in [("assets",load_assets),("work_orders",load_work_orders),("staff",load_staff),
                    ("inventory",load_inventory),("vendors",load_vendors),("budgets",load_budgets)]:
        if key not in st.session_state:
            st.session_state[key] = fn()
    if "notifs" not in st.session_state:
        st.session_state.notifs = []

def add_notif(msg, t="info"):
    st.session_state.notifs.insert(0, {"msg":msg,"type":t,"ts":datetime.now().strftime("%H:%M")})
    st.session_state.notifs = st.session_state.notifs[:15]

# ── CONSTANTS ────────────────────────────────────────────────────────────────
COLORS = ["#0ea472","#3b82f6","#f59e0b","#ef4444","#a855f7","#14b8a6","#f97316","#ec4899"]
PL = dict(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
          font=dict(family="Outfit",color="#6b7280",size=12),
          margin=dict(t=44,b=20,l=10,r=10),
          legend=dict(bgcolor="rgba(255,255,255,0.8)",bordercolor="#e5e7eb"))
STATUSES = ["Operational","Maintenance Required","Out of Service","Retired"]
ASSET_TYPES = ["HVAC","Elevator","Electrical","Plumbing","Fire Safety"]
PRIORITIES = ["High","Medium","Low"]
WO_STATUSES = ["Open","In Progress","Completed","Cancelled"]
DEPARTMENTS = ["HVAC","Elevator","Electrical","Plumbing","Fire Safety","General"]
SKILLS_LIST = ["HVAC","Electrical","Plumbing","Elevators","Generators","BMS","Fire Safety","Carpentry","Painting"]
AVAIL_LIST = ["Available","Busy","Off"]
INV_CATS = ["HVAC","Electrical","Plumbing","Elevator","Fire Safety","General"]

# ── HELPERS ──────────────────────────────────────────────────────────────────
def maintenance_alerts():
    alerts, today = [], datetime.now().date()
    for a in st.session_state.assets:
        d = datetime.strptime(a.next_maintenance,"%Y-%m-%d").date()
        diff = (d-today).days
        if diff<0:    alerts.append(("overdue", a.name, f"{abs(diff)}d past due"))
        elif diff<=7: alerts.append(("urgent",  a.name, f"Due in {diff}d"))
        elif diff<=30: alerts.append(("upcoming",a.name, f"Due in {diff}d"))
    return alerts

def section_header(eye, title, sub=""):
    st.markdown(f"""<div style="margin-bottom:24px;animation:fadeUp .35s ease both">
      <div style="font-size:11px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:#0ea472;font-family:\'DM Mono\',monospace;margin-bottom:4px">{eye}</div>
      <div style="font-family:\'DM Serif Display\',serif;font-size:28px;letter-spacing:-.4px;color:#111827;line-height:1.2">{title}</div>
      {"<div style=\'font-size:13px;color:#64748b;margin-top:6px\'>"  + sub + "</div>" if sub else ""}
    </div>""", unsafe_allow_html=True)

def pb(p):  # priority badge
    c,bg = {"High":("#ef4444","rgba(239,68,68,.12)"),"Medium":("#f59e0b","rgba(245,158,11,.12)"),"Low":("#0ea472","rgba(0,229,160,.10)")}.get(p,("#9ca3af","rgba(255,255,255,.05)"))
    return f'<span style="background:{bg};color:{c};border-radius:20px;padding:3px 10px;font-size:11px;font-family:DM Mono,monospace;font-weight:600">&#9679; {p}</span>'

def sb(s):  # status badge
    c,bg = {"Open":("#60a5fa","rgba(59,130,246,.12)"),"In Progress":("#f59e0b","rgba(245,158,11,.12)"),"Completed":("#0ea472","rgba(0,229,160,.10)"),"Cancelled":("#6b7280","rgba(255,255,255,.06)")}.get(s,("#9ca3af","rgba(255,255,255,.05)"))
    return f'<span style="background:{bg};color:{c};border-radius:20px;padding:3px 10px;font-size:11px;font-family:DM Mono,monospace;font-weight:600">{s}</span>'

def avb(a):  # availability badge
    c,bg = {"Available":("#0ea472","rgba(0,229,160,.1)"),"Busy":("#f59e0b","rgba(245,158,11,.1)"),"Off":("#6b7280","rgba(255,255,255,.05)")}.get(a,("#6b7280","rgba(255,255,255,.05)"))
    return f'<span style="background:{bg};color:{c};border-radius:20px;padding:2px 10px;font-size:11px;font-family:DM Mono,monospace">&#9679; {a}</span>'

def td_cell(val, mono=False, muted=False, bold=False, color=None):
    font = "font-family:DM Mono,monospace;" if mono else ""
    col  = f"color:{color};" if color else ("color:#6b7280;" if muted else ("color:#e8eaf0;" if bold else "color:#9ca3af;"))
    fw   = "font-weight:600;" if bold else ""
    return f'<td style="padding:12px 14px;font-size:12.5px;{font}{col}{fw}border-bottom:1px solid #f3f4f6">{val}</td>'

def badge_cell(badge_html):
    return f'<td style="padding:12px 14px;border-bottom:1px solid #f3f4f6">{badge_html}</td>'

def make_table(headers, rows):
    ths = "".join(f'<th style="padding:10px 14px;font-size:10px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#64748b;text-align:left;white-space:nowrap;background:#f9fafb">{h}</th>' for h in headers)
    return f'<div style="background:#ffffff;border:1px solid #e5e7eb;border-radius:14px;overflow:hidden;margin-bottom:16px;box-shadow:0 1px 4px rgba(0,0,0,.05)"><table style="width:100%;border-collapse:collapse"><thead><tr style="background:#f9fafb">{ths}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'

def to_csv(data_list, fields):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields)
    w.writeheader()
    for item in data_list:
        w.writerow({f: getattr(item,f,"") for f in fields})
    return buf.getvalue().encode()

def stock_bar(qty, reorder):
    pct = min(100, int(qty/max(reorder*2,1)*100))
    c = "#0ea472" if pct>60 else ("#f59e0b" if pct>30 else "#ef4444")
    return f'<div style="height:4px;background:#e5e7eb;border-radius:4px"><div style="height:100%;width:{pct}%;background:{c};border-radius:4px"></div></div>', c

# ── DASHBOARD ────────────────────────────────────────────────────────────────
def page_dashboard():
    section_header("Overview","Facility Dashboard","Real-time visibility across all operations.")
    open_wo     = sum(1 for w in st.session_state.work_orders if w.status in ("Open","In Progress"))
    avail_staff = sum(1 for s in st.session_state.staff if s.availability=="Available")
    low_inv     = sum(1 for i in st.session_state.inventory if i.quantity<=i.reorder_level)
    inv_val     = sum(i.quantity*i.unit_cost for i in st.session_state.inventory)
    asset_val   = sum(a.purchase_cost for a in st.session_state.assets)
    total_spend = sum(w.cost for w in st.session_state.work_orders)
    done_pct    = len([w for w in st.session_state.work_orders if w.status=="Completed"])/max(len(st.session_state.work_orders),1)*100

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    c1.metric("Total Assets",   len(st.session_state.assets), f"${asset_val/1000:.0f}k value")
    c2.metric("Open Orders",    open_wo, "Require action")
    c3.metric("Staff Available",avail_staff, f"of {len(st.session_state.staff)}")
    c4.metric("Low Inventory",  low_inv, "Need reorder")
    c5.metric("Completion",     f"{done_pct:.0f}%", "WO done rate")
    c6.metric("Total Spend",    f"${total_spend:,.0f}", "Parts costs")
    st.markdown("<div style='height:18px'></div>",unsafe_allow_html=True)

    alerts = maintenance_alerts()
    if alerts:
        st.markdown('<div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px">Maintenance Alerts</div>',unsafe_allow_html=True)
        for typ, name, sub in alerts:
            if typ=="overdue": st.error(f"\U0001f534 **OVERDUE: {name}** — {sub}")
            elif typ=="urgent": st.warning(f"\U0001f7e1 **URGENT: {name}** — {sub}")
            else: st.info(f"\U0001f535 **UPCOMING: {name}** — {sub}")
        st.markdown("<div style='height:8px'></div>",unsafe_allow_html=True)

    c1,c2,c3 = st.columns([2,2,1])
    with c1:
        weeks = [f"Wk{i}" for i in range(1,9)]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=weeks,y=[3,2,4,2,3,4,3,open_wo],name="Opened",line=dict(color="#3b82f6",width=2.5),fill="tozeroy",fillcolor="rgba(59,130,246,.07)"))
        fig.add_trace(go.Scatter(x=weeks,y=[2,3,1,4,2,3,2,int(done_pct/10)],name="Closed",line=dict(color="#0ea472",width=2.5),fill="tozeroy",fillcolor="rgba(0,229,160,.07)"))
        fig.update_layout(**PL,title="Work Order Trend",title_font=dict(size=13,color="#111827"),height=200,xaxis=dict(gridcolor="rgba(0,0,0,.06)"),yaxis=dict(gridcolor="rgba(0,0,0,.06)"))
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        mb = [b for b in st.session_state.budgets if b.month==2]
        bdf = pd.DataFrame([{"Cat":b.category[:4],"Alloc":b.allocated,"Spent":b.spent} for b in mb])
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name="Budget",x=bdf["Cat"],y=bdf["Alloc"],marker_color="rgba(59,130,246,.35)"))
        fig2.add_trace(go.Bar(name="Spent",x=bdf["Cat"],y=bdf["Spent"],marker_color="#0ea472"))
        fig2.update_layout(**PL,title="Feb Budget vs Spend",title_font=dict(size=13,color="#111827"),barmode="overlay",height=200,xaxis=dict(gridcolor="rgba(0,0,0,.06)",tickfont=dict(size=10)),yaxis=dict(gridcolor="rgba(0,0,0,.06)"))
        st.plotly_chart(fig2,use_container_width=True)
    with c3:
        sc = pd.DataFrame([{"s":a.status} for a in st.session_state.assets]).groupby("s").size().reset_index(name="n")
        fig3 = px.pie(sc,values="n",names="s",color_discrete_sequence=["#0ea472","#f59e0b","#ef4444","#6b7280"],hole=0.6)
        fig3.update_layout(**PL,title="Assets",title_font=dict(size=13,color="#111827"),height=200,showlegend=False)
        fig3.update_traces(textinfo="none")
        st.plotly_chart(fig3,use_container_width=True)

    cl,cr = st.columns([3,2])
    with cl:
        st.markdown('<div style="font-size:13px;font-weight:600;color:#111827;margin-bottom:8px">Recent Work Orders</div>',unsafe_allow_html=True)
        rows = [f"<tr>{td_cell(w.id,mono=True,muted=True)}{td_cell(w.title,bold=True)}{badge_cell(pb(w.priority))}{badge_cell(sb(w.status))}{td_cell(w.assigned_to.split()[0],muted=True)}{td_cell(w.due_date,mono=True,muted=True)}</tr>"
                for w in sorted(st.session_state.work_orders,key=lambda x:x.created_date,reverse=True)[:6]]
        st.markdown(make_table(["ID","Title","Priority","Status","Who","Due"],rows),unsafe_allow_html=True)
    with cr:
        st.markdown('<div style="font-size:13px;font-weight:600;color:#111827;margin-bottom:8px">Inventory Levels</div>',unsafe_allow_html=True)
        h = '<div style="background:#ffffff;border:1px solid #e5e7eb;border-radius:14px;padding:16px 18px;box-shadow:0 1px 4px rgba(0,0,0,.05)">'
        for item in st.session_state.inventory:
            bar, _ = stock_bar(item.quantity, item.reorder_level)
            h += f'<div style="margin-bottom:13px"><div style="display:flex;justify-content:space-between;margin-bottom:4px"><span style="font-size:12px;color:#111827;font-weight:500">{item.name[:26]}</span><span style="font-size:11px;font-family:DM Mono,monospace;color:#6b7280">{item.quantity} {item.unit}</span></div>{bar}</div>'
        h += "</div>"
        st.markdown(h,unsafe_allow_html=True)

# ── ASSETS ───────────────────────────────────────────────────────────────────
def page_assets():
    section_header("Assets","Asset Management","Track, maintain, and analyse all facility equipment.")
    tab1,tab2,tab3 = st.tabs(["Registry","Add Asset","Analytics"])
    with tab1:
        sc1,sc2,sc3 = st.columns([3,1,1])
        q    = sc1.text_input("",placeholder="Search assets...",key="asq",label_visibility="collapsed").lower()
        sf   = sc2.multiselect("Status",STATUSES,key="asf")
        tf   = sc3.multiselect("Type",ASSET_TYPES,key="atf")
        data = st.session_state.assets
        if q:  data=[a for a in data if q in a.name.lower() or q in a.type.lower() or q in a.location.lower() or q in a.manufacturer.lower()]
        if sf: data=[a for a in data if a.status in sf]
        if tf: data=[a for a in data if a.type in tf]
        sc_map = {"Operational":"#0ea472","Maintenance Required":"#f59e0b","Out of Service":"#ef4444","Retired":"#6b7280"}
        sbg_map = {"Operational":"rgba(0,229,160,.1)","Maintenance Required":"rgba(245,158,11,.1)","Out of Service":"rgba(239,68,68,.1)","Retired":"rgba(255,255,255,.05)"}
        rows=[]
        for a in data:
            spill=f'<span style="background:{sbg_map.get(a.status,"")};color:{sc_map.get(a.status,"#9ca3af")};border-radius:20px;padding:3px 10px;font-size:11px;font-family:DM Mono,monospace">{a.status}</span>'
            rows.append(f"<tr>{td_cell(a.id,mono=True,muted=True)}{td_cell(a.name,bold=True)}{td_cell(a.type)}{td_cell(a.location,muted=True)}{badge_cell(spill)}{td_cell(f'${a.purchase_cost:,.0f}' if a.purchase_cost else '—',mono=True,color='#0ea472')}{td_cell(a.last_maintenance,mono=True,muted=True)}{td_cell(a.next_maintenance,mono=True)}</tr>")
        st.markdown(make_table(["ID","Name","Type","Location","Status","Cost","Last","Next"],rows),unsafe_allow_html=True)
        c1,_=st.columns([1,5])
        with c1: st.download_button("Export CSV",to_csv(st.session_state.assets,["id","name","type","location","status","purchase_date","last_maintenance","next_maintenance","manufacturer","model","serial_number","warranty_expiry","purchase_cost","notes"]),"assets.csv","text/csv",key="dl_a")
        with st.expander("View / Edit / Delete"):
            sel=st.selectbox("Asset",[a.id for a in st.session_state.assets],format_func=lambda x:next((a.name for a in st.session_state.assets if a.id==x),x),key="ased")
            asset=next((a for a in st.session_state.assets if a.id==sel),None)
            if asset:
                c1,c2=st.columns(2)
                with c1:
                    nn=st.text_input("Name",asset.name,key="aen"); nt_=st.selectbox("Type",ASSET_TYPES,index=ASSET_TYPES.index(asset.type) if asset.type in ASSET_TYPES else 0,key="aet")
                    nl=st.text_input("Location",asset.location,key="ael"); ns=st.selectbox("Status",STATUSES,index=STATUSES.index(asset.status),key="aes")
                    nc=st.number_input("Purchase Cost",0.0,9999999.0,float(asset.purchase_cost),500.0,key="aec")
                with c2:
                    nm=st.text_input("Manufacturer",asset.manufacturer,key="aem"); nmo=st.text_input("Model",asset.model,key="aemo")
                    nsn=st.text_input("Serial",asset.serial_number,key="aesn")
                    nlm=st.date_input("Last Maint",datetime.strptime(asset.last_maintenance,"%Y-%m-%d"),key="aelm")
                    nnm=st.date_input("Next Maint",datetime.strptime(asset.next_maintenance,"%Y-%m-%d"),key="aenm")
                nno=st.text_area("Notes",asset.notes,key="aeno")
                b1,b2,_=st.columns([1,1,4])
                with b1:
                    if st.button("Save",key="aesv"):
                        asset.name=nn;asset.type=nt_;asset.location=nl;asset.status=ns;asset.purchase_cost=nc
                        asset.manufacturer=nm;asset.model=nmo;asset.serial_number=nsn;asset.notes=nno
                        asset.last_maintenance=nlm.strftime("%Y-%m-%d");asset.next_maintenance=nnm.strftime("%Y-%m-%d")
                        add_notif(f"Asset '{asset.name}' updated","info");st.success("Saved!");st.rerun()
                with b2:
                    st.markdown('<div class="danger-btn">',unsafe_allow_html=True)
                    if st.button("Delete",key="aedl"):
                        st.session_state.assets=[a for a in st.session_state.assets if a.id!=sel]
                        add_notif(f"Asset '{asset.name}' deleted");st.success("Deleted.");st.rerun()
                    st.markdown("</div>",unsafe_allow_html=True)
    with tab2:
        with st.form("add_asset"):
            c1,c2=st.columns(2)
            with c1:
                aid=st.text_input("ID",f"AST{len(st.session_state.assets)+1:03d}"); aname=st.text_input("Name"); atype=st.selectbox("Type",ASSET_TYPES)
                aloc=st.text_input("Location"); astat=st.selectbox("Status",STATUSES); acost=st.number_input("Cost ($)",0.0,9999999.0,0.0)
            with c2:
                amfr=st.text_input("Manufacturer"); amod=st.text_input("Model"); asn=st.text_input("Serial")
                apd=st.date_input("Purchase Date",datetime.now()); alm=st.date_input("Last Maint",datetime.now())
                anm=st.date_input("Next Maint",datetime.now()+timedelta(days=90)); awe=st.date_input("Warranty",datetime.now()+timedelta(days=365))
            anotes=st.text_area("Notes")
            if st.form_submit_button("Add Asset"):
                if not aname: st.error("Name required")
                else:
                    st.session_state.assets.append(Asset(aid,aname,atype,aloc,astat,apd.strftime("%Y-%m-%d"),alm.strftime("%Y-%m-%d"),anm.strftime("%Y-%m-%d"),amfr,amod,asn,awe.strftime("%Y-%m-%d"),acost,anotes))
                    add_notif(f"Asset '{aname}' added","success");st.success("Added!");st.rerun()
    with tab3:
        c1,c2=st.columns(2)
        with c1:
            sc=pd.DataFrame([{"Status":a.status} for a in st.session_state.assets]).groupby("Status").size().reset_index(name="n")
            fig=px.pie(sc,values="n",names="Status",title="Asset Status",color_discrete_sequence=COLORS,hole=0.4)
            fig.update_layout(**PL,title_font=dict(size=13,color="#111827"));st.plotly_chart(fig,use_container_width=True)
        with c2:
            vdf=pd.DataFrame([{"Type":a.type,"Value":a.purchase_cost/1000} for a in st.session_state.assets]).groupby("Type").sum().reset_index()
            fig2=px.bar(vdf,x="Type",y="Value",title="Value by Type ($k)",color="Type",color_discrete_sequence=COLORS)
            fig2.update_layout(**PL,title_font=dict(size=13,color="#111827"),xaxis=dict(gridcolor="rgba(0,0,0,.06)"),yaxis=dict(gridcolor="rgba(0,0,0,.06)"));st.plotly_chart(fig2,use_container_width=True)
        fig3=go.Figure()
        for a in st.session_state.assets:
            fig3.add_trace(go.Scatter(x=[a.last_maintenance,a.next_maintenance],y=[a.name,a.name],mode="lines+markers",name=a.name,line=dict(width=3),marker=dict(size=10)))
        fig3.update_layout(**PL,title="Maintenance Timeline",title_font=dict(size=13,color="#111827"),height=280,xaxis=dict(gridcolor="rgba(0,0,0,.06)"),yaxis=dict(gridcolor="rgba(0,0,0,.06)"))
        st.plotly_chart(fig3,use_container_width=True)

# ── WORK ORDERS ──────────────────────────────────────────────────────────────
def page_work_orders():
    section_header("Work Orders","Work Order Management","Create, assign, track, and close maintenance tasks.")
    tab1,tab2,tab3=st.tabs(["All Orders","Create Order","Analytics"])
    with tab1:
        sc1,sc2,sc3=st.columns([3,1,1])
        q =sc1.text_input("",placeholder="Search work orders...",key="woq",label_visibility="collapsed").lower()
        sf=sc2.multiselect("Status",WO_STATUSES,default=["Open","In Progress"],key="wosf")
        pf=sc3.multiselect("Priority",PRIORITIES,key="wopf")
        wos=st.session_state.work_orders
        if q:  wos=[w for w in wos if q in w.title.lower() or q in w.assigned_to.lower() or q in w.asset_id.lower()]
        if sf: wos=[w for w in wos if w.status in sf]
        if pf: wos=[w for w in wos if w.priority in pf]
        rows=[f"<tr>{td_cell(w.id,mono=True,muted=True)}{td_cell(w.title,bold=True)}{badge_cell(pb(w.priority))}{badge_cell(sb(w.status))}{td_cell(w.assigned_to)}{td_cell(w.due_date,mono=True,muted=True)}{td_cell(f'{w.estimated_hours}h/{w.actual_hours}h',mono=True,muted=True)}{td_cell(f'${w.cost:.0f}' if w.cost else '—',mono=True,color='#0ea472' if w.cost else None)}</tr>" for w in wos]
        st.markdown(make_table(["ID","Title","Priority","Status","Assigned","Due","Est/Act","Cost"],rows),unsafe_allow_html=True)
        c1,_=st.columns([1,5])
        with c1: st.download_button("Export CSV",to_csv(st.session_state.work_orders,["id","title","asset_id","priority","status","created_date","due_date","assigned_to","estimated_hours","actual_hours","cost","notes"]),"work_orders.csv","text/csv",key="dl_wo")
        with st.expander("Edit / Update"):
            sel=st.selectbox("Work Order",[w.id for w in st.session_state.work_orders],format_func=lambda x:next((w.title for w in st.session_state.work_orders if w.id==x),x),key="woed")
            wo=next((w for w in st.session_state.work_orders if w.id==sel),None)
            if wo:
                c1,c2,c3=st.columns(3)
                ns=c1.selectbox("Status",WO_STATUSES,index=WO_STATUSES.index(wo.status),key="woes")
                np_=c2.selectbox("Priority",PRIORITIES,index=PRIORITIES.index(wo.priority),key="woep")
                snames=[s.name for s in st.session_state.staff]
                na=c3.selectbox("Assigned To",snames,index=snames.index(wo.assigned_to) if wo.assigned_to in snames else 0,key="woea")
                c4,c5,c6=st.columns(3)
                ah=c4.number_input("Actual Hours",0.0,200.0,float(wo.actual_hours),.5,key="woeah")
                co=c5.number_input("Cost ($)",0.0,99999.0,float(wo.cost),10.0,key="woeco")
                dd=c6.date_input("Due Date",datetime.strptime(wo.due_date,"%Y-%m-%d"),key="woedd")
                nt=st.text_area("Notes",wo.notes,key="woent")
                b1,b2,_=st.columns([1,1,4])
                with b1:
                    if st.button("Save",key="woesv"):
                        wo.status=ns;wo.priority=np_;wo.assigned_to=na;wo.actual_hours=ah;wo.cost=co;wo.notes=nt;wo.due_date=dd.strftime("%Y-%m-%d")
                        add_notif(f"WO {wo.id} updated","info");st.success("Saved!");st.rerun()
                with b2:
                    st.markdown('<div class="danger-btn">',unsafe_allow_html=True)
                    if st.button("Delete",key="woedl"):
                        st.session_state.work_orders=[w for w in st.session_state.work_orders if w.id!=sel]
                        add_notif(f"WO {sel} deleted");st.success("Deleted.");st.rerun()
                    st.markdown("</div>",unsafe_allow_html=True)
    with tab2:
        with st.form("cwo"):
            c1,c2=st.columns(2)
            with c1:
                wid=st.text_input("ID",f"WO{len(st.session_state.work_orders)+1:03d}"); wt=st.text_input("Title")
                wa=st.selectbox("Asset",[a.id for a in st.session_state.assets],format_func=lambda x:next((a.name for a in st.session_state.assets if a.id==x),x)); wp=st.selectbox("Priority",PRIORITIES)
            with c2:
                avail=[s.name for s in st.session_state.staff if s.availability=="Available"]
                wass=st.selectbox("Assign To",avail if avail else ["No staff available"]); wdd=st.date_input("Due",datetime.now()+timedelta(days=7)); weh=st.number_input("Est Hours",.5,200.0,2.0,.5)
            wd=st.text_area("Description"); wn=st.text_area("Notes")
            if st.form_submit_button("Create Work Order"):
                if not wt: st.error("Title required")
                else:
                    st.session_state.work_orders.append(WorkOrder(wid,wt,wd,wa,wp,"Open",datetime.now().strftime("%Y-%m-%d"),wdd.strftime("%Y-%m-%d"),wass,weh,notes=wn))
                    add_notif(f"WO '{wt}' created","success");st.success("Created!");st.rerun()
    with tab3:
        c1,c2=st.columns(2)
        with c1:
            sc=pd.DataFrame([{"Status":w.status} for w in st.session_state.work_orders]).groupby("Status").size().reset_index(name="n")
            fig=px.bar(sc,x="Status",y="n",title="By Status",color="Status",color_discrete_sequence=COLORS)
            fig.update_layout(**PL,title_font=dict(size=13,color="#111827"),xaxis=dict(gridcolor="rgba(0,0,0,.06)"),yaxis=dict(gridcolor="rgba(0,0,0,.06)"));st.plotly_chart(fig,use_container_width=True)
        with c2:
            pc=pd.DataFrame([{"Priority":w.priority} for w in st.session_state.work_orders]).groupby("Priority").size().reset_index(name="n")
            fig2=px.pie(pc,values="n",names="Priority",title="By Priority",color_discrete_sequence=["#ef4444","#f59e0b","#0ea472"],hole=0.4)
            fig2.update_layout(**PL,title_font=dict(size=13,color="#111827"));st.plotly_chart(fig2,use_container_width=True)
        done=[w for w in st.session_state.work_orders if w.status=="Completed" and w.actual_hours>0]
        if done:
            df=pd.DataFrame([{"ID":w.id,"Est":w.estimated_hours,"Act":w.actual_hours} for w in done])
            fig3=go.Figure()
            fig3.add_trace(go.Bar(name="Est",x=df["ID"],y=df["Est"],marker_color=COLORS[1]))
            fig3.add_trace(go.Bar(name="Act",x=df["ID"],y=df["Act"],marker_color=COLORS[0]))
            fig3.update_layout(**PL,title="Est vs Actual Hours",title_font=dict(size=13,color="#111827"),barmode="group",xaxis=dict(gridcolor="rgba(0,0,0,.06)"),yaxis=dict(gridcolor="rgba(0,0,0,.06)"))
            st.plotly_chart(fig3,use_container_width=True)

# ── STAFF ────────────────────────────────────────────────────────────────────
def page_staff():
    section_header("Staff","Staff Management","Manage technicians, skills, and availability.")
    tab1,tab2=st.tabs(["Team Directory","Add Member"])
    with tab1:
        c1,c2=st.columns([3,1])
        q=c1.text_input("",placeholder="Search staff...",key="stq",label_visibility="collapsed").lower()
        af=c2.multiselect("Availability",AVAIL_LIST,key="staf")
        staff=st.session_state.staff
        if q: staff=[s for s in staff if q in s.name.lower() or q in s.role.lower() or any(q in sk.lower() for sk in s.skills)]
        if af: staff=[s for s in staff if s.availability in af]
        IC={"John Smith":"#059669","Mike Johnson":"#b45309","Sarah Williams":"#1d4ed8","Carlos Reyes":"#7c3aed","Amara Osei":"#be185d"}
        cols=st.columns(3)
        for i,s in enumerate(staff):
            ic=IC.get(s.name,"#9ca3af"); ini="".join([n[0] for n in s.name.split()][:2])
            skh="".join(f'<span style="background:#f3f4f6;color:#64748b;border-radius:6px;padding:2px 8px;font-size:10px;margin:2px;display:inline-block">{sk}</span>' for sk in s.skills)
            with cols[i%3]:
                st.markdown(f'''<div style="background:#ffffff;border:1px solid #e5e7eb;border-radius:14px;padding:20px;margin-bottom:16px">
                  <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px">
                    <div style="width:44px;height:44px;border-radius:50%;background:{ic};display:flex;align-items:center;justify-content:center;font-size:15px;font-weight:700;color:#fff;flex-shrink:0">{ini}</div>
                    <div style="flex:1"><div style="font-size:14px;font-weight:600;color:#0f172a">{s.name}</div><div style="font-size:11px;color:#6b7280">{s.role} &middot; {s.department}</div></div>
                    <div>{avb(s.availability)}</div>
                  </div>
                  <div style="margin-bottom:12px">{skh}</div>
                  <div style="display:flex;justify-content:space-between;padding-top:10px;border-top:1px solid #f3f4f6">
                    <div><div style="font-size:11px;color:#6b7280">&#128231; {s.email}</div><div style="font-size:11px;color:#64748b;margin-top:2px">&#128222; {s.phone}</div></div>
                    <div style="font-size:16px;font-family:DM Mono,monospace;color:#0ea472;font-weight:600">${s.hourly_rate}<span style="font-size:11px;color:#6b7280">/hr</span></div>
                  </div></div>''',unsafe_allow_html=True)
        with st.expander("Edit / Delete"):
            sel=st.selectbox("Select",[s.id for s in st.session_state.staff],format_func=lambda x:next((s.name for s in st.session_state.staff if s.id==x),x),key="sted")
            sm=next((s for s in st.session_state.staff if s.id==sel),None)
            if sm:
                c1,c2=st.columns(2)
                with c1:
                    snn=st.text_input("Name",sm.name,key="sen"); snr=st.text_input("Role",sm.role,key="ser")
                    snd=st.selectbox("Dept",DEPARTMENTS,index=DEPARTMENTS.index(sm.department) if sm.department in DEPARTMENTS else 0,key="sed2")
                with c2:
                    sne=st.text_input("Email",sm.email,key="see"); snp=st.text_input("Phone",sm.phone,key="sep")
                    snr2=st.number_input("Rate",15.0,200.0,float(sm.hourly_rate),5.0,key="ser2"); snav=st.selectbox("Availability",AVAIL_LIST,index=AVAIL_LIST.index(sm.availability),key="seav")
                snsk=st.multiselect("Skills",SKILLS_LIST,default=sm.skills,key="sesk")
                b1,b2,_=st.columns([1,1,4])
                with b1:
                    if st.button("Save",key="sesv"):
                        sm.name=snn;sm.role=snr;sm.department=snd;sm.email=sne;sm.phone=snp;sm.hourly_rate=snr2;sm.availability=snav;sm.skills=snsk
                        add_notif(f"'{sm.name}' updated","info");st.success("Saved!");st.rerun()
                with b2:
                    st.markdown('<div class="danger-btn">',unsafe_allow_html=True)
                    if st.button("Delete",key="sedl"):
                        st.session_state.staff=[s for s in st.session_state.staff if s.id!=sel]
                        add_notif(f"'{sm.name}' removed");st.success("Deleted.");st.rerun()
                    st.markdown("</div>",unsafe_allow_html=True)
        c1,_=st.columns([1,5])
        with c1: st.download_button("Export CSV",to_csv(st.session_state.staff,["id","name","role","department","email","phone","availability","hourly_rate"]),"staff.csv","text/csv",key="dl_st")
    with tab2:
        with st.form("ast"):
            c1,c2=st.columns(2)
            with c1:
                sid=st.text_input("ID",f"STF{len(st.session_state.staff)+1:03d}"); sname=st.text_input("Full Name"); srole=st.text_input("Role"); sdept=st.selectbox("Dept",DEPARTMENTS)
            with c2:
                semail=st.text_input("Email"); sphone=st.text_input("Phone"); srate=st.number_input("Rate ($)",15.0,200.0,35.0,5.0); savail=st.selectbox("Availability",AVAIL_LIST)
            sskills=st.multiselect("Skills",SKILLS_LIST)
            if st.form_submit_button("Add Member"):
                if not sname: st.error("Name required")
                else:
                    st.session_state.staff.append(Staff(sid,sname,srole,sdept,semail,sphone,sskills,savail,srate))
                    add_notif(f"'{sname}' added","success");st.success("Added!");st.rerun()

# ── INVENTORY ────────────────────────────────────────────────────────────────
def page_inventory():
    section_header("Inventory","Inventory Management","Track parts, supplies, stock levels and reorder needs.")
    tab1,tab2,tab3=st.tabs(["Stock Levels","Add Item","Analytics"])
    with tab1:
        low=[i for i in st.session_state.inventory if i.quantity<=i.reorder_level]
        if low: st.warning(f"\u26a0\ufe0f **{len(low)} item(s)** below reorder level.")
        c1,c2=st.columns([3,1])
        q=c1.text_input("",placeholder="Search inventory...",key="invq",label_visibility="collapsed").lower()
        cf=c2.multiselect("Category",INV_CATS,key="invcf")
        items=st.session_state.inventory
        if q: items=[i for i in items if q in i.name.lower() or q in i.category.lower() or q in i.supplier.lower()]
        if cf: items=[i for i in items if i.category in cf]
        rows=[]
        for item in items:
            at_low=item.quantity<=item.reorder_level
            bar,bc=stock_bar(item.quantity,item.reorder_level)
            flag=' <span style="background:rgba(239,68,68,.12);color:#f87171;border-radius:4px;padding:1px 6px;font-size:10px">LOW</span>' if at_low else ""
            nc=f'<td style="padding:12px 14px;border-bottom:1px solid #f3f4f6"><div style="font-size:13px;color:#111827;font-weight:500">{item.name}{flag}</div>{bar}</td>'
            rows.append(f"<tr>{td_cell(item.id,mono=True,muted=True)}{nc}{td_cell(item.category)}{td_cell(str(item.quantity),mono=True,color=bc)}{td_cell(item.unit,muted=True)}{td_cell(str(item.reorder_level),mono=True,muted=True)}{td_cell(item.supplier,muted=True)}{td_cell(f'${item.unit_cost}',mono=True)}{td_cell(f'${item.quantity*item.unit_cost:,.0f}',mono=True,color='#0ea472')}</tr>")
        st.markdown(make_table(["ID","Item","Cat","Qty","Unit","Reorder","Supplier","Unit $","Total"],rows),unsafe_allow_html=True)
        c1,_=st.columns([1,5])
        with c1: st.download_button("Export CSV",to_csv(st.session_state.inventory,["id","name","category","quantity","unit","reorder_level","supplier","unit_cost","location","last_ordered"]),"inventory.csv","text/csv",key="dl_inv")
        with st.expander("Edit / Restock / Delete"):
            sel=st.selectbox("Item",[i.id for i in st.session_state.inventory],format_func=lambda x:next((i.name for i in st.session_state.inventory if i.id==x),x),key="ined")
            inv=next((i for i in st.session_state.inventory if i.id==sel),None)
            if inv:
                c1,c2,c3=st.columns(3)
                nq=c1.number_input("Qty",0,99999,inv.quantity,1,key="ineq"); nrl=c2.number_input("Reorder Lvl",0,99999,inv.reorder_level,1,key="inerl"); nuc=c3.number_input("Unit Cost",0.0,99999.0,float(inv.unit_cost),.5,key="ineuc")
                ns=st.text_input("Supplier",inv.supplier,key="ines")
                b1,b2,_=st.columns([1,1,4])
                with b1:
                    if st.button("Save",key="inesv"):
                        inv.quantity=nq;inv.reorder_level=nrl;inv.unit_cost=nuc;inv.supplier=ns
                        add_notif(f"'{inv.name}' updated","info");st.success("Saved!");st.rerun()
                with b2:
                    st.markdown('<div class="danger-btn">',unsafe_allow_html=True)
                    if st.button("Delete",key="inedl"):
                        st.session_state.inventory=[i for i in st.session_state.inventory if i.id!=sel]
                        add_notif(f"'{inv.name}' removed");st.success("Deleted.");st.rerun()
                    st.markdown("</div>",unsafe_allow_html=True)
    with tab2:
        with st.form("ainv"):
            c1,c2=st.columns(2)
            with c1:
                iid=st.text_input("ID",f"INV{len(st.session_state.inventory)+1:03d}"); iname=st.text_input("Name"); icat=st.selectbox("Category",INV_CATS); iqty=st.number_input("Qty",0,99999,0); iunit=st.text_input("Unit")
            with c2:
                irl=st.number_input("Reorder Lvl",0,99999,10); isup=st.text_input("Supplier"); iuc=st.number_input("Unit Cost",0.0,99999.0,0.0,.5); iloc=st.text_input("Location")
            ilo=st.date_input("Last Ordered",datetime.now())
            if st.form_submit_button("Add Item"):
                if not iname: st.error("Name required")
                else:
                    st.session_state.inventory.append(Inventory(iid,iname,icat,iqty,iunit,irl,isup,iuc,iloc,ilo.strftime("%Y-%m-%d")))
                    add_notif(f"'{iname}' added","success");st.success("Added!");st.rerun()
    with tab3:
        c1,c2=st.columns(2)
        with c1:
            df=pd.DataFrame([{"Cat":i.category,"Val":i.quantity*i.unit_cost} for i in st.session_state.inventory]).groupby("Cat").sum().reset_index()
            fig=px.pie(df,values="Val",names="Cat",title="Value by Category",color_discrete_sequence=COLORS,hole=0.4)
            fig.update_layout(**PL,title_font=dict(size=13,color="#111827"));st.plotly_chart(fig,use_container_width=True)
        with c2:
            df2=pd.DataFrame([{"Item":i.name.split()[0],"Qty":i.quantity,"Reorder":i.reorder_level} for i in st.session_state.inventory])
            fig2=go.Figure()
            fig2.add_trace(go.Bar(name="Qty",x=df2["Item"],y=df2["Qty"],marker_color=COLORS[0]))
            fig2.add_trace(go.Bar(name="Reorder",x=df2["Item"],y=df2["Reorder"],marker_color=COLORS[3]))
            fig2.update_layout(**PL,title="Stock vs Reorder",barmode="group",title_font=dict(size=13,color="#111827"),xaxis=dict(gridcolor="rgba(0,0,0,.06)"),yaxis=dict(gridcolor="rgba(0,0,0,.06)"));st.plotly_chart(fig2,use_container_width=True)

# ── VENDORS ──────────────────────────────────────────────────────────────────
def page_vendors():
    section_header("Vendors","Vendor Management","Track suppliers, contracts, ratings, and contacts.")
    tab1,tab2=st.tabs(["Directory","Add Vendor"])
    with tab1:
        c1,c2=st.columns([3,1])
        q=c1.text_input("",placeholder="Search vendors...",key="venq",label_visibility="collapsed").lower()
        cf=c2.multiselect("Category",DEPARTMENTS,key="vencf")
        vens=st.session_state.vendors
        if q: vens=[v for v in vens if q in v.name.lower() or q in v.contact_name.lower() or q in v.category.lower()]
        if cf: vens=[v for v in vens if v.category in cf]
        today=datetime.now().date()
        cols=st.columns(3)
        for i,v in enumerate(vens):
            ct=datetime.strptime(v.contract_end,"%Y-%m-%d").date(); dl=(ct-today).days
            ec="#ef4444" if dl<60 else ("#f59e0b" if dl<180 else "#0ea472")
            el="EXPIRING" if dl<60 else (f"{dl}d left" if dl<180 else f"{dl//30}mo left")
            with cols[i%3]:
                st.markdown(f'''<div style="background:#ffffff;border:1px solid #e5e7eb;border-radius:14px;padding:20px;margin-bottom:16px">
                  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px">
                    <div><div style="font-size:14px;font-weight:600;color:#0f172a">{v.name}</div><div style="font-size:11px;color:#6b7280">{v.category}</div></div>
                    <div style="color:#f59e0b;font-size:16px">{"&#9733;"*int(v.rating)}{"&#9734;"*(5-int(v.rating))}</div>
                  </div>
                  <div style="font-size:12px;color:#64748b;margin-bottom:3px">&#128100; {v.contact_name}</div>
                  <div style="font-size:12px;color:#64748b;margin-bottom:3px">&#128231; {v.email}</div>
                  <div style="font-size:12px;color:#64748b;margin-bottom:12px">&#128222; {v.phone}</div>
                  <div style="display:flex;justify-content:space-between;align-items:center;padding-top:10px;border-top:1px solid #f3f4f6">
                    <div style="font-size:11px;color:#6b7280">Ends {v.contract_end}</div>
                    <span style="color:{ec};font-size:10px;font-family:DM Mono,monospace">{el}</span>
                  </div>{("<div style=\'font-size:11px;color:#64748b;margin-top:6px\'>" + v.notes + "</div>") if v.notes else ""}
                </div>''',unsafe_allow_html=True)
        with st.expander("Edit / Delete"):
            sel=st.selectbox("Vendor",[v.id for v in st.session_state.vendors],format_func=lambda x:next((v.name for v in st.session_state.vendors if v.id==x),x),key="vned")
            vn=next((v for v in st.session_state.vendors if v.id==sel),None)
            if vn:
                c1,c2=st.columns(2)
                with c1:
                    vnn=st.text_input("Name",vn.name,key="ven"); vnc=st.selectbox("Cat",DEPARTMENTS,index=DEPARTMENTS.index(vn.category) if vn.category in DEPARTMENTS else 0,key="venc")
                    vncn=st.text_input("Contact",vn.contact_name,key="vencn"); vne=st.text_input("Email",vn.email,key="vene")
                with c2:
                    vnp=st.text_input("Phone",vn.phone,key="venp"); vnr=st.number_input("Rating",1.0,5.0,float(vn.rating),.1,key="venr")
                    vnce=st.date_input("Contract End",datetime.strptime(vn.contract_end,"%Y-%m-%d"),key="vence")
                vnnt=st.text_area("Notes",vn.notes,key="vennt")
                b1,b2,_=st.columns([1,1,4])
                with b1:
                    if st.button("Save",key="vensv"):
                        vn.name=vnn;vn.category=vnc;vn.contact_name=vncn;vn.email=vne;vn.phone=vnp;vn.rating=vnr;vn.contract_end=vnce.strftime("%Y-%m-%d");vn.notes=vnnt
                        add_notif(f"'{vn.name}' updated","info");st.success("Saved!");st.rerun()
                with b2:
                    st.markdown('<div class="danger-btn">',unsafe_allow_html=True)
                    if st.button("Delete",key="vendl"):
                        st.session_state.vendors=[v for v in st.session_state.vendors if v.id!=sel]
                        add_notif(f"'{vn.name}' removed");st.success("Deleted.");st.rerun()
                    st.markdown("</div>",unsafe_allow_html=True)
        c1,_=st.columns([1,5])
        with c1: st.download_button("Export CSV",to_csv(st.session_state.vendors,["id","name","category","contact_name","email","phone","address","rating","contract_end","notes"]),"vendors.csv","text/csv",key="dl_ven")
    with tab2:
        with st.form("aven"):
            c1,c2=st.columns(2)
            with c1:
                vid=st.text_input("ID",f"VEN{len(st.session_state.vendors)+1:03d}"); vname=st.text_input("Name"); vcat=st.selectbox("Category",DEPARTMENTS); vcn=st.text_input("Contact Name"); vem=st.text_input("Email")
            with c2:
                vph=st.text_input("Phone"); vaddr=st.text_input("Address"); vrat=st.number_input("Rating",1.0,5.0,4.0,.1); vce=st.date_input("Contract End",datetime.now()+timedelta(days=365))
            vnt=st.text_area("Notes")
            if st.form_submit_button("Add Vendor"):
                if not vname: st.error("Name required")
                else:
                    st.session_state.vendors.append(Vendor(vid,vname,vcat,vcn,vem,vph,vaddr,vrat,vce.strftime("%Y-%m-%d"),vnt))
                    add_notif(f"Vendor '{vname}' added","success");st.success("Added!");st.rerun()

# ── BUDGETS ──────────────────────────────────────────────────────────────────
def page_budgets():
    section_header("Budget","Budget & Cost Tracking","Monitor spend vs. allocation across categories and months.")
    months={1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun"}
    sm=st.selectbox("View Month",list(months.values()),index=1)
    mn={v:k for k,v in months.items()}[sm]
    mb=[b for b in st.session_state.budgets if b.month==mn]
    ta=sum(b.allocated for b in mb); ts=sum(b.spent for b in mb); rem=ta-ts; pu=ts/ta*100 if ta else 0
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Budget",f"${ta:,.0f}"); c2.metric("Spent",f"${ts:,.0f}",f"{pu:.0f}% used"); c3.metric("Remaining",f"${rem:,.0f}"); c4.metric("Categories",len(mb))
    st.markdown("<div style='height:14px'></div>",unsafe_allow_html=True)
    c1,c2=st.columns([2,3])
    with c1:
        brows=""
        for b in sorted(mb,key=lambda x:x.spent,reverse=True):
            pct=min(100,b.spent/max(b.allocated,1)*100); bc="#0ea472" if pct<80 else ("#f59e0b" if pct<100 else "#ef4444")
            over=" <span style=\'color:#ef4444;font-size:10px\'>OVER</span>" if pct>=100 else ""
            brows+=f'''<div style="background:#f9fafb;border:1px solid #e5e7eb;border-radius:10px;padding:14px;margin-bottom:8px">
              <div style="display:flex;justify-content:space-between;margin-bottom:7px"><div style="font-size:13px;font-weight:600;color:#0f172a">{b.category}{over}</div><div style="font-size:11px;font-family:DM Mono,monospace;color:#64748b">${b.spent:,.0f} / ${b.allocated:,.0f}</div></div>
              <div style="height:5px;background:#e5e7eb;border-radius:4px"><div style="height:100%;width:{min(pct,100):.0f}%;background:{bc};border-radius:4px"></div></div>
              <div style="font-size:10px;color:#64748b;margin-top:4px;font-family:DM Mono,monospace">{pct:.0f}% &middot; ${max(b.allocated-b.spent,0):,.0f} left</div></div>'''
        st.markdown(f'<div style="background:#ffffff;border:1px solid #e5e7eb;border-radius:14px;padding:16px">{brows}</div>',unsafe_allow_html=True)
    with c2:
        td_=[]; 
        for mn2,ml in months.items():
            mb2=[b for b in st.session_state.budgets if b.month==mn2]
            if mb2: td_.append({"Month":ml,"Allocated":sum(b.allocated for b in mb2),"Spent":sum(b.spent for b in mb2)})
        if td_:
            tdf=pd.DataFrame(td_)
            fig=go.Figure()
            fig.add_trace(go.Bar(name="Budget",x=tdf["Month"],y=tdf["Allocated"],marker_color="rgba(59,130,246,.35)"))
            fig.add_trace(go.Bar(name="Spent",x=tdf["Month"],y=tdf["Spent"],marker_color="#0ea472"))
            fig.update_layout(**PL,title="6-Month Trend",title_font=dict(size=13,color="#111827"),barmode="overlay",xaxis=dict(gridcolor="rgba(0,0,0,.06)"),yaxis=dict(gridcolor="rgba(0,0,0,.06)"))
            st.plotly_chart(fig,use_container_width=True)
        fig2=px.pie(pd.DataFrame([{"Cat":b.category,"Spent":b.spent} for b in mb]),values="Spent",names="Cat",title=f"{sm} Spend by Category",color_discrete_sequence=COLORS,hole=0.4)
        fig2.update_layout(**PL,title_font=dict(size=13,color="#111827"));st.plotly_chart(fig2,use_container_width=True)

# ── REPORTS ──────────────────────────────────────────────────────────────────
def page_reports():
    section_header("Analytics","Reports & Analytics","Comprehensive data-driven facility insights.")
    rtype=st.selectbox("Report",["Executive Summary","Maintenance Report","Cost Analysis","Asset Performance","Staff Utilisation"])
    if rtype=="Executive Summary":
        op=sum(1 for a in st.session_state.assets if a.status=="Operational"); tot=len(st.session_state.assets)
        dp=len([w for w in st.session_state.work_orders if w.status=="Completed"])/max(len(st.session_state.work_orders),1)*100
        labor=sum(w.actual_hours*next((s.hourly_rate for s in st.session_state.staff if s.name==w.assigned_to),35) for w in st.session_state.work_orders if w.actual_hours>0)
        c1,c2,c3,c4=st.columns(4)
        c1.metric("Asset Health",f"{int(op/max(tot,1)*100)}%",f"{op}/{tot} operational"); c2.metric("WO Completion",f"{dp:.0f}%")
        c3.metric("Inventory Value",f"${sum(i.quantity*i.unit_cost for i in st.session_state.inventory):,.0f}"); c4.metric("Total Labor",f"${labor:,.0f}")
        c1,c2=st.columns(2)
        with c1:
            sc=pd.DataFrame([{"s":a.status} for a in st.session_state.assets]).groupby("s").size().reset_index(name="n")
            fig=px.pie(sc,values="n",names="s",title="Asset Health",color_discrete_sequence=COLORS,hole=0.4)
            fig.update_layout(**PL,title_font=dict(size=13,color="#111827"));st.plotly_chart(fig,use_container_width=True)
        with c2:
            wsc=pd.DataFrame([{"s":w.status} for w in st.session_state.work_orders]).groupby("s").size().reset_index(name="n")
            fig2=px.bar(wsc,x="s",y="n",title="Work Orders",color="s",color_discrete_sequence=COLORS)
            fig2.update_layout(**PL,title_font=dict(size=13,color="#111827"),xaxis=dict(gridcolor="rgba(0,0,0,.06)"),yaxis=dict(gridcolor="rgba(0,0,0,.06)"));st.plotly_chart(fig2,use_container_width=True)
    elif rtype=="Maintenance Report":
        today=datetime.now().date()
        for a in st.session_state.assets:
            d=datetime.strptime(a.next_maintenance,"%Y-%m-%d").date(); diff=(d-today).days
            if diff<0: st.error(f"\U0001f534 **OVERDUE: {a.name}** — was due {a.next_maintenance}")
            elif diff<=7: st.warning(f"\U0001f7e1 **URGENT: {a.name}** — due in {diff} days")
            elif diff<=30: st.info(f"\U0001f535 **{a.name}** — due in {diff} days")
        done=[w for w in st.session_state.work_orders if w.status=="Completed"]
        if done:
            st.markdown('<div style="font-size:14px;font-weight:600;color:#111827;margin:18px 0 10px">Completed Work Orders</div>',unsafe_allow_html=True)
            st.dataframe(pd.DataFrame([{"WO":w.id,"Title":w.title,"Asset":w.asset_id,"Assigned":w.assigned_to,"Hours":w.actual_hours,"Cost":f"${w.cost:.0f}"} for w in done]),use_container_width=True,hide_index=True)
    elif rtype=="Cost Analysis":
        labor=sum(w.actual_hours*next((s.hourly_rate for s in st.session_state.staff if s.name==w.assigned_to),35) for w in st.session_state.work_orders if w.actual_hours>0)
        parts=sum(w.cost for w in st.session_state.work_orders); inv_v=sum(i.quantity*i.unit_cost for i in st.session_state.inventory)
        c1,c2,c3=st.columns(3)
        c1.metric("Labor",f"${labor:,.2f}"); c2.metric("Parts",f"${parts:,.2f}"); c3.metric("Inventory",f"${inv_v:,.2f}")
        acd={}
        for w in st.session_state.work_orders: acd[w.asset_id]=acd.get(w.asset_id,0)+w.cost
        df=pd.DataFrame([{"Asset":k,"Cost":v} for k,v in acd.items()])
        fig=px.bar(df,x="Asset",y="Cost",title="Cost by Asset",color="Cost",color_continuous_scale=["#111318","#0ea472"])
        fig.update_layout(**PL,title_font=dict(size=13,color="#111827"),xaxis=dict(gridcolor="rgba(0,0,0,.06)"),yaxis=dict(gridcolor="rgba(0,0,0,.06)"));st.plotly_chart(fig,use_container_width=True)
    elif rtype=="Asset Performance":
        df=pd.DataFrame([{"Asset":a.name[:22],"Days":(datetime.now().date()-datetime.strptime(a.last_maintenance,"%Y-%m-%d").date()).days,"Status":a.status} for a in st.session_state.assets])
        fig=px.bar(df,x="Asset",y="Days",title="Days Since Last Maintenance",color="Status",color_discrete_map={"Operational":"#0ea472","Maintenance Required":"#f59e0b","Out of Service":"#ef4444","Retired":"#6b7280"})
        fig.update_layout(**PL,title_font=dict(size=13,color="#111827"),xaxis=dict(gridcolor="rgba(0,0,0,.06)"),yaxis=dict(gridcolor="rgba(0,0,0,.06)"));st.plotly_chart(fig,use_container_width=True)
    elif rtype=="Staff Utilisation":
        util=[{"Name":s.name,"Role":s.role,"WOs":len([w for w in st.session_state.work_orders if w.assigned_to==s.name]),"Hours":sum(w.actual_hours for w in st.session_state.work_orders if w.assigned_to==s.name),"Cost":f"${sum(w.actual_hours for w in st.session_state.work_orders if w.assigned_to==s.name)*s.hourly_rate:,.0f}","Rate":f"${s.hourly_rate}/hr","Status":s.availability} for s in st.session_state.staff]
        st.dataframe(pd.DataFrame(util),use_container_width=True,hide_index=True)
        hdf=pd.DataFrame([{"Name":s.name,"Hours":sum(w.actual_hours for w in st.session_state.work_orders if w.assigned_to==s.name)} for s in st.session_state.staff])
        fig=px.bar(hdf,x="Name",y="Hours",title="Hours by Technician",color="Name",color_discrete_sequence=COLORS)
        fig.update_layout(**PL,title_font=dict(size=13,color="#111827"),xaxis=dict(gridcolor="rgba(0,0,0,.06)"),yaxis=dict(gridcolor="rgba(0,0,0,.06)"));st.plotly_chart(fig,use_container_width=True)

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
def sidebar():
    with st.sidebar:
        st.markdown('''<div style="padding:4px 4px 20px">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px">
            <div style="width:32px;height:32px;background:linear-gradient(135deg,#0ea472,#3b82f6);border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:16px">&#127962;</div>
            <span style="font-family:'DM Serif Display',serif;font-size:20px;color:#111827!important">FacilityOS</span>
          </div>
          <div style="display:flex;align-items:center;gap:6px;margin-left:42px">
            <div style="width:6px;height:6px;border-radius:50%;background:#0ea472;box-shadow:0 0 6px #0ea472;animation:pulse 2s infinite"></div>
            <span style="font-size:11px;color:#64748b;font-family:'DM Mono',monospace;color:#8b95a8">v3.0 &middot; Online</span>
          </div></div>''',unsafe_allow_html=True)
        page=st.selectbox("Nav",["Dashboard","Assets","Work Orders","Staff","Inventory","Vendors","Budget","Reports"],label_visibility="collapsed")
        st.markdown("---")
        alerts=maintenance_alerts()
        if alerts:
            st.markdown('<div style="font-size:10px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:#64748b;margin-bottom:8px">Alerts</div>',unsafe_allow_html=True)
            for typ,name,sub in alerts[:5]:
                short=name[:20]
                if typ=="overdue": st.error(f"**OVR** {short}")
                elif typ=="urgent": st.warning(f"**URG** {short}")
                else: st.info(f"**UPC** {short}")
        st.markdown("---")
        iv=sum(i.quantity*i.unit_cost for i in st.session_state.inventory)
        av=sum(a.purchase_cost for a in st.session_state.assets)
        ow=sum(1 for w in st.session_state.work_orders if w.status in ("Open","In Progress"))
        li=sum(1 for i in st.session_state.inventory if i.quantity<=i.reorder_level)
        st.markdown(f'''<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px">
          <div style="background:#f9fafb;border:1px solid #e5e7eb;border-radius:10px;padding:10px"><div style="font-size:9px;color:#64748b;text-transform:uppercase;letter-spacing:.08em">Open WOs</div><div style="font-size:20px;font-family:DM Mono,monospace;color:{"#ef4444" if ow>3 else "#f59e0b" if ow>0 else "#0ea472"};margin-top:2px">{ow}</div></div>
          <div style="background:#f9fafb;border:1px solid #e5e7eb;border-radius:10px;padding:10px"><div style="font-size:9px;color:#64748b;text-transform:uppercase;letter-spacing:.08em">Low Stock</div><div style="font-size:20px;font-family:DM Mono,monospace;color:{"#ef4444" if li>0 else "#0ea472"};margin-top:2px">{li}</div></div>
        </div>
        <div style="background:#f9fafb;border:1px solid #e5e7eb;border-radius:10px;padding:10px;margin-bottom:8px"><div style="font-size:9px;color:#64748b;text-transform:uppercase;letter-spacing:.08em">Inventory Value</div><div style="font-size:17px;font-family:DM Mono,monospace;color:#0ea472;margin-top:2px">${iv:,.0f}</div></div>
        <div style="background:#f9fafb;border:1px solid #e5e7eb;border-radius:10px;padding:10px"><div style="font-size:9px;color:#64748b;text-transform:uppercase;letter-spacing:.08em">Asset Portfolio</div><div style="font-size:17px;font-family:DM Mono,monospace;color:#3b82f6;margin-top:2px">${av/1000:.0f}k</div></div>''',unsafe_allow_html=True)
        if st.session_state.notifs:
            st.markdown("---")
            st.markdown('<div style="font-size:10px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:#64748b;margin-bottom:8px">Activity</div>',unsafe_allow_html=True)
            for n in st.session_state.notifs[:6]:
                icon="✅" if n["type"]=="success" else "ℹ️"
                st.markdown(f'<div style="font-size:11px;color:#64748b;padding:5px 0;border-bottom:1px solid #f3f4f6">{icon} {n["msg"]} <span style="color:#9ca3af;font-size:10px;font-family:DM Mono,monospace">{n["ts"]}</span></div>',unsafe_allow_html=True)
        st.markdown("---")
        st.markdown(f'<div style="font-size:10px;color:#64748b;font-family:DM Mono,monospace">FacilityOS v3.0 &middot; {datetime.now().strftime("%b %d, %Y")}</div>',unsafe_allow_html=True)
        return page

# ── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    init()
    page=sidebar()
    if page=="Dashboard": page_dashboard()
    elif page=="Assets": page_assets()
    elif page=="Work Orders": page_work_orders()
    elif page=="Staff": page_staff()
    elif page=="Inventory": page_inventory()
    elif page=="Vendors": page_vendors()
    elif page=="Budget": page_budgets()
    elif page=="Reports": page_reports()

if __name__=="__main__":
    main()
