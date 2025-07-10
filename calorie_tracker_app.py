# Mallikarjun Simple Calorie Tracker (Streamlit for Android)

import streamlit as st
import sqlite3
from datetime import datetime

# --- DB Setup ---
conn = sqlite3.connect("calorie_tracker.db", check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS meals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    meal TEXT,
    calories REAL,
    protein REAL,
    carbs REAL,
    fat REAL,
    fiber REAL
)''')
conn.commit()

# --- Simple Mock Estimator ---
def estimate_nutrition(meal_desc):
    return {
        "Calories": 350,
        "Protein": 20,
        "Fat": 10,
        "Carbs": 40,
        "Fiber": 8
    }

# --- Streamlit App ---
st.set_page_config(page_title="Mallikarjun Tracker", layout="centered")
st.title("🍽️ Simple Calorie Tracker")

meal = st.text_input("What did you eat?", "e.g. 2 chapatis and egg curry")
if st.button("Log Meal") and meal:
    data = estimate_nutrition(meal)
    c.execute("INSERT INTO meals (date, meal, calories, protein, carbs, fat, fiber) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (datetime.now().date(), meal, data['Calories'], data['Protein'], data['Carbs'], data['Fat'], data['Fiber']))
    conn.commit()
    st.success("Meal Logged!")
    st.write("Nutrition Estimate:", data)

# --- Summary ---
st.markdown("---")
st.header("Today's Summary")
c.execute("SELECT meal, calories, protein, carbs, fat, fiber FROM meals WHERE date = ?", (datetime.now().date(),))
rows = c.fetchall()

if rows:
    total = [0]*5
    for row in rows:
        st.write("•", row[0])
        total = [t + float(v) for t, v in zip(total, row[1:])]

    st.markdown("---")
    st.metric("Total Calories", f"{total[0]} kcal")
    st.metric("Protein", f"{total[1]} g")
    st.metric("Carbs", f"{total[2]} g")
    st.metric("Fat", f"{total[3]} g")
    st.metric("Fiber", f"{total[4]} g")
else:
    st.info("No meals logged yet today.")
