import streamlit as st

st.set_page_config(layout="wide", page_title="SNA Diagnostics")

# --- CUSTOM CSS: COMPACT SIZING, GLOBAL CENTERING & STYLE OVERRIDES ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght=400;500;600&family=Montserrat:wght=600;700&display=swap');
    
    /* Global App Background, Base Font and Compressed Container Padding */
    .stApp {
        background-color: #f0f4f8;
        font-family: 'Inter', sans-serif;
    }
    .main .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 1.5rem !important;
        gap: 0.5rem !important;
    }
    
    /* Remove unnecessary default block margins */
    div[data-testid="stVerticalBlock"] > div {
        padding-bottom: 0px !important;
        margin-bottom: 0px !important;
    }
    
    /* Compact Custom Divider Style */
    hr {
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
        border: 0;
        border-top: 1px solid #cbd5e1;
    }
    
    /* All Titles, Subheaders and Section Headings Centered globally with Tight Spacing */
    h1, h2, h3, [data-testid="stMarkdownContainer"] h3 {
        font-family: 'Montserrat', sans-serif;
        text-align: center !important;
        justify-content: center !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    h1 {
        font-weight: 700;
        font-size: 2.6rem !important;
        color: #0f172a !important;
    }
    
    h3 {
        font-weight: 600;
        font-size: 1.75rem !important;
        color: #1e293b !important;
    }
    
    /* Center columns structurally and condense padding */
    div[data-testid="column"] {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding: 0.2rem 1rem !important;
    }
    
    /* KPI Card container style */
    .kpi-card {
        background-color: #ffffff !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
        border-top: 4px solid #1f77b4 !important; /* Professional Blue Accent */
        text-align: center;
        margin: 5px;
    }
    
    /* Text styling with text-align center for structured bullet lists */
    .stMarkdown p, .stMarkdown li {
        font-size: 1.15rem !important;
        line-height: 1.4 !important;
        color: #334155 !important;
        text-align: center !important;
        list-style-position: inside !important;
        margin-bottom: 0.2rem !important;
    }
    
    /* Custom White KPI Cards for Metrics with reduced padding */
    div[data-testid="stMetricContainer"] {
        background-color: white;
        border-radius: 12px;
        padding: 0.8rem 1.2rem !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid #e2e8f0;
        width: 100%;
    }
    
    /* Scale Up Metric Labels and Values */
    div[data-testid="stMetricLabel"] > div {
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        color: #64748b !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        text-align: center !important;
    }
    div[data-testid="stMetricValue"] > div {
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        color: #1f77b4 !important;
    }
    /* ADD THIS AT THE BOTTOM OF YOUR STYLE BLOCK */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important; 
    }

    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] li,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] span {
        color: white !important;
    }

    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: white !important;
    }
    
    /* Force black text inside st.info and st.warning blocks */
    div[data-testid="stInfoMessage"] p, 
    div[data-testid="stWarningMessage"] p {
        color: #000000 !important;
    }

    /* Optional: if you want the icons to match or stay visible */
    div[data-testid="stInfoMessage"] div[data-testid="stIcon"] {
        color: #000000 !important;
    }
    
     /* Optional hover effect */
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Structural page redirection mapping
if st.button("🏠 Back to Overview Home"):
    st.switch_page("Overview.py")  # Ensure this matches your exact overview file filename

st.title("Social Network Analysis Diagnostics")
st.html("<hr>")

# Create the columns
# Helper to render the cards
def render_kpi_card(col, label, value, url=None, info=None):
    with col:
        # Construct link if URL exists
        display_value = f'<a href="{url}" target="_blank" style="text-decoration:none; color:#0f172a;">{value}</a>' if url else value
        
        # Construct info icon if info is provided
        info_html = f'<span title="{info}" style="cursor:help; color:#3b82f6; font-size:12px;"> ℹ️</span>' if info else ""
        
        st.markdown(f'''
            <div class="kpi-card">
                <div style="font-size: 14px; color: #64748b; margin-bottom: 5px;">
                    {label}{info_html}
                </div>
                <div style="font-size: 20px; font-weight: bold; color: #0f172a;">
                    {display_value}
                </div>
            </div>
        ''', unsafe_allow_html=True)

# Layout for your 5 columns
cols = st.columns(5)
render_kpi_card(cols[0], "Target Node", "@futuremarketers_", 
                url="https://www.tiktok.com/@futuremarketers_", 
                info="The primary influencer identified by SNA centrality metrics (Click the username).")
render_kpi_card(cols[1], "Total Nodes", "304", 
                info="Total unique accounts detected in the C-Mart interaction network.")
render_kpi_card(cols[2], "Total Edges", "5,895", 
                info="Total successful interactions/mentions between accounts.")
render_kpi_card(cols[3], "Community Count", "4 Main", 
                info="Number of distinct clusters discovered in the network.")
render_kpi_card(cols[4], "Centrality Vector", "Betweenness", 
                info="Metric used to determine the 'bridge' power of a node.")

st.html("<hr>")

# Two column layout for Insights and Community Overview
col_left, col_right = st.columns(2)

with col_left:
    # 🔍 Network Insights
    st.info("### Key Network Insights")
    st.markdown("""
    * [**@futuremarketers_**](https://www.tiktok.com/@futuremarketers_) and [**@strawberrycovey**](https://www.tiktok.com/@strawberrycovey) are the main connectors in the network.  
    * These accounts help spread information quickly between different groups.  
    * They act as a bridge connecting **C-Mart** with student communities.  
    """)

with col_right:
    # 👥 Communities
    st.info("### Community Overview")
    st.markdown("""
    * **4 Main Communities Identified:**
        * `cmart` / `cmartchanglun` *(C-Mart accounts)* 
        * `uum` / `uumsintok` *(UUM community)* 
        * `student` *(main student group)* 
        * `studentlife` *(student lifestyle group)* 
        * Students mostly interact within their own groups.  
    """)

st.html("<hr>")

# Setup clean dashboard structure cards based on project summary details
st.subheader("High-Resolution Topology Layout View")

try:
    # Read and output the vector graphic pathways directly into the browser
    with open("SulamSNA.svg", "r", encoding="utf-8") as f:
        svg_content = f.read()
    st.components.v1.html(svg_content, height=700, scrolling=True)
except FileNotFoundError:
    st.info("💡 Drop your high-resolution network export file named `SulamSNA.svg` inside your root project folder to see it render live here.")
    
st.html("<hr>")

st.html("<hr>")
st.subheader("🚀 Strategic Recommendations")

# Use a 3-column layout for business recommendations
dec_col1, dec_col2, dec_col3 = st.columns(3)

with dec_col1:
    st.warning("### 🎯 Influencer Collaboration")
    st.markdown("""
    * **Recommendation:** Work with **@futuremarketers_** as a key promoter.
    * **Why:** This user has strong connections and can help spread C-Mart promotions to more people.
    * **Action:** Create special promotions or discount codes through this influencer.
    """)

with dec_col2:
    st.warning("### 📢 Community Engagement")
    st.markdown("""
    * **Recommendation:** Focus on the **Student Lifestyle** community.
    * **Why:** This group is active but has limited interaction with C-Mart.
    * **Action:** Organize student campaigns, contests, or activities to increase engagement.
    """)

with dec_col3:
    st.warning("### 🛡️ Building Stronger Connections")
    st.markdown("""
    * **Recommendation:** Develop more active users as future promoters.
    * **Why:** Relying on only a few influencers may limit information sharing.
    * **Action:** Support more student influencers to create a stronger and wider network.
    """)


st.html("<hr>")
# 📘 Information Section
st.subheader("Information")

col_info_left, col_info_right = st.columns(2)

with col_info_left:
    # 📊 How SNA Works
    st.info("### How SNA Works?")
    st.markdown("""
    * SNA shows how users are **connected in a network** 
    * **Node** = user / account  
    * **Edge** = interaction (like, comment, mention)  
    * Helps us understand **who interacts** and how info spreads  
    """)

with col_info_right:
    # 🔗 Betweenness Centrality
    st.info("### Betweenness Centrality")
    st.markdown("""
    * Shows **who acts as a bridge** between groups  
    * High value = connects different communities  
    * Important for **spreading information** 
    * Example: **futuremarketers_** links C-Mart with students  
    """)