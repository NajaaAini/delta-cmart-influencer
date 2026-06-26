import streamlit as st

st.set_page_config(layout="wide", page_title="About - SULAM Project")

# --- CUSTOM CSS: COMPACT SIZING, GLOBAL CENTERING & WHITE BACKGROUND CARDS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Montserrat:wght=600;700&display=swap');
    
    .stApp { background-color: #f0f4f8; font-family: 'Inter', sans-serif; }
    
    /* Apply Card Styling ONLY to the main structural columns */
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        background-color: white;
        border-radius: 16px;
        padding: 1.5rem !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
    }

    /* Target specific SDG columns to remove the card shadow/background */
    .sdg-card-override div[data-testid="column"] {
        background-color: transparent !important;
        box-shadow: none !important;
        border: none !important;
    }

    /* All Titles, Subheaders and Section Headings Centered */
    h1, h2, h3, h4 { font-family: 'Montserrat', sans-serif; text-align: center !important; }
    
    h1 { font-weight: 700; font-size: 2.6rem !important; color: #0f172a !important; }
    h3 { font-weight: 600; font-size: 1.75rem !important; color: #1e293b !important; }
    
    .stMarkdown p, .stMarkdown li { font-size: 1.1rem !important; color: #334155 !important; }
    
    hr { margin: 1rem 0; border-top: 1px solid #cbd5e1; }
    
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
    
    /* Team Member Card Style */
    .team-card {
        background: #ffffff;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #e2e8f0;
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .team-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border-color: #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# Navigation button
if st.button("🏠 Back to Overview Home"):
    st.switch_page("Overview.py")  # Ensure this matches your exact filename

col_logo, col_title = st.columns([1, 5])

with col_logo:
    # Use your logo file here
    st.image("logo2.png", width=140)

with col_title:
    st.markdown("<h1 class='custom-title' style='text-align: left !important;'>COMMUNITY-BASED INFLUENCER DEVELOPMENT FOR SHOPPING MALL ENGAGEMENT AT C-MART CHANGLUN</h1>", unsafe_allow_html=True)
st.markdown("---")
col_synopsis, col_objective = st.columns(2)

with col_synopsis:
    st.info("### Project Synopsis")
    st.markdown("""
    This project was conducted to help **C-Mart Changlun** understand customer behavior through social media analytics and interviews. 
    Data from TikTok and interview responses were analyzed to identify customer communities, interaction patterns, sentiments, and potential influencers.
    """)

with col_objective:
    st.info("### Project Objectives")
    st.markdown("""
    1. **Identify community-based influencers** that can enhance customer engagement.
    2. **Analyze social network structures** and influence patterns among customers.
    3. **Examine customer sentiments** and opinions toward C-Mart Changlun.
    4. **Develop a practical framework** for community-based influencer development.
    """)
    
col_theory1, col_theory2  = st.columns(2)

with col_theory1:
    st.info("### SNA?")
    st.markdown("""
    **Social Network Analysis (SNA)** is a method used to study how people or groups are connected and interact with each other.
    
    * **Nodes:** Represent individuals or entities (for example, users or accounts).
    * **Edges:** Show the relationship or interaction between nodes (for example, replies, mentions, or connections).
    * **Purpose:** Helps discover important users, communities, and patterns within a network.
    """)

with col_theory2:
    st.info("### Sentiment Analysis")
    st.markdown("""
    **Sentiment Analysis** is a technique that identifies the emotions or opinions expressed in text data.
    
    * **Sentiment Type:** Classifies feedback as **Positive**, **Negative**, or **Neutral**.
    * **Process:** Examines words and language patterns to understand user opinions.
    * **Purpose:** Helps measure public feedback, satisfaction, and overall perception.
    """)

st.markdown("---")

# --- ROW 1: Synopsis & Objectives ---

# --- FULL WIDTH: METHODOLOGY SECTION (2-Column Grid) ---
st.info("### KDD Methodology")
st.markdown("This project follows the **Knowledge Discovery in Databases (KDD)** framework to transform raw social media data into actionable insights.")

m_col1, m_col2 = st.columns([1, 1.5])

with m_col1:
    try:
        # 
        st.image("kdd.png", use_container_width=True)
    except Exception:
        st.info("💡 Place 'kdd.png' in your folder.")

with m_col2:
    st.markdown("""
    * **Data Selection:** Collected relevant data from TikTok interactions using Apify and customer feedback from surveys/interviews at C-Mart Changlun.
    
    * **Data Preprocessing:** Removed duplicate, incomplete, and unnecessary data to improve data quality before analysis.
    
    * **Data Transformation:** Organized and converted the cleaned data into a suitable format for SNA and sentiment analysis.
    
    * **Data Mining:** Applied **Social Network Analysis (SNA)** to identify user connections and influencers, and used sentiment analysis to understand customer opinions.
    
    * **Evaluation:** Interpreted the results to identify engagement patterns, customer perceptions, and insights for improving C-Mart's marketing strategies.
    """)

st.html("<hr>")
# --- FULL WIDTH: SDG ALIGNMENT SECTION (Icon beside Description) ---
st.info("### SDG Alignment")
st.markdown("This SULAM project proudly aligns with the following Sustainable Development Goals:")

st.markdown('<div class="sdg-card-override">', unsafe_allow_html=True)

# Helper function to create an Icon + Description row
def sdg_row(img_path, title, desc):
    col_icon, col_text = st.columns([1, 4]) # 1 part icon, 4 parts text
    with col_icon:
        st.image(img_path, width=80)
    with col_text:
        st.markdown(f"**{title}**")
        st.write(desc)

# Create the 2x2 grid
row1_c1, row1_c2 = st.columns(2)
row2_c1, row2_c2 = st.columns(2)
with row1_c1:
    sdg_row(
        "sdg4.png", 
        "SDG 4: Quality Education", 
        "Helping C-Mart vendors improve their digital skills through learning and knowledge sharing."
    )

with row1_c2:
    sdg_row(
        "sdg8.png", 
        "SDG 8: Decent Work", 
        "Supporting C-Mart growth by attracting more customers and increasing business opportunities through digital engagement."
    )

with row2_c1:
    sdg_row(
        "sdg9.png", 
        "SDG 9: Industry & Innovation", 
        "Using data analysis and SNA techniques to improve C-Mart's marketing strategies and customer outreach."
    )

with row2_c2:
    sdg_row(
        "sdg17.png", 
        "SDG 17: Partnership", 
        "Creating a strong collaboration between UUM and C-Mart Changlun to support continuous improvement and future growth."
    )
st.markdown('</div>', unsafe_allow_html=True)
st.html("<hr>")
# --- TEAM SECTION ---
st.info("###  Project Management Team")

# Adjust column ratios: 20% for Advisor, 80% for Team
col_advisor, col_team = st.columns([1, 4])

with col_advisor:
    st.markdown("### Project Advisor")
    with st.container(border=True):
        st.markdown("#### Assoc. Prof. Ts. Dr. Juhaida Abu Bakar")

with col_team:
    st.markdown("### Group Members")
    
    # Render all members in one row using 5 columns
    cols = st.columns(5)
    members = [
        ("Zahra Naila Putri Az", "297047"),
        ("Nur Ayunie Syukuriah", "297689"),
        ("Nur Najaa Aini", "297730"),
        ("Gilang Ramadhan", "291140"),
        ("Nur Fatinah", "297381")
    ]
    
    for i, col in enumerate(cols):
        with col:
            # Re-using the team-card class from previous CSS
            st.markdown(f'''
                <div class="team-card">
                    <div style="font-weight: 600; font-size: 0.85rem;">{members[i][0]}</div>
                    <div style="color: #64748b; font-size: 0.75rem;">{members[i][1]}</div>
                </div>
            ''', unsafe_allow_html=True)

st.divider()

# --- 📸 PHOTO GALLERY SECTION ---
st.subheader("📸 SULAM Fieldwork Activity Gallery")

# --- Gallery Row 1: Interview with vendor in Car Boot Sales ---
st.markdown("### Interview with Vendors in Car Boot Sales")
r1_c1, r1_c2, r1_c3 = st.columns(3)

with r1_c1:
    try:
        st.image("Vendor1.jpeg", use_container_width=True)
    except Exception:
        st.info("💡 Place image file `Vendor1.jpeg` here")

with r1_c2:
    try:
        st.image("Vendor2.jpg", use_container_width=True)
    except Exception:
        st.info("💡 Place image file `Vendor2.jpg` here")

with r1_c3:
    try:
        st.image("Vendor3.jpg", use_container_width=True)
    except Exception:
        st.info("💡 Place image file `Vendor3.jpg` here")
    
st.markdown(" ") 

# --- Gallery Row 2: Interview with visitor in Cmart Changlun ---
st.markdown("### Interview with Visitors in C-Mart Changlun")
r2_c1, r2_c2, r2_c3 = st.columns(3)

with r2_c1:
    try:
        st.image("Visitor1.jpeg", use_container_width=True)
    except Exception:
        st.info("💡 Place image file `Visitor1.jpeg` here")

with r2_c2:
    try:
        st.image("Visitor2.jpeg", use_container_width=True)
    except Exception:
        st.info("💡 Place image file `Visitor1.jpeg` here")

with r2_c3:
    try:
        st.image("Visitor3.jpeg", use_container_width=True)
    except Exception:
        st.info("💡 Place image file `Visitor1.jpeg` here")
        
st.markdown("### Social Media Data Analytics Class")
r2_c1, r2_c2, r2_c3 = st.columns(3)

with r2_c1:
    try:
        st.image("SMDA1.jpeg", use_container_width=True)
    except Exception:
        st.info("💡 Place image file `Visitor1.jpeg` here")

with r2_c2:
    try:
        st.image("SMDA2.jpeg", use_container_width=True)
    except Exception:
        st.info("💡 Place image file `Visitor1.jpeg` here")

with r2_c3:
    try:
        st.image("SMDA3.jpeg", use_container_width=True)
    except Exception:
        st.info("💡 Place image file `Visitor1.jpeg` here")