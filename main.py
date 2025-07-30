import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
from datetime import date, datetime, timezone
import os
import streamlit.web.bootstrap

# --- CONFIGURATION ---
st.set_page_config(page_title='🚀 NASA Space Explorer', layout='centered')
api_key = "dapyTTHF8ioAavC7Lnc8TZPlMnAFg8jZLvPOeB8j"

# --- HEADER ---
st.title("🚀 NASA Space Explorer")
st.markdown("Explore the cosmos through NASA APIs — APOD, Mars rover photos, news, and location-based tools.")

# --- SIDEBAR MENU ---
selected_feature = st.sidebar.selectbox("🔭 Choose a Feature", [
    "Astronomy Picture of the Day",
    "Mars Rover Photos",
    "Space News Feed",
    "Location Map Tool"
])

# --- FEATURE 1: Astronomy Picture of the Day ---
if selected_feature == "Astronomy Picture of the Day":
    st.subheader("🌌 Astronomy Picture of the Day")

    st.write("Pick a date to view the NASA Astronomy Picture of the Day:")
    selected_date = st.date_input("Select a date", value=date.today())

    if selected_date:
        url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}&date={selected_date}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if data["media_type"] == "image":
                st.image(data.get("url"), caption=data.get("title"), use_container_width=True)
            elif data["media_type"] == "video":
                st.video(data.get("url"))
            else:
                st.warning("Media type not supported.")

            st.subheader("📖 Explanation")
            st.write(data.get("explanation"))
        else:
            st.error("Failed to fetch APOD. Try another date (APOD started June 16, 1995).")

# --- FEATURE 2: Mars Rover Photos ---
elif selected_feature == "Mars Rover Photos":
    st.subheader("🪐 Mars Rover Photo Explorer")

    st.write("Choose a rover and Martian Sol (a solar day on Mars) to see real photos:")
    rover = st.selectbox("🔧 Choose Rover", ["Curiosity", "Opportunity", "Spirit"])
    sol = st.number_input("🔢 Enter Martian Sol", min_value=0, max_value=5000, value=1000)

    if st.button("Get Mars Photos"):
        url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos?sol={sol}&api_key={api_key}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            photos = data.get("photos", [])
            if photos:
                for photo in photos[:10]:  # Limit to 10 for performance
                    st.image(photo["img_src"], caption=f"{photo['camera']['full_name']} ({photo['earth_date']})",
                             use_container_width=True)
            else:
                st.warning("No photos found for that Sol. Try a different day.")
        else:
            st.error("Failed to fetch Mars photos. Check your internet or try again later.")

# --- FEATURE 3: Space News Feed ---
elif selected_feature == "Space News Feed":
    st.subheader("📰 Space News Feed")

    if st.button("Load Today's Space News"):
        url = "https://api.spaceflightnewsapi.net/v4/articles/?limit=20"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            articles = data.get("results", [])

            today = datetime.now(timezone.utc).date().isoformat()
            todays_articles = [article for article in articles if article["published_at"].startswith(today)]

            if todays_articles:
                for article in todays_articles:
                    st.markdown(f"### [{article['title']}]({article['url']})")
                    if article["image_url"]:
                        st.image(article["image_url"], width=600)
                    st.write(f"🕒 Published: {article['published_at']}")
                    st.write(article['summary'][:200] + "...")
                    st.markdown("---")
            else:
                st.info("No new articles published today. Come back tomorrow!")
        else:
            st.error("Unable to fetch space news.")

# --- FEATURE 4: Location Map Tool ---
elif selected_feature == "Location Map Tool":
    st.subheader("🌍 Location Map Tool")
    st.write("Click on the map to get latitude and longitude for any place on Earth.")

    # Initialize folium map
    m = folium.Map(location=[9.0820, 8.6753], zoom_start=5)
    m.add_child(folium.LatLngPopup())
    output = st_folium(m, width=None, height=500)

    if output["last_clicked"] is not None:
        lat = output["last_clicked"]["lat"]
        lon = output["last_clicked"]["lng"]
        st.success(f"📍 Selected Coordinates: Latitude = {lat:.4f}, Longitude = {lon:.4f}")
        st.markdown("You can now use this in APIs like weather, ISS tracker, or space imagery.")
    else:
        st.info("Click anywhere on the map to get coordinates.")

# --- ABOUT SECTION ---
with st.expander("ℹ️ About This App"):
    st.markdown("""
        **NASA Space Explorer** is a simple app powered by public APIs from NASA and Spaceflight News.

        Features:
        - Astronomy Picture of the Day (APOD)
        - Mars Rover Photos
        - Real-time Space News Feed
        - Interactive Earth Map Tool

        Built with ❤️ using Streamlit and curiosity.
    """)

port = int(os.environ.get("PORT", 8501))
script_path = "main.py"  # or whatever your actual file is

streamlit.web.bootstrap.run(script_path, [], {})


