import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

#########################
# 한국어 → 영어 변환
#########################
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

#########################
# 국가별 테마
#########################
country_theme = {
    "일본": {"color": "#E60033", "emoji": "🇯🇵", "bg": "https://images.unsplash.com/photo-1549692520-acc6669e2f0c", "keywords": ["도쿄", "온천", "사케", "스시", "안전한 치안"]},
    "태국": {"color": "#D4A017", "emoji": "🇹🇭", "bg": "https://images.unsplash.com/photo-1506976785307-8732e854ad89", "keywords": ["푸켓", "야시장", "마사지", "바다", "소매치기 주의"]},
    "미국": {"color": "#3C3B6E", "emoji": "🇺🇸", "bg": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee", "keywords": ["뉴욕", "총기 사건", "광활한 국토", "다양성", "자연"]},
    "프랑스": {"color": "#002654", "emoji": "🇫🇷", "bg": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34", "keywords": ["파리", "와인", "예술", "낭만", "소매치기 많음"]},
}

#########################
# 대사관 정보
#########################
embassy_info = {
    "일본": {"address": "도쿄도 미나토구 아자부", "phone": "+81-3-3452-7611", "lat": 35.6581, "lng": 139.7516},
    "미국": {"address": "워싱턴 D.C. 뉴햄프셔 Ave", "phone": "+1-202-939-5600", "lat": 38.9172, "lng": -77.0450},
    "태국": {"address": "방콕 싸톤", "phone": "+66-2-247-7537", "lat": 13.7230, "lng": 100.5460},
    "프랑스": {"address": "파리 16구", "phone": "+33-1-4753-0101", "lat": 48.8667, "lng": 2.3125},
    "대한민국": {"address": "서울 종로구", "phone": "+82-2-3210-0400", "lat": 37.57295, "lng": 126.97936},
}

#########################
# 뉴스 예시
#########################
def get_news(country):
    return [
        {"title": f"{country} 최근 범죄 뉴스 1", "url": "#"},
        {"title": f"{country} 사회·안전 뉴스 2", "url": "#"},
        {"title": f"{country} 여행자 주의보 관련 뉴스 3", "url": "#"},
    ]

#########################
# 국가 정보 API
#########################
def get_country_info(country):
    url = f"https://restcountries.com/v3.1/name/{country}"
    res = requests.get(url)
    return res.json()[0] if res.status_code == 200 else None

#########################
# Streamlit UI
#########################
st.set_page_config(layout="wide")
st.title("🌍 여행 안전 정보 프로그램")

# 선택지 방식
selected_country_kr = st.radio("여행하려는 나라를 선택하세요", list(country_map.keys()))
selected_country_en = country_map[selected_country_kr]

# 국가 테마 적용
theme = country_theme.get(selected_country_kr)
if theme:
    st.markdown(
        f"""<div style='padding:18px; border-radius:15px; background-size:cover; background-position:center; background-image:url({theme['bg']});'>
            <h2 style='color:white; text-shadow:0px 0px 8px black;'>{theme['emoji']} {selected_country_kr} 여행 정보</h2>
        </div>""", unsafe_allow_html=True
    )
else:
    st.header(f"{selected_country_kr} 여행 정보")

# API 데이터
info = get_country_info(selected_country_en)
if not info:
    st.error("국가 정보를 불러올 수 없습니다.")
    st.stop()

# 2열 레이아웃 기본 정보
col1, col2 = st.columns(2)
with col1:
    st.subheader("📌 기본 정보")
    st.write(f"**수도:** {info['capital'][0]}")
    st.write(f"**인구:** {info['population']:,}")
    st.write(f"**지역:** {info['region']}")
    st.write(f"**국가 코드:** {info['cca2']}")
with col2:
    st.subheader("🔍 특징 키워드")
    if theme:
        for key in theme['keywords']:
            st.markdown(f"✅ {key}")

# 지도 생성 (국가 위치 + 대사관 + 위험 지역)
lat, lng = info["latlng"]
m = folium.Map(location=[lat, lng], zoom_start=4)

# 국가 위치 마커
folium.Marker([lat, lng], tooltip=f"{selected_country_kr} 위치", icon=folium.Icon(color="blue")).add_to(m)

# 대사관 위치 마커
emb = embassy_info.get(selected_country_kr)
if emb:
    folium.Marker([emb['lat'], emb['lng']], tooltip=f"한국 대사관\n{emb['address']}\n{emb['phone']}", icon=folium.Icon(color="red", icon="info-sign")).add_to(m)

# 위험 지역 / 재난 예시 마커
risk_locations = [
    {"name": "관광지 위험지역 1", "lat": lat + 1, "lng": lng + 1},
    {"name": "관광지 위험지역 2", "lat": lat - 1, "lng": lng - 1},
]
for r in risk_locations:
    folium.Marker([r["lat"], r["lng"]], tooltip=r["name"], icon=folium.Icon(color="orange", icon="exclamation-sign")).add_to(m)

st.subheader("🗺️ 지도 (국가 위치 + 대사관 + 위험 지역)")
st_folium(m, width=700, height=500)

# 뉴스
st.subheader("📰 최근 범죄/안전 뉴스")
for article in get_news(selected_country_en):
    st.write(f"- [{article['title']}]({article['url']})")

# 실종자 정보 (예시)
st.subheader("🚨 최근 실종자 정보")
st.write("한국인 실종자 수: **2명(예시)**")
st.write("전체 실종자 수: **15명(예시)**")

# 동적 여행 팁
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
