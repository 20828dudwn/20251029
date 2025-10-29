import streamlit as st

# --- 기본 설정 ---
st.set_page_config(
    page_title="MBTI 성격 탐구소 🔮",
    page_icon="🧠",
    layout="centered"
)

# --- 헤더 ---
st.title("MBTI 성격 탐구소 🔍")
st.markdown("**당신의 MBTI를 입력하고, 성격·직업·궁합까지 알아보세요! ✨**")

# --- MBTI 데이터 ---
mbti_data = {
    "INTJ": {
        "emoji": "🧠",
        "title": "전략가 (Architect)",
        "desc": "독립적이고 통찰력 있는 전략가예요. 큰 그림을 보고 효율적으로 문제를 해결합니다.",
        "job": "데이터 분석가, 과학자, 전략 컨설턴트, 엔지니어",
        "match": "ENFP 💞 ENTP"
    },
    "INTP": {
        "emoji": "🤓",
        "title": "논리학자 (Logician)",
        "desc": "호기심 많고 아이디어가 넘치는 사고형 인재예요. 새로운 개념을 탐구하는 걸 좋아합니다.",
        "job": "연구원, 프로그래머, 철학자, 개발자",
        "match": "ENTJ 💞 ESTJ"
    },
    "ENTJ": {
        "emoji": "💼",
        "title": "리더 (Commander)",
        "desc": "목표 지향적이고 결단력 있는 리더예요. 조직을 이끌며 성과를 만들어냅니다.",
        "job": "경영인, 변호사, CEO, 프로젝트 매니저",
        "match": "INFP 💞 ISFP"
    },
    "ENTP": {
        "emoji": "💡",
        "title": "발명가 (Debater)",
        "desc": "토론과 창의성을 즐기는 아이디어 뱅크예요. 새로운 시각으로 세상을 바라봅니다.",
        "job": "마케팅 전문가, 창업가, 크리에이터, 컨설턴트",
        "match": "INFJ 💞 INTJ"
    },
    "INFJ": {
        "emoji": "🌙",
        "title": "선의의 옹호자 (Advocate)",
        "desc": "이상적이고 통찰력 깊은 사람으로, 세상을 더 나은 곳으로 만들고자 합니다.",
        "job": "상담가, 심리학자, 작가, 사회운동가",
        "match": "ENFP 💞 ENTP"
    },
    "INFP": {
        "emoji": "🎨",
        "title": "중재자 (Mediator)",
        "desc": "감성적이고 상상력이 풍부한 이상주의자예요. 진정성과 조화를 중요시합니다.",
        "job": "작가, 디자이너, 예술가, 상담가",
        "match": "ENTJ 💞 ENFJ"
    },
    "ENFJ": {
        "emoji": "🌟",
        "title": "선도자 (Protagonist)",
        "desc": "따뜻하고 카리스마 있는 리더예요. 다른 사람들을 돕고 영감을 줍니다.",
        "job": "교사, 인사담당자, 상담가, 리더십 코치",
        "match": "INFP 💞 ISFP"
    },
    "ENFP": {
        "emoji": "🔥",
        "title": "활동가 (Campaigner)",
        "desc": "열정적이고 자유로운 영혼이에요. 새로운 경험과 사람을 사랑합니다.",
        "job": "광고기획자, 작가, 예술가, 스타트업 창업자",
        "match": "INFJ 💞 INTJ"
    },
    "ISTJ": {
        "emoji": "📘",
        "title": "현실주의자 (Logistician)",
        "desc": "신중하고 책임감이 강한 사람으로, 체계적이고 신뢰할 수 있습니다.",
        "job": "공무원, 회계사, 변호사, 관리자",
        "match": "ESFP 💞 ESTP"
    },
    "ISFJ": {
        "emoji": "🕊️",
        "title": "수호자 (
