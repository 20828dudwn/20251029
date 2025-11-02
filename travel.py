import streamlit as st
import requests
import pandas as pd
import folium
from streamlit.components.v1 import html

st.set_page_config(page_title="Travel Safety Explorer", layout="wide")

# ---------------------------
# 국가 정보 API
# ---------------------------
@st.cache_data
def get_country_info(name):
    try:
        url = f"https://restcountries.com/v3.1/name/{name}"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()[0]

        return {
            "name": data["name"]["common"],
            "capital": data.get("capital", [""])[0],
            "latlng": data.get("latlng", [0, 0]),
            "population": data.get("population", 0),
            "languages": ", ".join(data.get("languages", {}).values()),
            "flag": data.get("flags", {}).get("png")
        }
    except:
        return {"error": "국가 데이터를 찾을 수 없습니다."}

# ---------------------------
# 뉴스 API
# ---------------------------
def fetch_news(query, page_size=5):
    # 뉴스 API는 데모용 — 실제 키 필요 없음
    return []

# ---------------------------
# 샘플 데이터: 대사관 연락처
# ---------------------------
EMBASSY = {
    "Japan": {"phone": "+81-3-3452-7611", "address": "1-2-5 Minato-ku, Tokyo"},
    "South Korea": {"phone": "+82-2-3210-0400", "address": "Seoul Government Complex"},
    "Philippines": {"phone": "+63-2-856-9210", "address": "Taguig, Manila"},
}

# ---------------------------
# 샘플 데이터: 지역 안전 점수
# ---------------------------
SAFETY_SCORES = {
    "Japan": {"Tokyo": 88, "Osaka": 82, "Sapporo": 90},
    "South Korea": {"Seoul": 92, "Busan": 85, "Jeju": 95},
    "Philippines": {"Manila": 45, "Cebu": 60, "Boracay": 70},
}

# ---------------------------
# UI 시작
# ---------------------------
st.title("🌍 Travel Safety Explorer — 안전 정보 통합")

country = st.text_input("국가명 입력 (예: Japan, South Korea, Philippines)", value="Japan")

info = get_country_info(country)

if info.get("error"):
    st.error(info["error"])
    st.stop()

# ---------------------------
# 국가 기본 정보
# ---------------------------
st.header(f"📌 국가 정보 — {info['name']}")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown(f"**수도:** {info['capital']}")
    st.markdown(f"**인구:** {info['population']:,}")
    st.markdown(f"**언어:** {info['languages']}")

with col2:
    if info["flag"]:
        st.image(info["flag"], width=150)

st.markdown("---")

# ---------------------------
# 대사관 연락처
# ---------------------------
st.header("📞 대사관 연락처")

emb = EMBASSY.get(info["name"])
if emb:
    st.markdown(f"**전화번호:** {emb['phone']}")
    st.markdown(f"**주소:** {emb['address']}")
else:
    st.info("대사관 연락처 데이터가 없습니다.")

st.markdown("---")

# ---------------------------
# 안전 점수
# ---------------------------
st.header("🛡 지역별 안전 점수")

scores = SAFETY_SCORES.get(info["name"])

if scores:
    df = pd.DataFrame({
        "지역": list(scores.keys()),
        "안전 점수": list(scores.values())
    })
    st.bar_chart(df.set_index("지역"))
else:
    st.info("안전 점수 데이터 없음.")

st.markdown("---")

# ---------------------------
# 지도 표시 (streamlit_folium 필요 없음)
# ---------------------------
st.header("🗺 지도 표시")

lat, lng = info["latlng"]

# folium 지도 생성
m = folium.Map(location=[lat, lng], zoom_start=5)
folium.Marker([lat, lng], tooltip=f"Capital: {info['capital']}").add_to(m)

# 지도 HTML로 변환 후 embed
map_html = m._repr_html_()
html(map_html, height=500)

st.markdown("---")

# ---------------------------
# 여행 팁
# ---------------------------
st.header("✅ 여행 안전 팁")
st.markdown("""
- 야간 이동 시 항상 조심하기  
- 현지 경찰/대사관 연락처 저장  
- 재난 경보 수시 확인  
- 유동 인구 많은 지역 중심으로 이동  
""")
