import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import os 
from db_config import get_db_engine

engine = get_db_engine()

def fetch_data(query):
    """Fetch data from the database."""
    with engine.connect() as connection:
        return pd.read_sql(query, connection)


st.set_page_config(page_title="F1 Dashboard", layout="wide")
st.title("Constructors Ananlysis Dashboard")


season = st.sidebar.selectbox("Select Season", list(range(2000, 2025))[::-1])


constructor_standings_query = f'''
SELECT constructor, MAX(points) AS season_points
FROM constructor_standings
WHERE year = {season}
GROUP BY constructor
ORDER BY season_points DESC;
'''
df_standings = fetch_data(constructor_standings_query)

st.subheader(f"🏆 constructors Standings for {season}")
st.dataframe(df_standings, hide_index=True, use_container_width=True)


constructors_evolution_query = f'''
    SELECT round, constructor, position
    FROM constructor_standings
    WHERE year = {season}
    ORDER BY round, position;
'''
df_evolution = fetch_data(constructors_evolution_query)

st.subheader(f"📈 Constructors Ranking Evolution Chart")

selected_constructor = st.multiselect("Select constructor", df_evolution['constructor'].unique(), default=df_evolution['constructor'].unique()[:5])
df_filtered = df_evolution[df_evolution['constructor'].isin(selected_constructor)]


highlight_round = st.slider("Select Round to Highlight", min_value=int(df_evolution["round"].min()), max_value=int(df_evolution["round"].max()), value=int(df_evolution["round"].max()/2))


fig_evolution = px.line(df_filtered, x="round", y="position", color="constructor", line_dash="constructor")
fig_evolution.update_yaxes(autorange="reversed")


fig_evolution.add_vrect(
    x0= highlight_round - 0.4, x1=highlight_round + 0.4,  
    fillcolor="blue", opacity=0.3, line_width=0
)


st.plotly_chart(fig_evolution, use_container_width=True)

st.subheader(f"💪 Wins, Podiums, DNFs and Finishes in Points")

stats_query = f'''
    SELECT constructor,
        COUNT(CASE WHEN win = 1 THEN 1 ELSE NULL END) AS wins,
        COUNT(CASE WHEN podium = 1 THEN 1 ELSE NULL END) AS podiums,
        COUNT(CASE WHEN points_finish = 1 THEN 1 ELSE NULL END) AS finishes_in_points,
        COUNT(CASE WHEN status = 'DNF' THEN 1 ELSE NULL END) AS dnfs
    FROM final_f1
    WHERE year = {season}
    GROUP BY constructor;
'''
df_stats = fetch_data(stats_query)


custom_colors = {
    "wins": "green",          
    "podiums": "blue",       
    "dnfs": "red",            
    "finishes_in_points": "orange"  
}


df_long = df_stats.melt(id_vars=["constructor"], 
                        value_vars=["wins", "podiums", "dnfs", "finishes_in_points"], 
                        var_name="Metric", 
                        value_name="Count")


fig_stats = px.bar(df_long, 
                   x="constructor", 
                   y="Count", 
                   color="Metric",  
                   barmode="group", 
                   color_discrete_map=custom_colors)  


st.plotly_chart(fig_stats, use_container_width=True)

st.markdown("---")
st.write("Fernando Alonso is just an rookie 🔰")
