import streamlit as st
import random

st.set_page_config(
    page_title="MBTI 다마고치",
    page_icon="🥚",
    layout="centered"
)

# ---------------- CSS -----------------
st.markdown("""
<style>

.main{
    background: linear-gradient(180deg,#FFF9FB,#F5F7FF);
}

.title{
    text-align:center;
    font-size:48px;
    font-weight:bold;
    background: linear-gradient(90deg,#ff4da6,#6c63ff);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    animation: glow 2s infinite alternate;
}

@keyframes glow{
from{transform:scale(1);}
to{transform:scale(1.05);}
}

.card{
padding:25px;
border-radius:20px;
background:white;
box-shadow:0 10px 25px rgba(0,0,0,0.12);
text-align:center;
transition:0.4s;
}

.card:hover{
transform:translateY(-8px) scale(1.03);
}

.job{
font-size:22px;
padding:8px;
}

.pet{
font-size:120px;
animation: bounce 1.5s infinite;
}

@keyframes bounce{
0%,100%{transform:translateY(0);}
50%{transform:translateY(-18px);}
}

.footer{
text-align:center;
color:gray;
}

</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🥚 MBTI 다마고치 직업 추천기 💼</div>", unsafe_allow_html=True)

st.write("")
st.write("✨ 당신의 MBTI를 선택하면 귀여운 다마고치와 추천 직업이 등장합니다!")

# --------------------------------------

jobs = {
"INTJ":["AI 연구원 🤖","의사 🩺","데이터 사이언티스트 📊"],
"INTP":["프로그래머 💻","교수 🎓","천문학자 🔭"],
"ENTJ":["CEO 👑","변호사 ⚖️","경영컨설턴트 📈"],
"ENTP":["발명가 💡","마케터 📣","창업가 🚀"],

"INFJ":["심리상담사 🌿","작가 📚","의사 🩺"],
"INFP":["소설가 ✍️","예술가 🎨","사회복지사 🤝"],
"ENFJ":["교사 🍎","HR 매니저 👨‍💼","상담사 💖"],
"ENFP":["유튜버 🎥","광고기획자 📺","여행작가 🌍"],

"ISTJ":["공무원 🏛️","회계사 💰","판사 ⚖️"],
"ISFJ":["간호사 💉","교사 📖","약사 💊"],
"ESTJ":["경찰 👮","군인 🪖","프로젝트 매니저 📋"],
"ESFJ":["승무원 ✈️","간호사 🏥","호텔리어 🏨"],

"ISTP":["기계공학자 ⚙️","파일럿 🛩️","응급구조사 🚑"],
"ISFP":["사진작가 📷","디자이너 🎨","플로리스트 🌸"],
"ESTP":["영업전문가 💼","운동선수 ⚽","소방관 🚒"],
"ESFP":["배우 🎭","가수 🎤","이벤트 플래너 🎉"]
}

pets={
"INTJ":"🦉",
"INTP":"🐧",
"ENTJ":"🦅",
"ENTP":"🦊",
"INFJ":"🦄",
"INFP":"🐰",
"ENFJ":"🦁",
"ENFP":"🐥",
"ISTJ":"🐢",
"ISFJ":"🐼",
"ESTJ":"🐯",
"ESFJ":"🐨",
"ISTP":"🐺",
"ISFP":"🐱",
"ESTP":"🐸",
"ESFP":"🐹"
}

mbti = st.selectbox(
    "🌟 MBTI를 선택하세요!",
    list(jobs.keys())
)

if st.button("🎁 결과 보기", use_container_width=True):

    progress = st.progress(0)

    for i in range(100):
        progress.progress(i+1)

    st.balloons()

    st.markdown(f"""
    <div class="card">

    <div class="pet">{pets[mbti]}</div>

    <h2>✨ {mbti} 다마고치 ✨</h2>

    <h3>💼 잘 어울리는 직업</h3>

    <div class="job">🥇 {jobs[mbti][0]}</div>
    <div class="job">🥈 {jobs[mbti][1]}</div>
    <div class="job">🥉 {jobs[mbti][2]}</div>

    </div>
    """, unsafe_allow_html=True)

    st.success("🎉 당신의 다마고치가 직업을 찾아왔어요!")

    st.snow()

st.write("")
st.markdown("<div class='footer'>💖 Made with Streamlit 💖</div>", unsafe_allow_html=True)
