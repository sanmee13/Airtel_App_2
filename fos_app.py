import streamlit as st
import datetime
import pandas as pd
import os

# Set up page configurations
st.set_page_config(page_title="FOS Intelligence — ASC Workways", page_icon="📍", layout="centered")

# ── 1. INJECT CUSTOM FONTS AND CSS ────────────────────────────────────
st.html("""
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;500&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
:root {
    --ink:#0f1117;--ink2:#1e2230;--ink3:#2d3348;--paper:#f5f4f0;--paper2:#ede9e0;--border:#d4cfc4;--border2:#e8e4dc;
    --red:#c8392b;--red2:#a52d21;--redl:#fdecea;--redxl:#fff8f7;--gold:#c07d2a;--goldl:#fdf3e0;--goldb:#f5d08a;
    --green:#1a6640;--greenl:#e6f4ed;--blue:#1a3a8f;--bluel:#e6ecf8;--muted:#7a7568;--muted2:#a8a398;
    --sh:0 2px 8px rgba(15,17,23,.08),0 1px 3px rgba(15,17,23,.05);--sh2:0 8px 24px rgba(15,17,23,.12);
}
.block-container { padding-top: 2.5rem !important; padding-bottom: 2rem !important; max-width: 760px !important; }
div[data-testid="stHeader"] { display: none; }
html, body { background: var(--paper); color: var(--ink); font-family:"Outfit",sans-serif; }

.hdr { background: var(--ink); padding: 0 20px; height: 52px; display: flex; align-items: center; justify-content: space-between; margin: 0 -20px 20px -20px; }
.hdr-brand { display: flex; align-items: center; gap: 10px; }
.hdr-dot { width: 8px; height: 8px; background: var(--red); border-radius: 50%; }
.hdr-name { font-family: "Syne", sans-serif; font-size: 15px; font-weight: 700; color: #fff; letter-spacing: .5px; }
.hdr-sub { font-size: 10px; color: #6b7280; letter-spacing: 2px; text-transform: uppercase; margin-left: 4px; }
.hdr-tag { font-family: "IBM Plex Mono", monospace; font-size: 11px; color: #6b7280; background: rgba(255,255,255,.06); padding: 4px 10px; border-radius: 4px; border: 1px solid rgba(255,255,255,.08); }

.search-pg { max-width: 520px; margin: 0 auto; padding: 20px 0px 40px; }
.search-eyebrow { font-size: 10px; font-weight: 600; color: var(--red); letter-spacing: 3px; text-transform: uppercase; margin-bottom: 8px; }
.search-title { font-family: "Syne", sans-serif; font-size: 32px; font-weight: 800; color: var(--ink); line-height: 1.15; margin-bottom: 12px; }
.search-meta { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 28px; }
.meta-chip { font-size: 11px; color: var(--muted); background: var(--paper2); border: 1px solid var(--border2); padding: 3px 10px; border-radius: 20px; }

.topbar { background: var(--ink); border-radius: 10px; padding: 14px 18px; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap; }
.tb-fos { font-family: "IBM Plex Mono", monospace; font-size: 18px; font-weight: 500; color: #fff; }
.tb-name { font-size: 12px; color: #9ca3af; margin-top: 2px; }
.tb-meta { font-size: 11px; color: #6b7280; margin-top: 1px; }
.tb-asc { background: rgba(124,58,237,.2); border: 1px solid rgba(124,58,237,.3); border-radius: 8px; padding: 8px 14px; text-align: center; }
.tb-asc-lbl { font-size: 9px; font-weight: 700; color: #a78bfa; text-transform: uppercase; letter-spacing: .8px; }
.tb-asc-val { font-family: "Syne", sans-serif; font-size: 20px; font-weight: 800; color: #c4b5fd; }
.tb-asc-sub { font-size: 10px; color: #a78bfa; margin-top: 1px; }

.alerts { display: flex; flex-direction: column; gap: 6px; margin-bottom: 12px; }
.al { display: flex; gap: 10px; padding: 10px 14px; border-radius: 8px; font-size: 12px; line-height: 1.5; align-items: flex-start; }
.al-ico { font-size: 14px; flex-shrink: 0; margin-top: 1px; }
.al-r { background: var(--redxl); border: 1px solid #fca5a5; color: #7f1d1d; }
.al-g { background: var(--goldl); border: 1px solid var(--goldb); color: #713f12; }
.al-c75 { background: linear-gradient(135deg,#fffbeb,#fef9c3); border: 2px solid #fcd34d; color: #713f12; }

.kpis { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 12px; }
@media(max-width: 500px){ .kpis { grid-template-columns: repeat(2, 1fr); } }
.kpi { background: #fff; border: 1px solid var(--border); border-radius: 8px; padding: 12px 14px; position: relative; overflow: hidden; }
.kpi::before { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3px; }
.kpi.kr::before { background: var(--red); } .kpi.kg::before { background: var(--gold); } .kpi.kgr::before { background: var(--green); } .kpi.kb::before { background: var(--blue); } .kpi.kp::before { background: #7c3aed; } .kpi.ki::before { background: var(--ink); }
.kpi-lbl { font-size: 9px; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: .7px; margin-bottom: 4px; }
.kpi-val { font-family: "Syne", sans-serif; font-size: 22px; font-weight: 800; color: var(--ink); line-height: 1; }
.kpi-sub { font-size: 10px; color: var(--muted); margin-top: 3px; }

.sec { margin-bottom: 12px; }
.sec-hdr { display: flex; align-items: center; justify-content: space-between; margin-bottom: 7px; }
.sec-t { font-family: "Syne", sans-serif; font-size: 13px; font-weight: 700; color: var(--ink); display: flex; align-items: center; gap: 6px; }
.pill { font-size: 10px; font-weight: 700; padding: 2px 9px; border-radius: 20px; white-space: nowrap; }
.pr { background: var(--redl); color: var(--red2); } .pg { background: var(--goldl); color: var(--gold); } .pgr { background: var(--greenl); color: var(--green); }

.card { background: #fff; border: 1px solid var(--border); border-radius: 10px; overflow: hidden; box-shadow: var(--sh); }
.card-hdr { padding: 10px 14px; border-bottom: 1px solid var(--border2); background: var(--paper2); display: flex; align-items: center; justify-content: space-between; gap: 6px; }
.card-t { font-size: 11px; font-weight: 600; color: var(--ink2); text-transform: uppercase; letter-spacing: .4px; }

.vrow { display: flex; gap: 10px; align-items: flex-start; padding: 10px 14px; border-bottom: 1px solid var(--border2); }
.vrow:last-child { border-bottom: none; }
.vrow.c75nv { background: linear-gradient(90deg,#fff7ed,#fff); border-left: 3px solid #fb923c; }
.vrow.c75win { background: linear-gradient(90deg,#fffbeb,#fff); border-left: 3px solid #fcd34d; }
.vnum { width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: "Syne", sans-serif; font-size: 11px; font-weight: 800; flex-shrink: 0; margin-top: 2px; }
.vn1 { background: var(--red); color: #fff; } .vn2 { background: var(--ink3); color: #fff; } .vn3 { background: var(--gold); color: #fff; } .vnn { background: var(--paper2); color: var(--muted); border: 1px solid var(--border); }
.vbody { flex: 1; min-width: 0; }
.vret { font-family: "IBM Plex Mono", monospace; font-size: 10px; color: var(--red); font-weight: 500; }
.vnm { font-size: 10px; color: var(--muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 200px; }
.vact { font-size: 13px; font-weight: 600; color: var(--ink); margin-top: 2px; line-height: 1.3; }
.vwhy { font-size: 11px; color: var(--muted); margin-top: 2px; line-height: 1.4; }
.vtag { display: inline-block; margin-top: 4px; padding: 2px 7px; border-radius: 3px; font-size: 9px; font-weight: 700; letter-spacing: .3px; }

.tg-c75nv { background: #fee2e2; color: #7f1d1d; border: 1px solid #fca5a5; }
.tg-c75 { background: #fef9c3; color: #713f12; border: 1px solid #fde047; }
.tg-drop { background: var(--redl); color: var(--red2); }
.tg-dorm { background: var(--goldl); color: var(--gold); }
.tg-top { background: var(--greenl); color: var(--green); }
.tg-sso { background: var(--bluel); color: var(--blue); }
.tg-wifi { background: #fff7ed; color: #c2410c; }
.tg-asc { background: #ede9fe; color: #6d28d9; }
.tg-in { background: var(--paper2); color: var(--muted); }
.vright { text-align: right; flex-shrink: 0; }
.vval { font-family: "IBM Plex Mono", monospace; font-size: 12px; font-weight: 700; color: var(--green); }
.vlbl { font-size: 9px; color: var(--muted); text-transform: uppercase; letter-spacing: .3px; }
</style>
""")

# ── 2. HELPER DATA UTILITIES ──────────────────────────────────────────
RS = '₹'
DB_FILE = "fos_data.xlsx"

def FM(v):
    return f"{RS}{v/1000:.0f}k" if v > 999 else str(round(v))

def safe_num(v):
    try:
        return float(v) if not pd.isna(v) else 0.0
    except:
        return 0.0

# ── 3. PANDAS DATA LOADING ENGINE ─────────────────────────────────────
@st.cache_data
def load_excel_database():
    if not os.path.exists(DB_FILE):
        return pd.DataFrame()
    try:
        df = pd.read_excel(DB_FILE)
        
        # Convert to string, strip spaces, and remove trailing '.0' if Excel read it as a float
        df['FOS_Number'] = df['FOS_Number'].astype(str).str.strip()
        df['FOS_Number'] = df['FOS_Number'].str.replace(r'\.0$', '', regex=True)
        
        return df
    except Exception as e:
        st.error(f"❌ Error compiling data structures from Excel: {e}")
        return pd.DataFrame()
        
# Import Database DataFrame
main_df = load_excel_database()

# ── 4. STATE SYSTEM SYNC ──────────────────────────────────────────────
if "current_view" not in st.session_state:
    st.session_state.current_view = "search"
if "selected_fos" not in st.session_state:
    st.session_state.selected_fos = ""

# Render Date Header banner
formatted_date = datetime.datetime.now().strftime("%a, %d %b %Y")
st.html(f"""
<div class="hdr">
  <div class="hdr-brand"><div class="hdr-dot"></div><span class="hdr-name">FOS INTELLIGENCE</span><span class="hdr-sub">ASC Workways</span></div>
  <div class="hdr-tag">{formatted_date}</div>
</div>
""")


# ── ROUTING ENGINE: DETECT ADMIN QUERY PARAMETER ──────────────────────
is_admin_route = st.query_params.get("page") == "admin"

if is_admin_route:
    st.markdown("### ⚙️ Admin Control Console")
    st.markdown("Upload the daily master Excel report here. The user database updates instantly.")
    
    uploaded_file = st.file_uploader("Drop daily 'fos_data.xlsx' report sheet below:", type=["xlsx"])
    
    if uploaded_file is not None:
        try:
            test_df = pd.read_excel(uploaded_file)
            if "FOS_Number" not in test_df.columns:
                st.error("❌ Schema mismatch! File structure is missing required 'FOS_Number' column headers.")
            else:
                with open(DB_FILE, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                st.cache_data.clear()
                st.success("🎉 Database successfully updated on the backend server! Active instances refreshed.")
        except Exception as e:
            st.error(f"CRITICAL COMPILATION FAILURE: {e}")
            
    if os.path.exists(DB_FILE):
        mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(DB_FILE)).strftime('%Y-%m-%d %H:%M:%S')
        st.info(f"📊 Active backend file timeline status: Last updated on **{mod_time}**")
    else:
        st.warning("⚠️ No database configured yet on the backend server. Regular links will show a holding page.")


# ── VIEW SCREEN 1: SEARCH DIRECTORY (USER APP LINK) ───────────────────
elif st.session_state.current_view == "search":
    if main_df.empty:
        st.html("""
        <div style="text-align:center; padding: 40px 10px;">
            <h3>🌐 System Under Daily Maintenance</h3>
            <p style="color:var(--muted)">The database is currently updating. Please check back shortly.</p>
        </div>
        """)
    else:
        summary_grp = main_df.groupby(['FOS_Number', 'TM_Name', 'Zone_Manager', 'Zone_Name']).size().reset_index(name='count')
        total_outlets = len(main_df)
        
        st.html(f"""
        <div class="search-pg">
            <div class="search-eyebrow">Field Officer Analytics</div>
            <div class="search-title">Today's Visit<br>Intelligence</div>
            <div class="search-meta">
                <span class="meta-chip">📍 {total_outlets:,} outlets</span>
                <span class="meta-chip">👤 {len(summary_grp)} FOS officers</span>
            </div>
        </div>
        """)
        
        selected_input = st.text_input("Enter FOS Officer Number:", value="", placeholder="Type FOS number here...")
        
        if st.button("View Dash →", use_container_width=True):
            cleaned_input = str(selected_input).strip()
            if cleaned_input:
                # Cast valid options to a set for fast, reliable matching
                valid_fos_set = set(main_df['FOS_Number'].unique())
                
                if cleaned_input in valid_fos_set:
                    st.session_state.selected_fos = cleaned_input
                    st.session_state.current_view = "dashboard"
                    st.rerun()
                else:
                    # Diagnostic fallback: Show up to 3 real examples from the sheet to reveal format issues
                    sample_formats = list(valid_fos_set)[:3]
                    sample_str = ", ".join([f"'{s}'" for s in sample_formats])
                    st.error(f"❌ FOS Number not found. Check formatting. Examples in your sheet look like: {sample_str}")
            else:
                st.error("Please enter a valid FOS identifier.") 
                
        # CHANGED: Replaced selectbox with text_input so no list is exposed on click
        selected_input = st.text_input("Enter FOS Officer Number:", value="", placeholder="Type FOS number here...")
        
        if st.button("View Dash →", use_container_width=True):
            cleaned_input = str(selected_input).strip()
            if cleaned_input:
                # Validate if the typed FOS number exists in the database
                if cleaned_input in main_df['FOS_Number'].values:
                    st.session_state.selected_fos = cleaned_input
                    st.session_state.current_view = "dashboard"
                    st.rerun()
                else:
                    st.error("❌ FOS Number not found in the records. Please verify the entry.")
            else:
                st.error("Please enter a valid FOS identifier.")


# ── VIEW SCREEN 2: DYNAMIC ANALYTICS DASHBOARD (USER APP LINK) ────────
elif st.session_state.current_view == "dashboard" and not main_df.empty:
    fos_df = main_df[main_df['FOS_Number'] == st.session_state.selected_fos]
    
    if fos_df.empty:
        st.warning("No record structures located matching selection criteria.")
        if st.button("Return to search"):
            st.session_state.current_view = "search"
            st.session_state.selected_fos = ""
            st.rerun()
    else:
        f_row = fos_df.iloc[0]
        meta = {"fos": f_row['FOS_Number'], "tm": f_row['TM_Name'], "zm": f_row['Zone_Manager'], "zn": f_row['Zone_Name']}
        
        outlets = []
        for _, row in fos_df.iterrows():
            tag = str(row.get('Outlet_Type', 'GT')).strip().upper()
            gt_tag = str(row.get('GT_Category', '')).strip()
            
            gc = safe_num(row.get('Gross_Apr26_MTD', 0))
            gp = safe_num(row.get('Gross_Mar26', 0))
            gav = (safe_num(row.get('Gross_Jan26', 0)) + safe_num(row.get('Gross_Feb26', 0)) + gp) / 3
            tc = safe_num(row.get('Tertiary_Mar26', 0))
            tt = safe_num(row.get('Tertiary_Total', 0))
            wc = safe_num(row.get('Wifi_Mar26', 0))
            bf = safe_num(row.get('Bill_Mar26', 0))
            bm = safe_num(row.get('Bill_Apr26_MTD', 0))
            b5 = safe_num(row.get('Bill_Feb26', 0))
            ss = safe_num(row.get('Swap_Apr26_MTD', 0))
            
            bl2 = bf + bm
            b_any = (b5 > 0 or bf > 0 or bm > 0)
            sso = any([safe_num(row.get('SSO_Jan26', 0)) >= 1, safe_num(row.get('SSO_Feb26', 0)) >= 1, safe_num(row.get('SSO_Mar26', 0)) >= 1])
            drop_calc = (gc - gp) / gp if gp > 0 else 0.0
            
            outlets.append({
                'r': row.get('Outlet_ID', ''), 'n': row.get('Outlet_Name', ''), 'tag': tag, 'gtTag': gt_tag,
                '_asc': tag == 'ASC', '_gt': tag != 'ASC', '_c75': (tag != 'ASC' and gt_tag == 'Club 75'),
                '_gc': gc, '_gp': gp, '_gav': gav, '_tc': tc, '_tt': tt, '_wc': wc, '_bf': bf, '_bm': bm,
                '_bl2': bl2, '_sb': bm, '_ss': ss, '_bAny': b_any, '_sso': sso,
                '_drop': drop_calc, '_dorm': (gc == 0 and gp == 0 and tt > 0), '_nv': (tag != 'ASC' and gt_tag == 'Club 75' and bl2 < 10)
            })

        dom = datetime.datetime.now().day
        is_win = (dom >= 29 or dom <= 4)
        
        gt = [r for r in outlets if r['_gt']]
        asc = [r for r in outlets if r['_asc']]
        c75 = sorted([r for r in gt if r['_c75']], key=lambda x: x['_gc'], reverse=True)
        c75nv = sorted([r for r in c75 if r['_nv']], key=lambda x: x['_bl2'])
        drops = sorted([r for r in gt if r['_drop'] < -0.25 and r['_gp'] >= 5], key=lambda x: x['_drop'])
        dormHT = sorted([r for r in gt if r['_dorm'] and r['_tt'] > 1000], key=lambda x: x['_tt'], reverse=True)
        topOL = sorted([r for r in gt if r['_gc'] >= r['_gav'] * 1.1 and r['_gc'] > 0], key=lambda x: x['_gc'], reverse=True)
        ssoOL = sorted([r for r in gt if r['_sso']], key=lambda x: x['_gc'], reverse=True)
        wifiOpp = sorted([r for r in gt if r['_wc'] == 0 and r['_tt'] > 5000], key=lambda x: x['_tt'], reverse=True)
        unbilled = [r for r in gt if not r['_bAny']]

        totG = sum(r['_gc'] for r in gt)
        totT = sum(r['_tc'] for r in gt)
        totSS = sum(r['_ss'] for r in outlets)
        totW = sum(r['_wc'] for r in outlets)
        ascG = sum(r['_gc'] for r in asc)
        ascGp = sum(r['_gp'] for r in asc)
        ascDrop = (ascG - ascGp) / ascGp if ascGp > 0 else None
        actOL = len([r for r in gt if r['_gc'] > 0])

        tasks = []
        used_rets = set()
        def add_task(r, a, w, cat, m, ml):
            if r['r'] in used_rets or len(tasks) >= 10: return
            used_rets.add(r['r'])
            tasks.append({'ret': r['r'], 'name': r['n'], 'a': a, 'w': w, 'cat': cat, 'm': m, 'ml': ml})

        for r in c75nv[:5 if is_win else 4]:
            add_task(r, f"Club 75 NOT VISITED — only {int(r['_bl2'])} billed", f"Min 10 required. Mar: {int(r['_bf'])} + Apr MTD: {int(r['_bm'])}. Visit immediately.", 'c75nv', r['_bl2'], 'billed L2M')
        if is_win:
            for r in [x for x in c75 if not x['_nv']][:3]:
                add_task(r, "Club 75 priority window visit", f"{int(r['_gc'])} sims Apr MTD. Collect orders, lock targets.", 'c75win', r['_gc'], 'APR MTD')
        for r in drops[:3]:
            add_task(r, f"Gross drop — {abs(round(r['_drop'] * 100))}% vs last month", f"Was {int(r['_gp'])} (Mar) → now {int(r['_gc'])} Apr MTD. Investigate & recover.", 'drop', r['_gc'], 'APR MTD')
        for r in dormHT[:2]:
            add_task(r, "Reactivate — zero gross, high tertiary", f"{RS}{r['_tt']/1000:.0f}k tertiary but not selling.", 'dorm', r['_tt'], 'tert')
        for r in [x for x in ssoOL if x['_gc'] < 2][:2]:
            add_task(r, "SSO not selling — push SIM", f"Only {int(r['_gc'])} Apr MTD gross. Retrain & incentivise.", 'sso', r['_sb'], 'billed')
        for r in topOL[:2]:
            add_task(r, "Maintain top performer", f"{int(r['_gc'])} sims Apr MTD, above avg {r['_gav']:.0f}.", 'top', r['_gc'], 'APR MTD')
        for r in wifiOpp[:1]:
            add_task(r, "Wifi upsell — zero bookings", f"{RS}{r['_tt']/1000:.0f}k tertiary. Easy win.", 'wifi', r['_tt'], 'tert')
        for r in unbilled[:1]:
            add_task(r, "Unbilled 3 months — push activation", "Zero billing Feb–Apr. Needs push.", 'drop', r['_gc'], 'APR MTD')
        for r in sorted(gt, key=lambda x: x['_tt'], reverse=True):
            add_task(r, "High-value — regular visit", f"{RS}{r['_tt']/1000:.0f}k tertiary.", 'top', r['_tt'], 'tert')

        TAG_STYLES = {
            'c75nv': '<span class="vtag tg-c75nv">⚠ CLUB75 NOT VIS</span>', 'c75win': '<span class="vtag tg-c75">🏆 CLUB 75</span>',
            'drop': '<span class="vtag tg-drop">GROSS DROP</span>', 'dorm': '<span class="vtag tg-dorm">DORMANT</span>',
            'top': '<span class="vtag tg-top">TOP</span>', 'sso': '<span class="vtag tg-sso">SSO</span>', 'wifi': '<span class="vtag tg-wifi">WIFI OPP</span>'
        }

        asc_badge_html = ""
        if len(asc) > 0:
            trend_lbl = ""
            if ascDrop is not None:
                trend_lbl = f"<span style='color:#a78bfa;font-size:11px'>↑{round(ascDrop*100)}%</span>" if ascDrop >= 0 else f"<span style='color:#f87171;font-size:11px'>↓{abs(round(ascDrop*100))}%</span>"
            asc_badge_html = f"""
            <div class="tb-asc">
                <div class="tb-asc-lbl">ASC Self Gross APR</div>
                <div class="tb-asc-val">{int(ascG)} <span style="font-size:12px;font-weight:400">MTD</span></div>
                <div class="tb-asc-sub">{len(asc)} outlet{'s' if len(asc)>1 else ''} {trend_lbl}</div>
            </div>
            """

        st.html(f"""
        <div class="topbar">
            <div style="display:flex;align-items:flex-start;gap:14px;flex-wrap:wrap">
                <div>
                    <div class="tb-fos">{meta['fos']}</div>
                    <div class="tb-name">{meta['tm']}</div>
                    <div class="tb-meta">{meta['zm']} · {meta['zn']} · {len(outlets)} outlets ({len(asc)} ASC · {len(gt)} GT)</div>
                </div>
                {asc_badge_html}
            </div>
        </div>
        """)

        alert_items = []
        if is_win and len(c75) > 0:
            nv_note = f" ⚠ {len(c75nv)} not visited yet." if len(c75nv) > 0 else " All visited ✓"
            alert_items.append(f'<div class="al al-c75"><div class="al-ico">🏆</div><div><strong>Club 75 Priority Window active (29th–4th)</strong> — visit all {len(c75)} Club 75 outlets first.{nv_note}</div></div>')
        if len(c75nv) > 0:
            alert_items.append(f'<div class="al al-r"><div class="al-ico">⚠️</div><div><strong>{len(c75nv)} Club 75 outlet{"s" if len(c75nv)>1 else ""} not visited</strong> — less than 10 sims billed Mar+Apr. Immediate action.</div></div>')
        if len(drops) > 0:
            alert_items.append(f'<div class="al al-r"><div class="al-ico">📉</div><div><strong>{len(drops)} outlet{"s" if len(drops)>1 else ""} with gross drop >25%</strong> (Apr MTD vs Mar)</div></div>')
        if ascDrop is not None and ascDrop < -0.2:
            alert_items.append(f'<div class="al al-r"><div class="al-ico">⚡</div><div><strong>ASC self gross down {abs(round(ascDrop*100))}%</strong> — was {int(ascGp)} (Mar), now {int(ascG)} Apr MTD</div></div>')
        if len(unbilled) > 0:
            alert_items.append(f'<div class="al al-g"><div class="al-ico">🧾</div><div><strong>{len(unbilled)} retailers</strong> with zero SIM billing Feb–Apr</div></div>')

        if alert_items:
            st.html(f'<div class="alerts">{"".join(alert_items)}</div>')

        c75_sub_color = 'var(--red)' if len(c75nv) > 0 else 'var(--green)'
        c75_sub_txt = f"{len(c75nv)} not visited" if len(c75nv) > 0 else "All visited ✓"
        
        st.html(f"""
        <div class="kpis">
            <div class="kpi kg"><div class="kpi-lbl">Club 75</div><div class="kpi-val" style="color:var(--gold)">{len(c75)}</div><div class="kpi-sub" style="color:{c75_sub_color}">{c75_sub_txt}</div></div>
            <div class="kpi kr"><div class="kpi-lbl">GT Gross APR MTD</div><div class="kpi-val">{int(totG)}</div><div class="kpi-sub">{actOL}/{len(gt)} active</div></div>
            <div class="kpi kgr"><div class="kpi-lbl">Tertiary MAR</div><div class="kpi-val" style="font-size:18px">{RS}{totT/1000:.0f}k</div><div class="kpi-sub">latest available</div></div>
            <div class="kpi kr"><div class="kpi-lbl">Gross Drops</div><div class="kpi-val" style="color:var(--red)">{len(drops)}</div><div class="kpi-sub">APR vs MAR</div></div>
            <div class="kpi kb"><div class="kpi-lbl">Sim Swaps APR</div><div class="kpi-val">{int(totSS)}</div><div class="kpi-sub">MTD</div></div>
            <div class="kpi ki"><div class="kpi-lbl">Wifi MAR</div><div class="kpi-val">{int(totW)}</div><div class="kpi-sub">latest available</div></div>
            <div class="kpi kr"><div class="kpi-lbl">Unbilled Feb–Apr</div><div class="kpi-val" style="color:var(--red)">{len(unbilled)}</div><div class="kpi-sub">retailers</div></div>
            <div class="kpi kp"><div class="kpi-lbl">SSO Outlets</div><div class="kpi-val">{len(ssoOL)}</div><div class="kpi-sub">active</div></div>
        </div>
        """)

        window_pill = '<span class="pill pg">🏆 Club 75 Window</span>' if is_win else ''
        task_rows_html = ""
        for idx, t in enumerate(tasks):
            rnk_class = 'vn1' if idx == 0 else 'vn2' if idx == 1 else 'vn3' if idx == 2 else 'vnn'
            row_mod_class = 'c75nv' if t['cat'] == 'c75nv' else 'c75win' if t['cat'] == 'c75win' else ''
            tag_badge = TAG_STYLES.get(t['cat'], '')
            
            task_rows_html += f"""
            <div class="vrow {row_mod_class}">
                <div class="vnum {rnk_class}">{idx+1}</div>
                <div class="vbody">
                    <div style="display:flex;align-items:center;gap:6px">
                        <span class="vret">{t['ret']}</span>
                        <span class="vnm">{t['name']}</span>
                    </div>
                    <div class="vact">{t['a']}</div>
                    <div class="vwhy">{t['w']}</div>
                    {tag_badge}
                </div>
                <div class="vright">
                    <div class="vval">{FM(t['m'])}</div>
                    <div class="vlbl">{t['ml']}</div>
                </div>
            </div>
            """

        st.html(f"""
        <div class="sec">
            <div class="sec-hdr">
                <div class="sec-t">🎯 Today's Visit Plan</div>
                <div style="display:flex;gap:5px">
                    <span class="pill pr">Top 10</span>
                    {window_pill}
                </div>
            </div>
            <div class="card">
                <div class="card-hdr"><div class="card-t">Priority-ranked outlet visits · Apr MTD analysis</div></div>
                {task_rows_html}
            </div>
        </div>
        """)

        if st.button("← Change FOS Officer Selection", use_container_width=True):
            st.session_state.current_view = "search"
            st.session_state.selected_fos = ""
            st.rerun()
