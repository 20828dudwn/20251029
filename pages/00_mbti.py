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
        "title": "수호자 (Defender)",
        "desc": "헌신적이고 따뜻한 마음을 가진 보호자예요. 다른 사람을 도와주는 것을 좋아합니다.",
        "job": "간호사, 교사, 상담가, 사회복지사",
        "match": "ESFP 💞 ESTP"
    },
    "ESTJ": {
        "emoji": "🏗️",
        "title": "경영자 (Executive)",
        "desc": "현실적이고 결단력 있는 리더예요. 명확한 원칙과 질서를 중시합니다.",
        "job": "관리자, 법률가, 경영인, 군인",
        "match": "ISFP 💞 INFP"
    },
    "ESFJ": {
        "emoji": "🤝",
        "title": "친선도모자 (Consul)",
        "desc": "사교적이고 배려심이 깊은 사람으로, 주변의 조화를 중요하게 여깁니다.",
        "job": "간호사, 상담가, 교사, 서비스직",
        "match": "ISFP 💞 INFP"
    },
    "ISTP": {
        "emoji": "🛠️",
        "title": "장인 (Virtuoso)",
        "desc": "문제 해결 능력이 뛰어난 실용주의자예요. 손으로 무언가를 만드는 걸 좋아합니다.",
        "job": "엔지니어, 파일럿, 프로그래머, 정비사",
        "match": "ESFJ 💞 ESTJ"
    },
    "ISFP": {
        "emoji": "🌿",
        "title": "예술가 (Adventurer)",
        "desc": "감각적이고 자유로운 영혼이에요. 현재의 순간을 즐기는 성향을 가집니다.",
        "job": "디자이너, 음악가, 사진작가, 플로리스트",
        "match": "ENFJ 💞 ESFJ"
    },
    "ESTP": {
        "emoji": "⚡",
        "title": "사업가 (Entrepreneur)",
        "desc": "에너지 넘치고 모험을 즐기는 현실주의자예요. 즉흥적이지만 능동적입니다.",
        "job": "영업가, 창업가, 스포츠 코치, 프로게이머",
        "match": "ISFJ 💞 ISTJ"
    },
    "ESFP": {
        "emoji": "🎉",
        "title": "연예인 (Entertainer)",
        "desc": "밝고 긍정적인 성격으로 사람들을 즐겁게 합니다. 인생을 즐길 줄 아는 타입이에요.",
        "job": "연예인, 배우, 이벤트 플래너, 홍보 전문가",
        "match": "ISFJ 💞 ISTJ"
    },
}

# --- 검색창 ---
user_input = st.text_input("🔎 MBTI를 입력하세요:", placeholder="예: INFP, ESTJ, ENTP...").upper().strip()

# --- 결과 표시 ---
if user_input:
    if user_input in mbti_data:
        info = mbti_data[user_input]
        st.markdown(f"## {info['emoji']} {user_input} - {info['title']}")
        st.info(info["desc"])

        st.markdown(f"### 💼 추천 직업")
        st.success(info["job"])

        st.markdown(f"### 💖 잘 맞는 궁합 MBTI")
        st.warning(info["match"])
    else:
        st.error("⚠️ 존재하지 않는 MBTI 유형이에요. 다시 입력해 주세요!")

# --- 푸터 ---
st.markdown("---")
st.caption("✨ 만든이: ChatGPT | Streamlit으로 구현된 MBTI 탐색 웹앱 💫")

