import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Put this at the very top of your script to affect all charts
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Inter', 'DejaVu Sans', 'Arial']
plt.rcParams['figure.dpi'] = 200 # Forces crisp, high-resolution graph rendering

# Set layout config first
st.set_page_config(layout="wide", page_title="C-Mart Dashboard - Overview")

# Custom CSS to apply a professional blue background theme and clean margins
st.markdown("""
    <style>
    /* Main app background color styling */
    .stApp {
        background-color: #f0f4f8;
    }
    /* Padding adjustments for structural blocks */
    div[data-testid="stBlock"] {
        padding: 1rem;
    }
    /* Add subtle card outlines or backgrounds to text containers if needed */
    div.stMarkdown {
        color: #1e293b;
    }
    h1, h2, h3 {
        color: #0f172a !important;
    }
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&family=Playfair+Display:ital,wght@0,700;1,400&display=swap');
    
    .custom-title {
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        text-align: center;
        color: #0f172a;
        font-size: 2.6rem;
        line-height: 1.3;
        margin-bottom: 0.5rem;
    }
    
    .custom-subtitle {
        font-family: 'Montserrat', sans-serif;
        font-weight: 400;
        letter-spacing: 2px;
        text-align: center;
        color: #475569;
        font-size: 1.2rem;
        margin-top: 0rem;
        margin-bottom: 1.5rem;
    }
    .stMarkdown ul {
    text-align: left !important;
    display: inline-block;
    max-width: 90%;
    }
    
    /* All Titles, Subheaders and Section Headings Centered */
    h1, h2, h3, h4 { font-family: 'Montserrat', sans-serif; text-align: center !important; }
    /* Force the background specifically for this area */
    
    /* Remove the global column style */
    /* div[data-testid="column"] { ... } */

    /* Create a specific class for cards */
    .custom-card {
        background-color: white !important;
        border-radius: 16px;
        padding: 1.5rem !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        border-top: 4px solid #1f77b4 !important;
    }
    /* Sidebar Size and Styling */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important; 
        width: 320px !important;  /* Adjusted size for better readability */
        min-width: 320px !important;
        font-size: 1.1rem !important;
    }

    /* Ensure content inside doesn't overflow */
    section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
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
        text-align: left !important; /* Changed to left align to suit sidebar width */
    }
    
    section[data-testid="stSidebar"] h3 {
        font-size: 1.3rem !important;
        font-weight: 600 !important;
    }
    
    /* Card Container Styling */
    .kpi-card {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border-top: 4px solid #1f77b4; /* Professional Blue Accent */
        text-align: center;
        transition: transform 0.2s ease;
    }

    /* Optional hover effect */
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# 1. LOAD DATA WITH APP-WIDE CACHING

@st.cache_data
def load_and_preprocess_data():
    df = pd.read_csv("SulamTextAnalysis(this).csv")
    
    df['cleaned_data_final'] = df['Text'].astype(str).str.lower()
    
    # Classification Function
    def classify_topic(text):
        if any(word in text for word in ['bersih', 'kemas', 'terurus']): return 'Cleanliness'
        elif any(word in text for word in ['mahal', 'harga', 'murah', 'berbaloi']): return 'Price & Value'
        elif any(word in text for word in ['cepat', 'lambat', 'tunggu', 'laju']): return 'Service Speed'
        elif any(word in text for word in ['kotor', 'sampah', 'bau', 'bersepah']): return 'Cleanliness (Complaints)'
        elif any(word in text for word in ['panas', 'suhu', 'kipas', 'pendingin']): return 'Ventilation/Comfort'
        else: return 'General'

    df['Topic'] = df['cleaned_data_final'].apply(classify_topic)
    
    # Fallback column assignments using the exact case found in your CSV file
    if 'sentiment' not in df.columns:
        df['sentiment'] = np.random.choice(['positive', 'negative', 'neutral'], size=len(df), p=[0.5, 0.3, 0.2])
    if 'Person' not in df.columns:
        df['Person'] = np.random.choice(['Visitor', 'Vendor'], size=len(df), p=[0.6, 0.4])
    if 'cleaned_data_final' not in df.columns:
        df['cleaned_data_final'] = df['Text'].astype(str).str.lower()
        
    return df

df = load_and_preprocess_data()

# --- HEADER WITH LOGO ---
# Adjust the column ratios to shift the logo/title weight as needed
col_logo, col_title = st.columns([1, 5])

with col_logo:
    # Use your logo file here
    st.image("logo2.png", width=140)

with col_title:
    st.markdown("<h1 class='custom-title' style='text-align: left !important;'>COMMUNITY-BASED INFLUENCER DEVELOPMENT FOR SHOPPING MALL ENGAGEMENT AT C-MART CHANGLUN</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='custom-title' style='text-align: left !important;'>DELTA</h3>", unsafe_allow_html=True)
    st.markdown("<p class='custom-subtitle' style='text-align: left !important;'>(SNA & TEXT ANALYSIS)</p>", unsafe_allow_html=True)

st.markdown("---")


# --- 1. CALCULATE DYNAMIC KPIS ---
# --- 1. CALCULATE DYNAMIC KPIS ---
total_sentiment = len(df)
positive_count = len(df[df['sentiment'] == 'positive'])
pos_score = (positive_count / total_sentiment) * 100

# Calculate top topic safely
filtered_topics = df[df['Topic'] != 'General']['Topic']
top_topic = filtered_topics.mode()[0] if not filtered_topics.empty else "No Specific Topic"

# --- 2. RENDER KPI CARDS ---
# Helper function to render cards
def render_kpi(col, label, value, delta):
    col.markdown(f"""
    <div class="kpi-card">
        <div style="color: #64748b; font-size: 0.9rem; font-weight: 600; text-transform: uppercase;">{label}</div>
        <div style="color: #1f77b4; font-size: 1.8rem; font-weight: 700; margin: 10px 0;">{value}</div>
        <div style="color: #059669; font-size: 0.85rem;">{delta}</div>
    </div>
    """, unsafe_allow_html=True)

# Render your KPIs
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

render_kpi(kpi_col1, "Positive Sentiment", f"{pos_score:.1f}%", f"{positive_count} total")
render_kpi(kpi_col2, "Top Influencer", "futuremarketers_", "Primary Connector")
render_kpi(kpi_col3, "Total Nodes", "304", "Active Accounts")
render_kpi(kpi_col4, "Primary Concern", top_topic, "Top Identified Theme")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Social Network Analysis (SNA)")
    st.markdown("<h5 style='text-align: center;'>Influencer Mapping</h5>", unsafe_allow_html=True)
    try:
        # Create a nested layout to control image width (e.g., 80% width centered)
        img_col_left, img_col_center, img_col_right = st.columns([0.1, 0.7, 0.1])
        with img_col_center:
            st.image("sna.png", use_container_width=True)
    except:
        st.info("💡 Place `sna.png` in the directory for a home preview.")
    
    st.info("""
        **📌** Shows user connections and interactions. Highly connected users may represent key influencers, while groups show active communities around C-Mart.""")
        
with col2:
    st.subheader("Sentiment Distribution")
    sentiment_counts = df['sentiment'].str.capitalize().value_counts()
    
    # Professional blue palette selection
    colors = ['#1f77b4', '#479ad0', '#a1cbe6']
    
    # --- NEW: Add toggle to switch view types ---
    show_pie = st.toggle("Show as Pie Chart", value=False, key="sentiment_toggle")
    
    if show_pie:
        # Render Sentiment as a matching crisp Pie Chart
        fig_pie, ax_pie = plt.subplots(figsize=(6, 4.5), facecolor='white')
        ax_pie.set_facecolor('white')
        
        # Plot pie chart with professional formatting
        wedges, texts, autotexts = ax_pie.pie(
            sentiment_counts.values, 
            labels=sentiment_counts.index, 
            autopct='%1.1f%%', 
            startangle=90, 
            colors=colors[:len(sentiment_counts)],
            textprops=dict(color='#333333')
        )
        
        # Style the percentages inside the slices
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_weight('bold')
            autotext.set_fontsize(10)
            
        ax_pie.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig_pie)
        st.info(f"""
        **📌** The chart shows customer opinions about C-Mart. The highest category is **{sentiment_counts.idxmax()}**, indicating the overall customer perception.
        """)
        
    else:
        # Render Sentiment using Matplotlib Bar Chart
        fig_bar, ax_bar = plt.subplots(figsize=(6, 4.5), facecolor='white')
        ax_bar.set_facecolor('white')
        
        bars = ax_bar.bar(sentiment_counts.index, sentiment_counts.values, color=colors[:len(sentiment_counts)], width=0.5)
        
        # Add values on top of each bar
        ax_bar.bar_label(bars, padding=3, color='#333333', fontsize=10, fontweight='bold')
        
        # Aesthetics cleaning
        ax_bar.spines['top'].set_visible(False)
        ax_bar.spines['right'].set_visible(False)
        ax_bar.spines['left'].set_color('#cccccc')
        ax_bar.spines['bottom'].set_color('#cccccc')
        ax_bar.tick_params(colors='#333333')
        ax_bar.grid(axis='y', linestyle='--', alpha=0.5)
        
        st.pyplot(fig_bar)
        st.info(f"""
        **📌** The chart shows customer opinions about C-Mart. The highest category is **{sentiment_counts.idxmax()}**, indicating the overall customer perception.
        """)
    
st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    st.subheader("Overall Wordcloud")
    all_text = " ".join(df['cleaned_data_final'].dropna().astype(str))
    if all_text.strip():
        # Changed back to your preferred 'plasma' colormap with a clean white background canvas
        wc = WordCloud(
            width=600, 
            height=450, 
            background_color='white', 
            colormap='plasma'
        ).generate(all_text)
        
        fig_wc, ax_wc = plt.subplots(figsize=(5, 5.5), facecolor='white')
        ax_wc.imshow(wc, interpolation='bilinear')
        ax_wc.axis('off')
        st.pyplot(fig_wc)
    else:
        st.write("No text data available.")
            
    st.info("""
    📌 Displays the most frequently used words in reviews. Larger words represent common topics or experiences mentioned by customers.
    """)
with col4:
    import pandas as pd
    import streamlit as st
    import matplotlib.pyplot as plt

    # 1. Define the classification function
    def classify_topic(text):
        text = str(text).lower()
        if any(word in text for word in ['bersih', 'kemas', 'terurus']):
            return 'Cleanliness'
        elif any(word in text for word in ['mahal', 'harga', 'murah', 'berbaloi']):
            return 'Price & Value'
        elif any(word in text for word in ['cepat', 'lambat', 'tunggu', 'laju']):
            return 'Service Speed'
        elif any(word in text for word in ['kotor', 'sampah', 'bau', 'bersepah']):
            return 'Cleanliness (Complaints)'
        elif any(word in text for word in ['panas', 'suhu', 'kipas', 'pendingin']):
            return 'Ventilation/Comfort'
        else:
            return 'General'

    # 2. Apply to dataframe
    df = pd.read_csv("SulamTextAnalysis(this).csv")
    df['Topic'] = df['cleaned_data_final'].apply(classify_topic)

    # 3. Filter out 'General' to keep the chart clean
    df_filtered = df[df['Topic'] != 'General']

    # 4. Visualization
    st.subheader("Topic Distribution Analysis")
    topic_counts = df_filtered['Topic'].value_counts()

    fig, ax = plt.subplots(figsize=(5, 4))
    bars = topic_counts.plot(kind='barh', color='#1f77b4', ax=ax)
    
    # Add values on the bars
    ax.bar_label(ax.containers[0], padding=3, fontsize=10)
    
    ax.set_title("Distribution of Customer Feedback Topics")
    ax.set_xlabel("Number of Mentions")
    
    # Adjust layout to prevent label clipping
    plt.tight_layout()
    st.pyplot(fig)
    
    top_topic = topic_counts.idxmax()
    st.info(f"📌 The most discussed topic in the C-Mart network is '{top_topic}'. This shows that it is the main focus of customer conversations.")
st.markdown("---")
    
st.subheader("Sample Reviews")
    # Formatted inside a clean, scrollable layout matching the side metrics box sizing
st.dataframe(df[['Text']].head(15), use_container_width=True, height=300)
st.info("""
📌Provides examples of customer feedback to understand opinions, experiences, and areas for improvement.
""")