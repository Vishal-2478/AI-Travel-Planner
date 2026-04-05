import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from serpapi import GoogleSearch
from datetime import datetime

# Load keys
# load_dotenv()

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
SERPAPI_KEY = st.secrets["SERPAPI_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)

# ---------- UI ----------
st.title("🌍 AI Travel Planner")

destination = st.text_input("Enter destination")
days = st.slider("Number of days", 1, 10, 3)
source = st.text_input("From (IATA code)", "BOM")
destination_code = st.text_input("To (IATA code)", "DEL")
budget = st.selectbox("Budget", ["Low", "Medium", "High"])
interests = st.text_area("Your interests")

# ---------- HELPER FUNCTIONS ----------


def format_time(time_str):
    try:
        dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        return dt.strftime("%I:%M %p")
    except:
        return "N/A"


def format_duration(minutes):
    try:
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours}h {mins}m"
    except:
        return "N/A"


def format_layovers(layovers):
    if not layovers:
        return "Non-stop"

    result = []
    for layover in layovers:
        name = layover.get("name", "Unknown")
        duration = layover.get("duration", 0)

        hours = duration // 60
        mins = duration % 60

        result.append(f"{name} ({hours}h {mins}m)")

    return " → ".join(result)


# ---------- SERPAPI ----------


def get_flights(source, destination):
    params = {
        "engine": "google_flights",
        "departure_id": source,
        "arrival_id": destination,
        "outbound_date": "2026-05-10",
        "return_date": "2026-05-15",
        "currency": "INR",
        "hl": "en",
        "gl": "in",
        "api_key": SERPAPI_KEY,
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    print("FULL RESPONSE:", results)

    return results.get("best_flights", [])


# ---------- AGENTS ----------


def research_agent(destination, interests):
    prompt = f"""
    Suggest best places in {destination}
    based on {interests}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def planner_agent(destination, days, budget, research):
    prompt = f"""
    Create {days}-day travel plan for {destination}
    Budget: {budget}

    Use this:
    {research}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


# ---------- BUTTON ----------

if st.button("Generate Plan"):

    st.write("✈️ Fetching flights...")
    flights = get_flights(source, destination_code)

    st.write("🔍 Researching...")
    research = research_agent(destination, interests)

    st.write("🗺️ Planning...")
    plan = planner_agent(destination, days, budget, research)

    # ---------- FLIGHTS UI ----------

    st.subheader("✈️ Flights")

    if flights:
        for i, flight in enumerate(flights[:3], 1):

            flights_info = flight.get("flights", [])
            if not flights_info:
                continue

            first_leg = flights_info[0]
            last_leg = flights_info[-1]

            # Airline
            airline = first_leg.get("airline", "N/A")

            # Departure
            dep_airport = first_leg.get("departure_airport", {}).get("name", "N/A")
            dep_time = format_time(
                first_leg.get("departure_airport", {}).get("time", "")
            )

            # Arrival
            arr_airport = last_leg.get("arrival_airport", {}).get("name", "N/A")
            arr_time = format_time(last_leg.get("arrival_airport", {}).get("time", ""))

            # Duration
            duration = format_duration(flight.get("total_duration", 0))

            # Price
            price = flight.get("price", "N/A")

            # Layovers
            layovers = format_layovers(flight.get("layovers", []))

            # ---------- CLEAN TEXT UI ----------
            st.markdown(f"### ✈️ Flight {i} — {airline}")

            col1, col2 = st.columns(2)

            with col1:
                st.write("🛫 **Departure**")
                st.write(dep_airport)
                st.write(dep_time)

            with col2:
                st.write("🛬 **Arrival**")
                st.write(arr_airport)
                st.write(arr_time)

            st.write("⏱ **Duration:**", duration)
            st.write("🛑 **Layovers:**", layovers)
            st.write("💰 **Price:** ₹", price)

            st.divider()

    else:
        st.warning("No flights found 😢")

    # ---------- OTHER OUTPUT ----------

    st.subheader("📍 Places")
    st.write(research)

    st.subheader("🗺️ Plan")
    st.write(plan)
