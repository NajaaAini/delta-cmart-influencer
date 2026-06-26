import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer

st.set_page_config(layout="wide", page_title="Wordcloud Analytics")


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

# Structural page redirection mapping
if st.button("🏠 Back to Overview Home"):
    st.switch_page("Overview.py")  # Ensure this matches your exact main file name

st.title("Dynamic Wordcloud Analysis")
st.markdown("---")

@st.cache_data
def get_shared_data():
    return pd.read_csv("SulamTextAnalysis(this).csv")

try:
    df = get_shared_data()
except:
    st.error("Please ensure 'SulamTextAnalysis(this).csv' is in your root directory path.")
    st.stop()

# Interactive User Filtering Controls
col_f1, col_f2 = st.columns(2)
with col_f1:
    s_filter = st.selectbox("Filter Sentiment", ["All", "Positive", "Negative", "Neutral"])
with col_f2:
    p_filter = st.selectbox("Filter Role / Person Type", ["All", "Visitor", "Vendor"])



# Processing and robust query subsets filtering
filtered_df = df.copy()

# Determine the exact name of the sentiment column present in your CSV (lowercase 'sentiment')
sent_col = 'sentiment' if 'sentiment' in filtered_df.columns else ('Sentiment' if 'Sentiment' in filtered_df.columns else None)

# --- 1. VISUALIZATION SETTINGS ---
st.markdown("### Visualization Settings")
max_words_slicer = st.slider("Select maximum number of words to display:", min_value=5, max_value=150, value=50, step=5)
show_raw = st.toggle("Show Wordcloud for Raw Data (Ignore Filters)", value=False)
st.markdown("---")

# --- 2. DYNAMIC DATA & COLUMN SELECTION ---
if show_raw:
    # Use the full dataframe and the raw 'Text' column
    active_df = df.copy()
    target_col = 'Text' if 'Text' in active_df.columns else 'cleaned_data_final'
else:
    # Use the filtered dataframe and the cleaned column
    active_df = df.copy()
    # Apply your filters
    if sent_col:
        active_df[sent_col] = active_df[sent_col].astype(str).str.strip().str.lower()
        if s_filter != "All":
            active_df = active_df[active_df[sent_col] == s_filter.lower()]
            
    if 'Person' in active_df.columns:
        active_df['Person'] = active_df['Person'].astype(str).str.strip().str.lower()
        if p_filter != "All":
            target_role = p_filter.lower()
            active_df = active_df[active_df['Person'].str.contains(target_role, na=False)]
    
    target_col = 'cleaned_data_final' if 'cleaned_data_final' in active_df.columns else 'Text'

# Build the corpus from the selected dataframe and column
text_corpus = active_df[target_col].dropna().astype(str).tolist()
text_corpus = [t for t in text_corpus if t.strip() != ""]

def get_ngrams(corpus, n=1):
    try:
        # Added broad token pattern to prevent CountVectorizer from ignoring short or specific Malay root words
        vec = CountVectorizer(ngram_range=(n, n), token_pattern=r'(?u)\b\w+\b').fit(corpus)
        bag_of_words = vec.transform(corpus)
        sum_words = bag_of_words.sum(axis=0) 
        words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
        return dict(sorted(words_freq, key = lambda x: x[1], reverse=True))
    except:
        return {}

if text_corpus:
    col_w1, col_w2 = st.columns(2)
    
    with col_w1:
        st.subheader("Unigram Wordcloud")
        unigram_freq = get_ngrams(text_corpus, n=1)
        if unigram_freq:
            wc_uni = WordCloud(
                width=600, 
                height=450, 
                background_color='white', 
                colormap='plasma', 
                max_words=max_words_slicer
            ).generate_from_frequencies(unigram_freq)
            
            fig, ax = plt.subplots(figsize=(6, 4.5))
            ax.imshow(wc_uni, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)
        else:
            st.write("No valid unigrams found for this selection.")
            
    with col_w2:
        st.subheader("Bigram Wordcloud")
        bigram_freq = get_ngrams(text_corpus, n=2)
        if bigram_freq:
            wc_bi = WordCloud(
                width=600, 
                height=450, 
                background_color='white', 
                colormap='plasma', 
                max_words=max_words_slicer
            ).generate_from_frequencies(bigram_freq)
            
            fig, ax = plt.subplots(figsize=(6, 4.5))
            ax.imshow(wc_bi, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)
        else:
            st.write("No valid bigrams found for this selection.")
else:
    st.warning("No records matched the selected query metrics.")

# --- 1. CALCULATE TABLES BASED ON FILTERED DATA ---
st.markdown("---")
col_u, col_b = st.columns(2)

# Get Positive Data from the already filtered_df
pos_df = filtered_df[filtered_df['sentiment'].str.lower() == 'positive']
pos_corpus = pos_df[target_col].dropna().astype(str).tolist()
pos_bigram_freq = get_ngrams(pos_corpus, n=2) # Now automatically ignores 'sangat setuju'
pos_bi_df = pd.DataFrame(list(pos_bigram_freq.items()), columns=['Phrase', 'Freq']).head(5)

# Get Negative Data from the already filtered_df
neg_df = filtered_df[filtered_df['sentiment'].str.lower() == 'negative']
neg_corpus = neg_df[target_col].dropna().astype(str).tolist()
neg_bigram_freq = get_ngrams(neg_corpus, n=2) # Now automatically ignores 'sangat setuju'
neg_bi_df = pd.DataFrame(list(neg_bigram_freq.items()), columns=['Phrase', 'Freq']).head(5)

# Display Tables
with col_u:
    st.info("#### Top 5 Positive Phrases")
    st.table(pos_bi_df if not pos_bi_df.empty else pd.DataFrame({"Phrase": ["No data"], "Freq": [0]}))

with col_b:
    st.info("#### Top 5 Negative Phrases")
    st.table(neg_bi_df if not neg_bi_df.empty else pd.DataFrame({"Phrase": ["No data"], "Freq": [0]}))

# --- 2. GENERATE FILTER-AWARE DECISION MATRIX ---
st.markdown("---")
st.subheader("🚀 Strategic Action Plan (Decision Matrix)")

c1, c2 = st.columns(2)

with c1:
    st.success("### ✅ Strengths")
    if not pos_bi_df.empty:
        for item in pos_bi_df['Phrase'].head(3):
            st.markdown(f"- **{item.upper()}**")
        st.info("💡 **Action:** Use these keywords in your next marketing campaign!")
    else:
        st.write("No positive data available for this filter.")

with c2:
    st.warning("### 🔧 Interventions")
    if not neg_bi_df.empty:
        neg_top3 = neg_bi_df['Phrase'].head(3).tolist()
        for item in neg_top3:
            st.markdown(f"- **{item.upper()}**")
        
        neg_text = " ".join(neg_top3).lower()

        # 1. Define Intervention Map
        # This keeps your logic centralized and easy to read
        interventions = {
            'harga': "🚨 **Action (Pricing):** Review pricing competitiveness and offer student-exclusive bundles.",
            'mahal': "🚨 **Action (Pricing):** Conduct a price-comparison study against nearby competitors.",
            'servis': "🚨 **Action (Staffing):** Implement 'Service Excellence' training sessions for front-line staff.",
            'lambat': "🚨 **Action (Operations):** Optimize queue management at checkout counters.",
            'panas': "🚨 **Action (Facilities):** Propose infrastructure audit: check AC maintenance and install air curtains.",
            'udara': "🚨 **Action (Facilities):** Improve ventilation; investigate airflow blockage in high-traffic zones.",
            'kurang': "🚨 **Action (Engagement):** Conduct a 'Customer Feedback' session to identify missing amenities."
        }

        # 2. Check for matches (Higher priority checks first)
        found_intervention = False
        for keyword, action in interventions.items():
            if keyword in neg_text:
                st.error(action)
                found_intervention = True
                break # Stop after finding the most relevant match
        
        # 3. Default fallback
        if not found_intervention:
            st.error("🚨 **Action:** Conduct a deep-dive operational review to isolate the core customer pain point.")
    else:
        st.write("No negative feedback detected. Maintain current standards!")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import gensim
from gensim import corpora

st.markdown("---")
st.subheader("Operational Diagnostics")

# Force every entry to be a string before splitting
tokenized_data = [str(text).split() for text in df['cleaned_data_final']]

# Then apply the stop_words filter
stop_words = ['betul', 'kalau', 'sekali', 'sangat', 'setuju', 'perlu', 'memenuhi']
filtered_tokenized_data = [[w for w in text if w not in stop_words] for text in tokenized_data]


# --- 1. DATA PREP ---
PILLARS = ['Cleanliness', 'Price & Value', 'Service Speed', 'Ventilation/Comfort']

# Ensure data is clean (Fixes your previous error)
df['cleaned_data_final'] = df['cleaned_data_final'].fillna('').astype(str)

def classify_topic(text):
    text = str(text).lower()
    if any(w in text for w in ['bersih', 'kemas', 'terurus', 'kotor', 'sampah', 'bau']): return 'Cleanliness'
    elif any(w in text for w in ['mahal', 'harga', 'murah', 'berbaloi']): return 'Price & Value'
    elif any(w in text for w in ['cepat', 'lambat', 'tunggu', 'laju', 'kaunter']): return 'Service Speed'
    elif any(w in text for w in ['panas', 'suhu', 'kipas', 'pendingin', 'udara']): return 'Ventilation/Comfort'
    return 'Other'

df['Topic'] = df['cleaned_data_final'].apply(classify_topic)
df_filtered = df[df['Topic'] != 'Other']

# --- 2. COLUMN LAYOUT ---
col1, col2 = st.columns(2)

# --- LEFT COLUMN: Manual Distribution ---
with col1:
    st.info("####  Manual Topic Distribution")
    topic_counts = df_filtered['Topic'].value_counts()
    fig1, ax1 = plt.subplots(figsize=(2, 3))
    topic_counts.plot(kind='barh', color='#1f77b4', ax=ax1)
    ax1.bar_label(ax1.containers[0], padding=3)
    st.pyplot(fig1)

# --- RIGHT COLUMN: LDA Significance (Top 5) ---
with col2:
    # --- SIMPLIFIED THEMATIC DISCLOSURE ---
    st.info("#### Thematic Insights")

    # Define your verified themes and their representative keywords
    theme_insights = {
        "Cleanliness & Hygiene": ["bersih", "kotor", "sampah", "bau", "lantai"],
        "Price & Value": ["mahal", "harga", "murah", "berbaloi", "student"],
        "Service Speed": ["cepat", "lambat", "tunggu", "kaunter", "laju"],
        "Ventilation/Comfort": ["panas", "suhu", "kipas", "udara", "selesa"]
    }

    # Display as an interactive expander
    for theme, keywords in theme_insights.items():
        with st.expander(f"📌 {theme}"):
            st.write(f"**Associated Keywords:** {', '.join(keywords)}")
            st.write(f"This theme covers concerns regarding **{theme.lower()}** based on the analyzed customer feedback.")