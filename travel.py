import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime
import folium
from streamlit_folium import st_folium

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

st.set_page_config(page_title="Travel Safety Explorer", layout="wide")

@st.cache_data(show_spinner=False)
def get_country_info(country_name):
    try:
        url = f"https://restcountries.com/v3.1/name/{country_name}"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()[0]
        info = {
            "name": data.get("name", {}).get("common"),
            "capital": ", ".join(data.get("capital", [])),
            "latlng": data.get("latlng", [0,0]),
            "population": data.get("population"),
            "languages": ", ".join(data.get("languages", {}).values()) if data.get("languages") else "",
            "flag": data.get("flags", {}).get("png"),
        }
        return info
    except:
        return {"error": "Country not found"}

@st.cache_data(show_spinner=False)
def fetch_news(query, page_size=10):
    if not NEWSAPI_KEY:
        return {"error": "NEWSAPI_KEY not set"}
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "pageSize": page_size,
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": NEWSAPI_KEY,
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}

# Embassy Contacts (sample dataset)
EMBASSY_DB = {
    "Japan": {"phone": "+81-3-3452-7611", "address": "1-2-5 Minato-ku, Tokyo"},
    "Philippines": {"phone": "+63-2-856-9210", "address": "122 Upper McKinley Rd, Taguig"},
    "South Korea": {"phone": "+82-2-3210-0400", "address": "Seoul Government Complex"},
}

# Safety Scores (sample, 1~100)
SAFETY_SCORES = {
    "Japan": {"도쿄": 88, "오사카": 82, "삿포로": 90},
    "Philippines": {"마닐라": 45, "세부": 60, "보라카이": 70},
    "South Korea": {"서울": 92, "부산": 85, "제주": 95},
}

st.title("🌍 Travel Safety Explorer (확장 버전)")

with st.sidebar:
    country = st.text_input("국가명 입력", value="Japan")
    max_news = st.slider("뉴스 표시 개수", 1, 20, 5)
    include_disaster = st.checkbox("재난 뉴스 포함", True)

info = get_country_info(country)

if info.get("error"):
    st.error("국가 정보를 찾을 수 없습니다.")
else:
    st.subheader(f"국가 기본 정보 — {info['name']}")
    st.markdown(f"**수도:** {info['capital']}")
    st.markdown(f"**인구:** {info['population']:,}")
    st.markdown(f"**언어:** {info['languages']}")
    if info.get("flag"):
        st.image(info['flag'], width=150)

    st.markdown("---")

    # Embassy Info
    st.header("📞 대사관 연락처")
    embassy = EMBASSY_DB.get(info["name"])
    if embassy:
        st.markdown(f"**전화번호:** {embassy['phone']}")
        st.markdown(f"**주소:** {embassy['address']}")
    else:
        st.info("대사관 정보가 없습니다. 추가 데이터가 필요합니다.")

    st.markdown("---")

    # Safety Scores
    st.header("🛡 지역별 안전 점수")
    regions = SAFETY_SCORES.get(info["name"], {})
    if regions:
        df_score = pd.DataFrame({"지역": list(regions.keys()), "안전점수": list(regions.values())})
        st.bar_chart(df_score.set_index("지역"))
    else:
        st.info("안전 점수 데이터 없음.")

    st.markdown("---")

    # Map
    st.header("🗺 국가 지도")
    lat, lng = info["latlng"]
    country_map = folium.Map(location=[lat, lng], zoom_start=5)
    folium.Marker([lat, lng], tooltip=f"Capital: {info['capital']}").add_to(country_map)
    st_folium(country_map, width=700, height=450)

    st.markdown("---")

    # Crime News
    st.header("🚨 최신 범죄 뉴스")
    crime_query = f"{country} crime OR robbery OR assault"
    crime_news = fetch_news(crime_query, max_news)
    if crime_news.get("error"):
        st.warning(crime_news["error"])
    else:
        for a in crime_news.get("articles", []):
            st.markdown(f"**{a.get('title')}**")
            st.write(a.get('description'))
            st.write(a.get('url'))
            st.markdown("---")

    # Disaster News
    if include_disaster:
        st.header("🌋 재난·재해 뉴스")
        disaster_query = f"{country} earthquake OR flood OR typhoon OR wildfire"
        dn = fetch_news(disaster_query, 5)
        if dn.get("error"):
            st.warning(dn["error"])
        else:
            for a in dn.get("articles", []):
                st.markdown(f"**{a.get('title')}**")
                st.write(a.get('description'))
                st.write(a.get('url'))
                st.markdown("---")

st.caption("데모 데이터 기반. 실제 상황은 현지 정부·대사관 공지 참고 필수.")
