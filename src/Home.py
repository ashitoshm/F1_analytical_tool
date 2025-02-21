import streamlit as st
from PIL import Image

def home_page():
   
    st.set_page_config(
        page_title="F1 Analytics Dashboard",
        page_icon="🏎️",
        layout="wide"
    )

   
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.title("🏎️ Formula 1 Analytics Dashboard")
        st.markdown("""
        Welcome to the comprehensive F1 Analytics Dashboard! This tool provides detailed insights 
        into Formula 1 championship standings and performance metrics.
        """)

    
    st.markdown("## 📊 Available Modules")

    
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 🏃 Drivers Standings
        """)
        st.markdown("""
        Explore detailed driver statistics including:
        - Current championship standings
        - Points progression
        - Performance metrics
        - Head-to-head comparisons
        """)
        if st.button("Go to Drivers Analysis", key="drivers_btn"):
            st.switch_page("pages/Drivers_Standing.py")

    with col2:
        st.markdown("""
        ### 🏭 Constructors Standings
        """)
        st.markdown("""
        Analyze team performance through:
        - Team championship standings
        - Constructor point trends
        - Team comparisons
        - Performance analytics
        """)
        if st.button("Go to Constructors Analysis", key="constructors_btn"):
            st.switch_page("pages/Constructors_standings.py")

   
    st.markdown("---")
    st.markdown("## 📌 Quick Tips")
    
    # Create three columns for tips
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 💡 Data Updates
        The dashboard contains data of seasons from 2000 to 2024. 
        """)
    
    with col2:
        st.markdown("""
        ### 🔍 Interactive Features
        Use filters and interactive elements in each module to customize your analysis view.
        """)
    
    with col3:
        st.markdown("""
        ### 📊 Visualization Options
        Switch between different chart types to view data from multiple perspectives.
        """)

   
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <p>Built with ❤️ for F1 fans </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    home_page()