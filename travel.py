import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

# =========================
# 한국어 → 영어 변환
# =========================
country_map = {
    "대한민국": "South Korea",
    "일본": "Japan",
    "중국": "China",
    "미국": "United States",
    "프랑스": "France",
    "독일": "Germany",
    "영국": "United Kingdom",
    "캐나다": "Canada",
    "호주": "Australia",
    "태국": "Thailand",
}

# =========================
# 국가별 테마
# =========================
country_theme = {
    "일본": {"color": "#E60033", "emoji": "🇯🇵", "bg": "https://images.unsplash.com/photo-1549692520-acc6669e2f0c", "keywords": ["도쿄", "온천", "사케", "스시", "안전한 치안"]},
    "태국": {"color": "#D4A017", "emoji": "🇹🇭", "bg": "https://images.unsplash.com/photo-1506976785307-8732e854ad89", "keywords": ["푸켓", "야시장", "마사지", "바다", "소매치기 주의"]},
    "미국": {"color": "#3C3B6E", "emoji": "🇺🇸", "bg": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee", "keywords": ["뉴욕", "총기 사건", "광활한 국토", "다양성", "자연"]},
    "프랑스": {"color": "#002654", "emoji": "🇫🇷", "bg": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34", "keywords": ["파리", "와인", "예술", "낭만", "소매치기 많음"]},
}

# =========================
# 대사관 정보
# =========================
embassy_info = {
    "일본": {"address": "도쿄도 미나토구 아자부", "phone": "+81-3-3452-7611", "lat": 35.6581, "lng": 139.7516},
    "미국": {"address": "워싱턴 D.C. 뉴햄프셔 Ave", "phone": "+1-202-939-5600", "lat": 38.9172, "lng": -77.0450},
    "태국": {"address": "방콕 싸톤", "phone": "+66-2-247-7537", "lat": 13.7230, "lng": 100.5460},
    "프랑스": {"address": "파리 16구", "phone": "+33-1-4753-0101", "lat": 48.8667, "lng": 2.3125},
    "대한민국": {"address": "서울 종로구", "phone": "+82-2-3210-0400", "lat": 37.57295, "lng": 126.97936},
}

# =========================
# 뉴스 (예시)
# =========================
def get_news(country):
    return [
        {"title": f"{country} 최근 범죄 뉴스 1", "url": "#"},
        {"title": f"{country} 사회·안전 뉴스 2", "url": "#"},
        {"title": f"{country} 여행자 주의보 관련 뉴스 3", "url": "#"},
    ]

# =========================
# 국가 정보 API
# =========================
def get_country_info(country):
    url = f"https://restcountries.com/v3.1/name/{country}"
    res = requests.get(url)
    return res.json()[0] if res.status_code == 200 else None

# =========================
# Streamlit UI
# =========================
st.set_page_config(layout="wide")
st.sidebar.header("🌍 여행 국가 선택")
selected_country_kr = st.sidebar.selectbox("국가 선택", list(country_map.keys()))
selected_country_en = country_map[selected_country_kr]

# 안전 점수 카드
safety_score = 75
st.sidebar.markdown(f"<div style='background-color:#f0f0f0; padding:15px; border-radius:10px; text-align:center;'>\n<h3>안전 점수</h3>\n<h1 style='color:#4CAF50;'>{safety_score}/100</h1>\n</div>", unsafe_allow_html=True)

# 메인 화면 헤더
theme = country_theme.get(selected_country_kr)
if theme:
    st.markdown(f"""<div style='padding:25px; border-radius:15px; background-image:url({theme['bg']}); background-size:cover;'>\n<h1 style='color:white; text-shadow:2px 2px 8px black;'>{theme['emoji']} {selected_country_kr} 여행 정보</h1>\n</div>""", unsafe_allow_html=True)
else:
    st.header(f"{selected_country_kr} 여행 정보")

# 기본 정보 & 키워드 카드
info = get_country_info(selected_country_en)
if info:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📌 기본 정보")
        st.markdown(f"""
        <div style='padding:15px; border-radius:10px; background-color:#f9f9f9;'>
        <p><b>수도:</b> {info['capital'][0]}</p>
        <p><b>인구:</b> {info['population']:,}</p>
        <p><b>지역:</b> {info['region']}</p>
        <p><b>국가 코드:</b> {info['cca2']}</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.subheader("🔍 특징 키워드")
        if theme:
            for key in theme['keywords']:
                st.markdown(f"<div style='padding:8px; border-radius:8px; background-color:#e0f7fa; display:inline-block; margin:2px;'>{key}</div>", unsafe_allow_html=True)

# 지도 생성
lat, lng = info["latlng"]
m = folium.Map(location=[lat, lng], zoom_start=4)
folium.Marker([lat, lng], tooltip=f"{selected_country_kr} 위치", icon=folium.Icon(color="blue")).add_to(m)

# 대사관 마커
emb = embassy_info.get(selected_country_kr)
if emb:
    folium.Marker([emb['lat'], emb['lng']], tooltip=f"한국 대사관\n{emb['address']}\n{emb['phone']}", icon=folium.Icon(color="red", icon="info-sign")).add_to(m)

# 위험 지역 마커 예시
risk_locations = [
    {"name": "관광지 위험지역 1", "lat": lat + 1, "lng": lng + 1},
    {"name": "관광지 위험지역 2", "lat": lat - 1, "lng": lng - 1},
]
for r in risk_locations:
    folium.Marker([r['lat'], r['lng']], tooltip=r['name'], icon=folium.Icon(color="orange", icon="exclamation-sign")).add_to(m)

st.subheader("🗺️ 지도 (국가 위치 + 대사관 + 위험 지역)")
st_folium(m, width=800, height=500)

# 뉴스
st.subheader("📰 최근 범죄/안전 뉴스")
for article in get_news(selected_country_en):
    st.markdown(f"- [{article['title']}]({article['url']})")

# 실제 실종자 데이터
st.subheader("🚨 최근 실종자 정보")
korean_missing_overseas = 2474
domestic_missing_last_year = 124223
st.markdown(f"<div style='padding:15px; border-radius:10px; background-color:#fff3e0;'>국내 신고된 실종자 수(작년): <b>{domestic_missing_last_year:,}건</b><br>해외 한국인 실종·납치·구금 건수(2018~2022 상반기): <b>{korean_missing_overseas:,}건</b></div>", unsafe_allow_html=True)

# 여행 안전 팁
st.subheader("💡 여행 안전 팁")
if selected_country_kr == "일본":
    st.info("일본은 안전하지만 관광지 소매치기와 지진 대비 필요")
elif selected_country_kr == "태국":
    st.warning("야시장·바닷가 근처 소매치기, 오토바이 사고 주의")
elif selected_country_kr == "미국":
    st.error("총기 사건 빈발, 방문 전 위험도 확인 필요")
elif selected_country_kr == "프랑스":
    st.warning("파리 관광지 소매치기 주의")
else:
    st.info("여행 시 기본 안전 수칙 준수")
