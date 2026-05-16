import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
data = pd.read_csv("Students Social Media Addiction.csv")

# Set page config
st.set_page_config(page_title="Social Media Dashboard", layout="wide")

# Custom CSS for styling
page_bg_style = """
<style>
    .stApp {
        background-color: #000000;
        color: #F0E6F6;
        font-family: 'Segoe UI', sans-serif;
    }
    [data-testid="stSidebar"] {
        background-color: #121212;
        color: #E1C6F6;
    }
    .kpi {
        color: #F0E6F6;
    }
    hr {
        border: 1.5px solid #BB86FC;
    }
</style>
"""
st.markdown(page_bg_style, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title('📊 Social Media Dashboard')
    gender_filter = st.multiselect('Select Gender', options=data['Gender'].unique(), default=data['Gender'].unique())
    academic_filter = st.multiselect('Select Academic Level', options=data['Academic_Level'].unique(), default=data['Academic_Level'].unique())
    relationship_filter = st.multiselect('Select Relationship Status', options=data['Relationship_Status'].unique(), default=data['Relationship_Status'].unique())
    st.markdown("---")
    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis', 'purples']
    selected_color_theme = st.selectbox('🎨 Select Heatmap Color Theme', color_theme_list, index=color_theme_list.index('purples'))
    st.caption("🎯 Theme applies to the heatmap only.")

# Filter data
filtered_data = data[
    (data['Gender'].isin(gender_filter)) &
    (data['Academic_Level'].isin(academic_filter)) &
    (data['Relationship_Status'].isin(relationship_filter))
]

# Header
st.title("📱 Social Media Addiction Among Students")
st.info("👉 Use the filters in the **sidebar** to explore the data by gender, academic level, and relationship status.")

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
def metric_card(label, value, color, emoji, is_int=False):
    formatted_value = f"{int(value)}" if is_int else f"{value:.2f}"
    return f"""
    <div style="
        background-color: {color};
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.7);
        font-weight: 700;
        font-size: 12px;
    ">
        {emoji} {label}<br>
        <span style="font-size: 40px;">{formatted_value}</span>
    </div>
    """

with col1:
    st.markdown(metric_card("Addiction Score", filtered_data['Addicted_Score'].mean(), "#BB86FC", "📱"), unsafe_allow_html=True)
with col2:
    st.markdown(metric_card("Daily Usage (hours)", filtered_data['Avg_Daily_Usage_Hours'].mean(), "#F48FB1", "⏰"), unsafe_allow_html=True)
with col3:
    st.markdown(metric_card("Mental Health Score", filtered_data['Mental_Health_Score'].mean(), "#CE93D8", "🧠"), unsafe_allow_html=True)
with col4:
    st.markdown(metric_card("Total Students", len(filtered_data), "#9575CD", "👥", is_int=True), unsafe_allow_html=True)

st.markdown("---")

# Charts
col5, col6, col7 = st.columns(3)

with col5:
    fig = px.scatter(
        filtered_data,
        x='Addicted_Score',
        y='Mental_Health_Score',
        color='Gender',
        title='📉 Addiction Score vs Mental Health Score',
        template='plotly_white',
        hover_data=filtered_data.columns,
        color_discrete_map={'Female': '#FADADD', 'Male': '#B0E0E6'}
    )
    st.plotly_chart(fig, use_container_width=True)

with col6:
    fig = px.histogram(
        filtered_data,
        x='Avg_Daily_Usage_Hours',
        nbins=10,
        title='⏰ Distribution of Daily Usage (hrs)',
        template='plotly_white',
        color_discrete_sequence=['#FFDDEE'],
        hover_data=filtered_data.columns
    )
    st.plotly_chart(fig, use_container_width=True)

with col7:
    fig = px.histogram(
        filtered_data,
        x='Addicted_Score',
        color='Gender',
        barmode='group',
        title='📱 Addiction Level by Gender',
        template='plotly_white',
        color_discrete_map={'Female': '#FADADD', 'Male': '#B0E0E6'},
        hover_data=filtered_data.columns
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
col8, col9, col10 = st.columns(3)

with col8:
    platform_counts = filtered_data['Most_Used_Platform'].value_counts().reset_index()
    platform_counts.columns = ['Platform', 'Count']
    pastel_colors = ["#FFD1DC", "#AEC6CF", "#FFB347", "#B39EB5", "#AAF0D1", "#ACE1AF", "#CBAACB", "#FF6961"]
    fig = px.pie(
        platform_counts,
        names='Platform',
        values='Count',
        title='📌 Most Used Social Media Platforms',
        template='plotly_white',
        color_discrete_sequence=pastel_colors
    )
    st.plotly_chart(fig, use_container_width=True)

with col9:
    fig = px.scatter(
        filtered_data,
        x='Avg_Daily_Usage_Hours',
        y='Sleep_Hours_Per_Night',
        color='Gender',
        size='Addicted_Score',
        title='🌙 Sleep Hours vs Daily Usage',
        template='plotly_white',
        color_discrete_map={'Female': '#FADADD', 'Male': '#B0E0E6'},
        hover_data=filtered_data.columns
    )
    st.plotly_chart(fig, use_container_width=True)

with col10:
    academic_data = pd.crosstab(
        filtered_data['Most_Used_Platform'],
        filtered_data['Affects_Academic_Performance']
    ).reset_index()

    melted = academic_data.melt(id_vars='Most_Used_Platform', var_name='Impact', value_name='Count')

    fig = px.bar(
        melted,
        x="Most_Used_Platform",
        y="Count",
        color="Impact",
        barmode="stack",
        title="🎓 Academic Performance Impact by Platform",
        template='plotly_white',
        color_discrete_map={'Yes': '#FFA6A6', 'No': '#FFFDD0'},
        hover_data=melted.columns
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

# Correlation Heatmap
st.markdown("---")
st.subheader("📊 Correlation Heatmap")

corr_data = filtered_data[[
    'Addicted_Score',
    'Mental_Health_Score',
    'Avg_Daily_Usage_Hours',
    'Sleep_Hours_Per_Night',
    'Conflicts_Over_Social_Media'
]]
corr_matrix = corr_data.corr().round(2)

fig = px.imshow(
    corr_matrix,
    text_auto=True,
    color_continuous_scale=selected_color_theme,
    title="🔗 Correlation Between Key Metrics",
    labels=dict(color='Correlation')
)

fig.update_layout(
    width=700,
    height=500,
    margin=dict(l=50, r=50, t=80, b=50),
    font=dict(color="white"),
    paper_bgcolor="#000000",
    plot_bgcolor="#000000"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
🟪 **How to Read the Heatmap:**
- **+1.00** = Strong positive link (both increase)
- **0.00** = No relationship
- **–1.00** = One goes up, the other goes down
""")
