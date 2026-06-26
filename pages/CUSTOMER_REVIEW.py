import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="Full Reviews Table")


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
    
    /* Target the main selectbox container */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        background-color: #ffffff !important; /* Your chosen light color */
        border: 2px solid #0f172a !important;   /* Your chosen border color */
        border-radius: 8px !important;
    }

    /* Target the text inside the selectbox */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        color: #1e293b !important;
    }

    /* Target the dropdown arrow icon */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] svg {
        fill: #1e293b !important;
    }
    
    </style>
""", unsafe_allow_html=True)

if st.button("🏠 Back to Overview Home"):
    st.switch_page("Overview.py")

st.title("Full Review Explorer")
st.markdown("---")

df = pd.read_csv("SulamTextAnalysis(this).csv")

col_r1, col_r2 = st.columns(2)
with col_r1:
    s_filter = st.selectbox("Filter Sentiment", ["All", "Positive", "Negative", "Neutral"], key="table_s")
with col_r2:
    p_filter = st.selectbox("Filter Role / Person Type", ["All", "Visitor", "Vendor"], key="table_p")

sent_col = 'sentiment' if 'sentiment' in df.columns else 'Sentiment'
person_col = 'Person' if 'Person' in df.columns else 'person'

filtered_df = df.copy()

if s_filter != "All":
    filtered_df = filtered_df[filtered_df[sent_col].str.lower() == s_filter.lower()]
if p_filter != "All":
    filtered_df = filtered_df[filtered_df[person_col].str.lower() == p_filter.lower()]

# --- 2. RENDER THE TABLE ---
st.subheader("Raw Data Feedback Matrix")

# Ensure all columns exist in the subset we display
display_cols = [c for c in ['Text', sent_col, person_col] if c in filtered_df.columns]

# Display the dataframe with high contrast formatting
st.dataframe(
    filtered_df[display_cols], 
    use_container_width=True,
    column_config={
        sent_col: st.column_config.Column("Sentiment", width="small"),
        person_col: st.column_config.Column("Role", width="small")
    }
)

csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download filtered data as CSV",
    data=csv,
    file_name='sulam_filtered_data.csv',
    mime='text/csv',
)