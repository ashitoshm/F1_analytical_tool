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
st.title("Driver Ananlysis Dashboard")


season = st.sidebar.selectbox("Select Season", list(range(2000, 2025))[::-1])


driver_standings_query = f'''
SELECT DISTINCT ON (driver_name) 
    driver_name,
    constructor,
    points AS season_points
FROM driver_standings
WHERE year = {season}
ORDER BY driver_name, season_points DESC, constructor;
'''
df_standings = fetch_data(driver_standings_query)

st.subheader(f"🏆 Driver Standings for {season}")
st.dataframe(df_standings, hide_index=True, use_container_width=True)


standings_evolution_query = f'''
    SELECT round, driver_name, position
    FROM driver_standings
    WHERE year = {season}
    ORDER BY round, position;
'''
df_evolution = fetch_data(standings_evolution_query)

st.subheader(f"📈 Drivers Ranking Evolution Chart")

selected_drivers = st.multiselect("Select Drivers", df_evolution['driver_name'].unique(), default=df_evolution['driver_name'].unique()[:5])
df_filtered = df_evolution[df_evolution['driver_name'].isin(selected_drivers)]


highlight_round = st.slider("Select Round to Highlight", min_value=int(df_evolution["round"].min()), max_value=int(df_evolution["round"].max()), value=int(df_evolution["round"].max()/2))


fig_evolution = px.line(df_filtered, x="round", y="position", color="driver_name", line_dash="driver_name")
fig_evolution.update_yaxes(autorange="reversed")


fig_evolution.add_vrect(
    x0= highlight_round - 0.4, x1=highlight_round + 0.4, 
    fillcolor="blue", opacity=0.3, line_width=0
)


st.plotly_chart(fig_evolution, use_container_width=True)

st.subheader(f"💪 Wins, Podiums, DNFs and Finishes in Points")

stats_query = f'''
    SELECT driver_name,
        COUNT(CASE WHEN win = 1 THEN 1 ELSE NULL END) AS wins,
        COUNT(CASE WHEN podium = 1 THEN 1 ELSE NULL END) AS podiums,
        COUNT(CASE WHEN points_finish = 1 THEN 1 ELSE NULL END) AS finishes_in_points,
        COUNT(CASE WHEN status = 'DNF' THEN 1 ELSE NULL END) AS dnfs
    FROM final_f1
    WHERE year = {season}
    GROUP BY driver_name;
'''
df_stats = fetch_data(stats_query)


custom_colors = {
    "wins": "green",         
    "podiums": "blue",        
    "dnfs": "red",            
    "finishes_in_points": "orange"  
}


df_long = df_stats.melt(id_vars=["driver_name"], 
                        value_vars=["wins", "podiums", "dnfs", "finishes_in_points"], 
                        var_name="Metric", 
                        value_name="Count")


fig_stats = px.bar(df_long, 
                   x="driver_name", 
                   y="Count", 
                   color="Metric", 
                   barmode="group", 
                   color_discrete_map=custom_colors) 


st.plotly_chart(fig_stats, use_container_width=True)

st.markdown("---")
st.write("Fernando Alonso is just an rookie 🔰")
