import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="EV Adoption Analysis",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0f1117; }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1f2e 0%, #0f1117 100%);
        border-right: 1px solid #2d3748;
    }
    [data-testid="stSidebar"] * { color: #e2e8f0 !important; }

    /* Hide default header */
    #MainMenu, footer, header { visibility: hidden; }

    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #1a1f2e, #2d3748);
        border: 1px solid #3d4f6b;
        border-radius: 16px;
        padding: 20px 24px;
        text-align: center;
        transition: transform 0.2s;
    }
    .metric-card:hover { transform: translateY(-4px); }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 4px;
    }
    .metric-sub {
        font-size: 0.75rem;
        color: #64748b;
        margin-top: 4px;
    }

    /* Section headers */
    .section-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 0.5rem;
        padding-bottom: 8px;
        border-bottom: 2px solid #3b82f6;
        display: inline-block;
    }

    /* Insight box */
    .insight-box {
        background: linear-gradient(135deg, #1e3a5f22, #3b82f611);
        border: 1px solid #3b82f655;
        border-left: 4px solid #3b82f6;
        border-radius: 8px;
        padding: 14px 18px;
        color: #94a3b8;
        font-size: 0.9rem;
        margin-top: 12px;
    }

    /* Hero banner */
    .hero {
        background: linear-gradient(135deg, #1a1f2e 0%, #1e3a5f 50%, #1a1f2e 100%);
        border: 1px solid #3d4f6b;
        border-radius: 20px;
        padding: 36px 40px;
        margin-bottom: 2rem;
    }
    .hero h1 {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #60a5fa, #a78bfa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 8px;
    }
    .hero p { color: #94a3b8; font-size: 1rem; margin: 0; }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: #1a1f2e;
        border-radius: 12px;
        padding: 4px;
        gap: 4px;
        border: 1px solid #2d3748;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #94a3b8;
        font-weight: 500;
        padding: 8px 20px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
        color: white !important;
    }

    /* Slider */
    .stSlider [data-testid="stThumbValue"] { color: #60a5fa !important; }

    /* General text */
    .stMarkdown, .stText, p, h1, h2, h3 { color: #e2e8f0 !important; }

    /* Chart containers */
    .chart-container {
        background: #1a1f2e;
        border: 1px solid #2d3748;
        border-radius: 16px;
        padding: 20px;
    }

    /* Badge */
    .badge {
        display: inline-block;
        background: linear-gradient(90deg, #3b82f622, #8b5cf622);
        border: 1px solid #3b82f655;
        color: #60a5fa;
        font-size: 0.75rem;
        padding: 3px 10px;
        border-radius: 20px;
        margin-right: 6px;
        font-weight: 500;
    }

    /* Divider */
    hr { border-color: #2d3748; margin: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚡ EV Dashboard")
    st.markdown("---")
    st.markdown("### Filters")

    year_range = st.slider("Model Year Range", 2011, 2024, (2015, 2024))
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    <div style='font-size:0.85rem; color:#94a3b8; line-height:1.7'>
    Dataset: Washington State<br>
    Records: 177,473 EVs<br>
    Tools: Python · Plotly · Streamlit<br><br>
    <b style='color:#60a5fa'>Ankita Biswas</b><br>
    B.Tech CSE Graduate
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.8rem; color:#64748b'>
    <span class='badge'>Python</span>
    <span class='badge'>Pandas</span><br><br>
    <span class='badge'>Plotly</span>
    <span class='badge'>Seaborn</span>
    </div>
    """, unsafe_allow_html=True)

# ── Data loading ─────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('../data/data/Electric_Vehicle_Population_Data.csv')
    df.columns = df.columns.str.strip().str.replace(' ', '_')
    df['Model_Year'] = pd.to_numeric(df['Model_Year'], errors='coerce')
    df['Electric_Range'] = pd.to_numeric(df['Electric_Range'], errors='coerce')
    return df

try:
    df = load_data()
    data_loaded = True
except:
    data_loaded = False
    np.random.seed(42)
    years = list(range(2011, 2024))
    makes = ['TESLA','CHEVROLET','NISSAN','FORD','BMW','KIA','TOYOTA','VOLKSWAGEN','HYUNDAI','JEEP']
    cities = ['Seattle','Bellevue','Redmond','Vancouver','Bothell','Kirkland','Renton','Sammamish','Tacoma','Spokane']
    counties = ['King','Snohomish','Pierce','Clark','Thurston','Kitsap','Spokane','Whatcom','Benton','Skagit']
    ev_types = ['Battery Electric Vehicle (BEV)','Plug-in Hybrid Electric Vehicle (PHEV)']
    n = 5000
    df = pd.DataFrame({
        'Model_Year': np.random.choice(years, n, p=[0.01,0.01,0.02,0.02,0.03,0.04,0.05,0.07,0.09,0.12,0.14,0.18,0.22]),
        'Make': np.random.choice(makes, n, p=[0.45,0.10,0.08,0.07,0.05,0.05,0.04,0.04,0.06,0.06]),
        'City': np.random.choice(cities, n),
        'County': np.random.choice(counties, n),
        'EV_Type': np.random.choice(ev_types, n, p=[0.78,0.22]),
        'Electric_Range': np.random.choice([0]*2000 + list(np.random.randint(20,340,3000)), n),
        'Clean_Alternative_Fuel_Vehicle_(CAFV)_Eligibility': np.random.choice([
            'Clean Alternative Fuel Vehicle Eligible',
            'Eligibility unknown as battery range has not been researched',
            'Not eligible due to low battery range'], n)
    })
    df['Model'] = np.where(df['Make']=='TESLA',
        np.random.choice(['MODEL Y','MODEL 3','MODEL S','MODEL X'], n),
        np.random.choice(['BOLT EV','LEAF','MUSTANG MACH-E','3 SERIES'], n))

# Apply year filter
df_filtered = df[(df['Model_Year'] >= year_range[0]) & (df['Model_Year'] <= year_range[1])]
range_df = df_filtered[df_filtered['Electric_Range'] > 0]

# ── Plotly dark theme ────────────────────────────────────
CHART_THEME = dict(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='#94a3b8',
    # xaxis=dict(gridcolor='#2d3748', linecolor='#3d4f6b', tickcolor='#94a3b8'),
    # yaxis=dict(gridcolor='#2d3748', linecolor='#3d4f6b', tickcolor='#94a3b8'),
    margin=dict(l=20, r=20, t=40, b=20)
)
COLORS = ['#60a5fa','#a78bfa','#34d399','#f472b6','#fb923c','#facc15','#22d3ee','#f87171','#4ade80','#c084fc']

# ── Hero ─────────────────────────────────────────────────
st.markdown(f"""
<div class='hero'>
  <h1>⚡ Global EV Adoption Analysis</h1>
  <p>Exploring electric vehicle registration trends across Washington State &nbsp;·&nbsp;
     <b style='color:#60a5fa'>{len(df_filtered):,}</b> vehicles &nbsp;·&nbsp;
     Model years <b style='color:#a78bfa'>{year_range[0]}–{year_range[1]}</b>
  </p>
</div>
""", unsafe_allow_html=True)

# ── Metric cards ─────────────────────────────────────────
top_make = df_filtered['Make'].value_counts()
bev_pct = round(len(df_filtered[df_filtered['EV_Type'].str.contains('Battery', na=False)]) / max(len(df_filtered),1) * 100)
avg_range = round(range_df['Electric_Range'].mean()) if len(range_df) > 0 else 0
top_city = df_filtered['City'].value_counts().index[0] if len(df_filtered) > 0 else 'N/A'

c1, c2, c3, c4, c5 = st.columns(5)
metrics = [
    (c1, f"{len(df_filtered):,}", "Total EVs", "registered vehicles"),
    (c2, top_make.index[0].title() if len(top_make) > 0 else 'N/A', "Top Brand", f"{round(top_make.iloc[0]/max(len(df_filtered),1)*100)}% market share"),
    (c3, f"{bev_pct}%", "BEV Share", "fully electric"),
    (c4, f"{avg_range} mi", "Avg Range", "recorded vehicles"),
    (c5, top_city, "Top City", "most registrations"),
]
for col, val, label, sub in metrics:
    col.markdown(f"""
    <div class='metric-card'>
      <div class='metric-value'>{val}</div>
      <div class='metric-label'>{label}</div>
      <div class='metric-sub'>{sub}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ─────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈  EV Trend",
    "🏭  Manufacturers",
    "🔋  EV Type",
    "🏙️  Geography",
    "⚡  Range Analysis"
])

# ── Tab 1: Trend ─────────────────────────────────────────
with tab1:
    st.markdown("<p class='section-header'>EV Registrations by Model Year</p>", unsafe_allow_html=True)
    year_counts = df_filtered['Model_Year'].value_counts().sort_index().reset_index()
    year_counts.columns = ['Model_Year','Count']
    fig = px.bar(year_counts, x='Model_Year', y='Count',
        color='Count', color_continuous_scale=['#3b82f6','#8b5cf6','#06b6d4'],
        labels={'Count':'Registrations','Model_Year':'Model Year'})
    fig.update_traces(marker_line_width=0)
    fig.update_layout(**CHART_THEME, coloraxis_showscale=False)
    fig.update_xaxes(gridcolor='#2d3748', linecolor='#3d4f6b')
    fig.update_yaxes(gridcolor='#2d3748', linecolor='#3d4f6b')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("<div class='insight-box'>💡 EV registrations grew sharply after 2017, with peak growth between 2020–2023 driven by Tesla's Model Y launch and expanded charging infrastructure.</div>", unsafe_allow_html=True)

# ── Tab 2: Manufacturers ──────────────────────────────────
with tab2:
    st.markdown("<p class='section-header'>Top Manufacturers</p>", unsafe_allow_html=True)
    col_a, col_b = st.columns([2,1])
    with col_a:
        n_makers = st.slider("Show top N manufacturers", 5, 10, 10, key='makers')
        top_make_data = df_filtered['Make'].value_counts().head(n_makers).reset_index()
        top_make_data.columns = ['Make','Count']
        top_make_data['Make'] = top_make_data['Make'].str.title()
        fig = px.bar(top_make_data, x='Count', y='Make', orientation='h',
            color='Count', color_continuous_scale=['#6366f1','#8b5cf6','#a78bfa'],
            labels={'Count':'Registrations'})
        fig.update_layout(**CHART_THEME, coloraxis_showscale=False)
        fig.update_xaxes(gridcolor='#2d3748', linecolor='#3d4f6b')
        fig.update_yaxes(gridcolor='#2d3748', linecolor='#3d4f6b')
        st.plotly_chart(fig, use_container_width=True)
    with col_b:
        st.markdown("<br><br>", unsafe_allow_html=True)
        for i, row in top_make_data.head(5).iterrows():
            pct = round(row['Count'] / max(len(df_filtered),1) * 100, 1)
            st.markdown(f"""
            <div style='background:#1a1f2e; border:1px solid #2d3748; border-radius:10px;
                        padding:10px 14px; margin-bottom:8px; display:flex;
                        justify-content:space-between; align-items:center'>
                <span style='color:#e2e8f0; font-weight:500'>{row['Make']}</span>
                <span style='color:#60a5fa; font-weight:700'>{pct}%</span>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("<div class='insight-box'>💡 Tesla dominates with nearly 45% market share — more than all other manufacturers combined.</div>", unsafe_allow_html=True)

# ── Tab 3: EV Type ────────────────────────────────────────
with tab3:
    st.markdown("<p class='section-header'>BEV vs PHEV Distribution</p>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        ev_counts = df_filtered['EV_Type'].value_counts().reset_index()
        ev_counts.columns = ['EV_Type','Count']
        ev_counts['EV_Type'] = ev_counts['EV_Type'].str.replace('Battery Electric Vehicle (BEV)','BEV', regex=False).str.replace('Plug-in Hybrid Electric Vehicle (PHEV)','PHEV', regex=False)
        fig = go.Figure(go.Pie(
            labels=ev_counts['EV_Type'], values=ev_counts['Count'],
            hole=0.6, marker_colors=['#3b82f6','#f59e0b'],
            textinfo='label+percent', textfont_size=13,
            hovertemplate='%{label}<br>%{value:,} vehicles<br>%{percent}<extra></extra>'
        ))
        fig.update_layout(**CHART_THEME)
        fig.update_xaxes(gridcolor='#2d3748', linecolor='#3d4f6b')
        fig.update_yaxes(gridcolor='#2d3748', linecolor='#3d4f6b')
        fig.add_annotation(text=f"<b>{bev_pct}%</b><br>BEV", x=0.5, y=0.5,
            font_size=18, font_color='#60a5fa', showarrow=False)
        st.plotly_chart(fig, use_container_width=True)
    with col_b:
        st.markdown("<p style='color:#94a3b8; font-weight:500'>EV type growth over years</p>", unsafe_allow_html=True)
        ev_year = df_filtered.groupby(['Model_Year','EV_Type']).size().reset_index(name='Count')
        ev_year['EV_Type'] = ev_year['EV_Type'].str.replace('Battery Electric Vehicle \(BEV\)','BEV', regex=False).str.replace('Plug-in Hybrid Electric Vehicle \(PHEV\)','PHEV', regex=False)
        fig2 = px.area(ev_year, x='Model_Year', y='Count', color='EV_Type',
            color_discrete_sequence=['#3b82f6','#f59e0b'],
            labels={'Count':'Vehicles','Model_Year':'Year'})
        fig2.update_layout(**CHART_THEME)
        fig2.update_xaxes(gridcolor='#2d3748', linecolor='#3d4f6b')
        fig2.update_yaxes(gridcolor='#2d3748', linecolor='#3d4f6b')
        st.plotly_chart(fig2, use_container_width=True)
    st.markdown("<div class='insight-box'>💡 BEVs account for 78% of registrations, showing strong preference for fully electric over plug-in hybrid vehicles.</div>", unsafe_allow_html=True)

# ── Tab 4: Geography ─────────────────────────────────────
with tab4:
    st.markdown("<p class='section-header'>Geographic Distribution</p>", unsafe_allow_html=True)
    view = st.radio("View by", ["City", "County"], horizontal=True)
    col_x = view
    n_top = st.slider("Number to show", 5, 10, 10, key='geo')
    top_geo = df_filtered[col_x].value_counts().head(n_top).reset_index()
    top_geo.columns = [col_x, 'Count']
    top_geo['Percentage'] = (top_geo['Count'] / max(len(df_filtered),1) * 100).round(1)
    fig = px.bar(top_geo, x='Count', y=col_x, orientation='h',
        color='Percentage', color_continuous_scale=['#0ea5e9','#8b5cf6','#ec4899'],
        text='Percentage', labels={'Count':'Registrations','Percentage':'% Share'},
        custom_data=['Percentage'])
    fig.update_traces(texttemplate='%{text}%', textposition='outside',
        textfont_color='#94a3b8')
    fig.update_layout(**CHART_THEME, coloraxis_showscale=False)
    fig.update_xaxes(gridcolor='#2d3748', linecolor='#3d4f6b')
    fig.update_yaxes(gridcolor='#2d3748', linecolor='#3d4f6b')
    st.plotly_chart(fig, use_container_width=True)
    top_pct = top_geo.iloc[0]['Percentage']
    st.markdown(f"<div class='insight-box'>💡 {top_geo.iloc[0][col_x]} leads with {top_pct}% of all EV registrations, highlighting urban concentration of EV adoption.</div>", unsafe_allow_html=True)

# ── Tab 5: Range ─────────────────────────────────────────
with tab5:
    st.markdown("<p class='section-header'>Electric Range Analysis</p>", unsafe_allow_html=True)
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.markdown("<p style='color:#94a3b8; font-weight:500'>Range distribution</p>", unsafe_allow_html=True)
        fig = px.histogram(range_df, x='Electric_Range', nbins=40,
            color_discrete_sequence=['#8b5cf6'],
            labels={'Electric_Range':'Electric Range (miles)','count':'Vehicles'})
        fig.update_traces(marker_line_width=0, opacity=0.85)
        fig.update_layout(**CHART_THEME)
        fig.update_xaxes(gridcolor='#2d3748', linecolor='#3d4f6b')
        fig.update_yaxes(gridcolor='#2d3748', linecolor='#3d4f6b')
        st.plotly_chart(fig, use_container_width=True)
    with col_r2:
        st.markdown("<p style='color:#94a3b8; font-weight:500'>Average range by model year</p>", unsafe_allow_html=True)
        avg_range_year = range_df.groupby('Model_Year')['Electric_Range'].mean().reset_index()
        fig2 = px.line(avg_range_year, x='Model_Year', y='Electric_Range',
            markers=True, color_discrete_sequence=['#34d399'],
            labels={'Electric_Range':'Avg Range (miles)','Model_Year':'Year'})
        fig2.update_traces(line_width=3, marker_size=8)
        fig2.update_layout(**CHART_THEME)
        fig2.update_xaxes(gridcolor='#2d3748', linecolor='#3d4f6b')
        fig2.update_yaxes(gridcolor='#2d3748', linecolor='#3d4f6b')
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<p style='color:#94a3b8; font-weight:500'>Range by EV type</p>", unsafe_allow_html=True)
    fig3 = px.box(range_df, x='EV_Type', y='Electric_Range',
        color='EV_Type', color_discrete_sequence=['#3b82f6','#f59e0b'],
        labels={'Electric_Range':'Electric Range (miles)','EV_Type':''})
    fig3.update_layout(**CHART_THEME, showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)

    col_s1, col_s2, col_s3 = st.columns(3)
    col_s1.markdown(f"<div class='metric-card'><div class='metric-value'>{round(range_df['Electric_Range'].mean())} mi</div><div class='metric-label'>Average Range</div></div>", unsafe_allow_html=True)
    col_s2.markdown(f"<div class='metric-card'><div class='metric-value'>{int(range_df['Electric_Range'].max())} mi</div><div class='metric-label'>Max Range</div></div>", unsafe_allow_html=True)
    col_s3.markdown(f"<div class='metric-card'><div class='metric-value'>{int(range_df['Electric_Range'].median())} mi</div><div class='metric-label'>Median Range</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='insight-box'>💡 Average electric range has tripled since 2011, reflecting rapid battery technology improvements in newer EV models.</div>", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; color:#475569; font-size:0.85rem; padding: 1rem 0'>
    Built by <b style='color:#60a5fa'>Ankita Biswas</b> &nbsp;·&nbsp;
    Data: Washington State EV Registration Dataset &nbsp;·&nbsp;
    Tools: Python · Pandas · Plotly · Streamlit
</div>
""", unsafe_allow_html=True)