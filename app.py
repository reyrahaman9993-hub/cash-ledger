import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date

# Set your secret Admin PIN here
ADMIN_PIN = "3010"

st.set_page_config(
    page_title="LedgerFlow - Cash Tracking",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 1. State Management
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Light"

if "panel_action" not in st.session_state:
    st.session_state.panel_action = None

if "transactions" not in st.session_state:
    st.session_state.transactions = [
        {"id": 1, "Date": "2025-12-01", "Amount": 31000.0, "Type": "Cash Given"},
        {"id": 2, "Date": "2026-02-04", "Amount": 5167.0, "Type": "Cash Received"},
        {"id": 3, "Date": "2026-02-07", "Amount": 4000.0, "Type": "Cash Given"},
        {"id": 4, "Date": "2026-02-19", "Amount": 2000.0, "Type": "Cash Received"},
        {"id": 5, "Date": "2026-02-23", "Amount": 1000.0, "Type": "Cash Received"},
        {"id": 6, "Date": "2026-03-05", "Amount": 5167.0, "Type": "Cash Received"},
        {"id": 7, "Date": "2026-03-10", "Amount": 2000.0, "Type": "Cash Given"},
        {"id": 8, "Date": "2026-03-11", "Amount": 3000.0, "Type": "Cash Received"},
        {"id": 9, "Date": "2026-03-21", "Amount": 1500.0, "Type": "Cash Given"},
        {"id": 10, "Date": "2026-04-06", "Amount": 5167.0, "Type": "Cash Received"},
        {"id": 11, "Date": "2026-06-13", "Amount": 4000.0, "Type": "Cash Received"},
        {"id": 12, "Date": "2026-07-02", "Amount": 30000.0, "Type": "Cash Given"},
        {"id": 13, "Date": "2026-07-06", "Amount": 573.0, "Type": "Cash Given"},
        {"id": 14, "Date": "2026-07-29", "Amount": 4690.0, "Type": "Cash Received"},
        {"id": 15, "Date": "2026-08-03", "Amount": 10000.0, "Type": "Cash Received"},
        {"id": 16, "Date": "2026-10-02", "Amount": 2000.0, "Type": "Cash Given"},
        {"id": 17, "Date": "2026-11-03", "Amount": 35000.0, "Type": "Cash Given"},
        {"id": 18, "Date": "2026-11-08", "Amount": 5000.0, "Type": "Cash Received"}
    ]

# Theme Colors
is_dark = (st.session_state.theme_mode == "Dark")
bg_page = "#0f172a" if is_dark else "#f8fafc"
bg_card = "#1e293b" if is_dark else "#ffffff"
border_color = "#334155" if is_dark else "#cbd5e1"
text_primary = "#f8fafc" if is_dark else "#0f172a"
text_muted = "#94a3b8" if is_dark else "#475569"
plotly_template = "plotly_dark" if is_dark else "plotly_white"

# Styling
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    .stApp {{
        background-color: {bg_page};
        color: {text_primary};
    }}
    .block-container {{
        padding-top: 4.5rem !important;
        padding-bottom: 2.5rem;
        max-width: 1250px;
    }}
    label[data-testid="stWidgetLabel"] p,
    div[data-testid="stWidgetLabel"] p {{
        color: {text_primary} !important;
        font-weight: 700 !important;
        font-size: 13px !important;
    }}
    div[data-baseweb="select"] > div {{
        background-color: {bg_card} !important;
        border: 1px solid {border_color} !important;
        border-radius: 10px !important;
    }}
    div[data-baseweb="select"] * {{
        color: {text_primary} !important;
        font-weight: 600 !important;
    }}
    .metric-card {{
        background: {bg_card};
        border: 1px solid {border_color};
        border-radius: 18px;
        padding: 22px;
        box-shadow: 0 4px 12px rgba(0,0,0,{"0.25" if is_dark else "0.03"});
        min-height: 145px;
    }}
    .metric-card-owed {{
        border-left: 5px solid #f59e0b !important;
    }}
    .card-top {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }}
    .card-label {{
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: {text_muted};
    }}
    .card-icon-pill {{
        width: 34px;
        height: 34px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
    }}
    .pill-red {{ background: {"rgba(239,68,68,0.2)" if is_dark else "#fee2e2"}; color: #ef4444; }}
    .pill-green {{ background: {"rgba(16,185,129,0.2)" if is_dark else "#dcfce7"}; color: #10b981; }}
    .pill-orange {{ background: {"rgba(245,158,11,0.2)" if is_dark else "#fef3c7"}; color: #f59e0b; }}
    .pill-indigo {{ background: {"rgba(99,102,241,0.2)" if is_dark else "#e0e7ff"}; color: #818cf8; }}
    .card-value {{
        font-size: 27px;
        font-weight: 800;
        color: {text_primary};
        letter-spacing: -0.02em;
        margin-bottom: 6px;
    }}
    .card-value-orange {{ color: #f59e0b; }}
    .card-subtext {{
        font-size: 13px;
        color: {text_muted};
        font-weight: 500;
    }}
    .progress-track {{
        width: 100%;
        height: 8px;
        background: {"#334155" if is_dark else "#e2e8f0"};
        border-radius: 999px;
        overflow: hidden;
        margin-top: 8px;
    }}
    .progress-fill {{
        height: 100%;
        background: #10b981;
        border-radius: 999px;
    }}
</style>
""", unsafe_allow_html=True)

# 2. Compute Ledger Data
if st.session_state.transactions:
    df = pd.DataFrame(st.session_state.transactions)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)
    df["Net_Impact"] = df.apply(lambda r: r["Amount"] if r["Type"] == "Cash Given" else -r["Amount"], axis=1)
    df["Running_Balance"] = df["Net_Impact"].cumsum()

    given_entries = df[df["Type"] == "Cash Given"]
    received_entries = df[df["Type"] == "Cash Received"]
    total_given = given_entries["Amount"].sum()
    total_received = received_entries["Amount"].sum()
    net_owed = total_given - total_received
    recovery_rate = (total_received / total_given * 100) if total_given > 0 else 0
else:
    df = pd.DataFrame(columns=["id", "Date", "Amount", "Type", "Running_Balance"])
    total_given = total_received = net_owed = recovery_rate = 0
    given_entries = received_entries = []

# 3. Header Bar
head_col1, head_col2, head_col3, head_col4 = st.columns([5, 2, 2, 2], vertical_alignment="center")

with head_col1:
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:12px;">
        <div style="background:#4f46e5; color:white; width:44px; height:44px; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:22px; font-weight:bold;">⚖️</div>
        <div>
            <h2 style="margin:0; font-size:22px; font-weight:800; color:{text_primary};">LedgerFlow</h2>
            <p style="margin:0; font-size:12px; color:{text_muted};">Cash Given & Received Tracking</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with head_col2:
    selected_theme = st.selectbox(
        "Theme", 
        ["Light", "Dark"], 
        index=0 if st.session_state.theme_mode == "Light" else 1,
        key="theme_selector"
    )
    if selected_theme != st.session_state.theme_mode:
        st.session_state.theme_mode = selected_theme
        st.rerun()

with head_col3:
    csv_bytes = df.to_csv(index=False).encode('utf-8') if not df.empty else b""
    st.download_button(
        label="📥 Export CSV",
        data=csv_bytes,
        file_name="ledger_transactions.csv",
        mime="text/csv",
        use_container_width=True
    )

with head_col4:
    action = st.selectbox(
        "Manage Data",
        ["Select...", "➕ Add Entry", "🗑️ Delete Entry"],
        key="action_menu"
    )
    if action == "➕ Add Entry" and st.session_state.panel_action != "add":
        st.session_state.panel_action = "add"
        st.rerun()
    elif action == "🗑️ Delete Entry" and st.session_state.panel_action != "delete":
        st.session_state.panel_action = "delete"
        st.rerun()

# 4. Action Drawers (Protected with Admin PIN)
if st.session_state.panel_action == "add":
    with st.expander("➕ Add New Transaction (Admin Only)", expanded=True):
        a1, a2, a3, a4 = st.columns(4)
        with a1:
            in_date = st.date_input("Date", value=date.today())
        with a2:
            in_type = st.selectbox("Type", ["Cash Given", "Cash Received"])
        with a3:
            in_amount = st.number_input("Amount (₹)", min_value=1.0, value=1000.0, step=100.0)
        with a4:
            entered_pin = st.text_input("Enter Admin PIN", type="password")
        
        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            if st.button("Save Transaction", type="primary", use_container_width=True):
                if entered_pin != ADMIN_PIN:
                    st.error("⛔ Unauthorized Access: You do not have permission to alter the ledger entries!")
                else:
                    new_id = max([x["id"] for x in st.session_state.transactions], default=0) + 1
                    st.session_state.transactions.append({
                        "id": new_id,
                        "Date": str(in_date),
                        "Amount": float(in_amount),
                        "Type": in_type
                    })
                    st.session_state.panel_action = None
                    st.rerun()
        with btn_c2:
            if st.button("Close", use_container_width=True):
                st.session_state.panel_action = None
                st.rerun()

elif st.session_state.panel_action == "delete":
    with st.expander("🗑️ Delete Transaction (Admin Only)", expanded=True):
        if not st.session_state.transactions:
            st.info("No transactions available to delete.")
        else:
            col_del1, col_del2 = st.columns([3, 1])
            with col_del1:
                options = {
                    f"ID {item['id']} | {item['Date']} | {item['Type']} | ₹{item['Amount']:,.2f}": item['id']
                    for item in sorted(st.session_state.transactions, key=lambda x: x["Date"], reverse=True)
                }
                selected_label = st.selectbox("Select entry to delete:", list(options.keys()))
                target_id = options[selected_label]
            with col_del2:
                entered_pin = st.text_input("Admin PIN", type="password", key="del_pin")
            
            del_c1, del_c2 = st.columns(2)
            with del_c1:
                if st.button("Confirm Delete", type="primary", use_container_width=True):
                    if entered_pin != ADMIN_PIN:
                        st.error("🚨 Tamper Alert: Only the owner can delete transactions from the ledger!")
                    else:
                        st.session_state.transactions = [
                            x for x in st.session_state.transactions if x["id"] != target_id
                        ]
                        st.session_state.panel_action = None
                        st.rerun()
            with del_c2:
                if st.button("Cancel", use_container_width=True):
                    st.session_state.panel_action = None
                    st.rerun()

st.write("")

# 5. KPI Cards
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="card-top">
            <span class="card-label">Total Cash Given</span>
            <div class="card-icon-pill pill-red">↗</div>
        </div>
        <div class="card-value">₹{total_given:,.2f}</div>
        <div class="card-subtext"><b style="color:#ef4444;">{len(given_entries)} entries</b> disbursed</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="card-top">
            <span class="card-label">Total Cash Received</span>
            <div class="card-icon-pill pill-green">↙</div>
        </div>
        <div class="card-value">₹{total_received:,.2f}</div>
        <div class="card-subtext"><b style="color:#10b981;">{len(received_entries)} entries</b> collected</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card metric-card-owed">
        <div class="card-top">
            <span class="card-label">Cash Still Owed</span>
            <div class="card-icon-pill pill-orange">⏳</div>
        </div>
        <div class="card-value card-value-orange">₹{net_owed:,.2f}</div>
        <div class="card-subtext">Net remaining balance</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="card-top">
            <span class="card-label">Recovery Rate</span>
            <div class="card-icon-pill pill-indigo">🕒</div>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:baseline;">
            <div class="card-value">{recovery_rate:.1f}%</div>
            <span style="font-size:12px; color:{text_muted}; font-weight:600;">Target: 100%</span>
        </div>
        <div class="progress-track">
            <div class="progress-fill" style="width: {min(recovery_rate, 100)}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# 6. Interactive Charts
ch1, ch2 = st.columns([7, 5])

if not df.empty:
    with ch1:
        df_chart = df.copy()
        df_chart["Period"] = df_chart["Date"].dt.to_period("M")
        monthly = df_chart.groupby(["Period", "Type"])["Amount"].sum().unstack(fill_value=0).reset_index()
        monthly["MonthYear"] = monthly["Period"].dt.strftime("%b %Y")
        
        y_cols = [c for c in ["Cash Given", "Cash Received"] if c in monthly.columns]
        fig_bar = px.bar(
            monthly,
            x="MonthYear",
            y=y_cols,
            barmode="group",
            title="<b>Monthly Cash Activity</b>",
            color_discrete_map={"Cash Given": "#ef4444", "Cash Received": "#10b981"},
            template=plotly_template,
            height=340
        )
        fig_bar.update_layout(
            paper_bgcolor=bg_card,
            plot_bgcolor=bg_card,
            font=dict(family="Plus Jakarta Sans", color=text_primary, size=12),
            margin=dict(l=20, r=20, t=50, b=20),
            legend=dict(
                title_text="",
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(color=text_primary)
            ),
            xaxis=dict(tickfont=dict(color=text_primary), title=""),
            yaxis=dict(tickfont=dict(color=text_primary), title="Amount (₹)")
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with ch2:
        fig_donut = go.Figure(data=[go.Pie(
            labels=["Cash Received", "Cash Still Owed"],
            values=[total_received, max(net_owed, 0)],
            hole=0.68,
            marker_colors=["#10b981", "#f59e0b"],
            textinfo="percent+label",
            textfont=dict(color=text_primary, size=11)
        )])
        fig_donut.update_layout(
            title="<b>Recovery Breakdown</b>",
            paper_bgcolor=bg_card,
            plot_bgcolor=bg_card,
            template=plotly_template,
            height=340,
            font=dict(family="Plus Jakarta Sans", color=text_primary),
            margin=dict(l=20, r=20, t=50, b=20),
            showlegend=False
        )
        st.plotly_chart(fig_donut, use_container_width=True)

# 7. Strictly Read-Only Table (No Cell Editing Allowed)
st.subheader("📋 Transaction History")
st.caption("🔒 Verified Ledger: Table records are read-only.")

if not df.empty:
    tbl_df = df.copy()
    tbl_df["Formatted Date"] = tbl_df["Date"].dt.strftime("%d %b %Y")
    tbl_df["Formatted Amount"] = tbl_df["Amount"].apply(lambda x: f"₹{x:,.2f}")
    tbl_df["Balance After Transaction"] = tbl_df["Running_Balance"].apply(lambda x: f"₹{x:,.2f}")

    st.dataframe(
        tbl_df[["id", "Formatted Date", "Type", "Formatted Amount", "Balance After Transaction"]],
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No transaction data available.")
