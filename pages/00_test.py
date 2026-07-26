import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------------------------------------------
# 1. 페이지 설정
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="8개년 글로벌 무역 시뮬레이터",
    page_icon="🛳️",
    layout="wide"
)

# -----------------------------------------------------------------------------
# 2. 기초 데이터 수립 (2017 ~ 2024 실데이터 및 연도별 주요 사건)
# -----------------------------------------------------------------------------
# 데이터 기준: 한국 무역통계 기준 경향성 (단위: 억 달러)
HISTORICAL_DATA = {
    2017: {"수출": 5737, "수입": 4784, "GDP성장률": 3.2},
    2018: {"수출": 6049, "수입": 5352, "GDP성장률": 2.9},
    2019: {"수출": 5422, "수입": 5033, "GDP성장률": 2.2},
    2020: {"수출": 5125, "수입": 4676, "GDP성장률": -0.7},
    2021: {"수출": 6444, "수입": 6151, "GDP성장률": 4.3},
    2022: {"수출": 6836, "수입": 7312, "GDP성장률": 2.6},
    2023: {"수출": 6327, "수입": 6427, "GDP성장률": 1.4},
    2024: {"수출": 6838, "수입": 6320, "GDP성장률": 2.2}
}

YEAR_EVENTS = {
    2018: {
        "title": "⚡ 미·중 무역 전쟁 본격화",
        "desc": "미국과 중국의 관세 폭탄전으로 글로벌 공급망이 흔들리고 물동량 증가세가 둔화됩니다.",
        "export_mod": 1.05,
        "import_mod": 1.08,
        "risk_mod": 1.1
    },
    2019: {
        "title": "📉 글로벌 반도체 단가 급락 및 한일 무역 갈등",
        "desc": "메모리 반도체 가격 폭락과 일본의 핵심 소재 수출 규제로 IT·무역 부문이 직격탄을 맞습니다.",
        "export_mod": 0.90,
        "import_mod": 0.95,
        "risk_mod": 1.2
    },
    2020: {
        "title": "🦠 코로나19 팬데믹 쇼크",
        "desc": "전 세계 봉쇄령(Lockdown)으로 국경이 닫히고 세계 교역량이 국면 상 최저치로 폭락합니다.",
        "export_mod": 0.85,
        "import_mod": 0.88,
        "risk_mod": 1.5
    },
    2021: {
        "title": "🚀 보상 소비 폭발 & 해상 운임 급증",
        "desc": "각국의 경기 부양책과 유동성 공급으로 글로벌 수요가 폭발하나 물류 병목 현상으로 운임이 폭등합니다.",
        "export_mod": 1.25,
        "import_mod": 1.20,
        "risk_mod": 0.9
    },
    2022: {
        "title": "🛢️ 러시아-우크라이나 전쟁 & 원자재 쇼크",
        "desc": "에너지 및 곡물 가격 폭등으로 수입 비용이 급증하고 고물가·고금리 기조가 시작됩니다.",
        "export_mod": 1.05,
        "import_mod": 1.28,
        "risk_mod": 1.4
    },
    2023: {
        "title": "🏦 고금리 장기화 & 중국 경기 회복 지연",
        "desc": "글로벌 긴축 재정 지속과 핵심 수출국인 중국의 경기 회복 지연으로 교역이 다시 둔화됩니다.",
        "export_mod": 0.92,
        "import_mod": 0.90,
        "risk_mod": 1.1
    },
    2024: {
        "title": "🤖 AI 반도체 붐 & 홍해 물류 위기",
        "desc": "AI 산업 급성장으로 반도체 수출이 반등하지만 중동 지정학 위기로 해상 우회 운송 비용이 발생합니다.",
        "export_mod": 1.15,
        "import_mod": 1.02,
        "risk_mod": 1.0
    }
}

ITEMS = {
    "반도체/전자": {"base_margin": 0.25, "volatility": 0.15},
    "자동차/배터리": {"base_margin": 0.18, "volatility": 0.08},
    "석유화학/에너지": {"base_margin": 0.12, "volatility": 0.25},
    "식품/농산물": {"base_margin": 0.08, "volatility": 0.05}
}

# -----------------------------------------------------------------------------
# 3. 세션 상태(Session State) 관리
# -----------------------------------------------------------------------------
BASE_CAPITAL = 100.0  # 기본 자본 100억원

if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "current_turn" not in st.session_state:
    st.session_state.current_turn = 1  # 총 7턴 (2018년 ~ 2024년)
if "capital" not in st.session_state:
    st.session_state.capital = BASE_CAPITAL
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------------------------------------------------------
# 4. 게임 화면 구현
# -----------------------------------------------------------------------------
st.title("🛳️ 8개년 글로벌 무역 시뮬레이터 (2018~2024)")
st.caption("2017년 실적 기준 기본 자본 100억원으로 시작하여, 7년간의 거시 경제 파도를 극복하세요!")

# 대시보드 상단 요약
col_a, col_b, col_c, col_d = st.columns(4)
col_a.metric("현재 자산", f"{st.session_state.capital:,.1f} 억원", 
             f"{st.session_state.capital - BASE_CAPITAL:,.1f} 억원" if st.session_state.game_started else "0 억원")
col_b.metric("진행 상황", f"{st.session_state.current_turn} / 7 턴" if st.session_state.current_turn <= 7 else "완료")
current_year = 2017 + st.session_state.current_turn if st.session_state.current_turn <= 7 else 2024
col_c.metric("현재 연도", f"{current_year}년")
col_d.metric("기준 연도 데이터(2017)", f"수출 {HISTORICAL_DATA[2017]['수출']}억$ / 수입 {HISTORICAL_DATA[2017]['수입']}억$")

st.markdown("---")

# 게임 종료 조건 검사
if st.session_state.current_turn > 7:
    st.balloons()
    st.success("🎉 축하합니다! 7개년(2018년~2024년) 무역 경영을 모두 마쳤습니다.")
    
    profit_rate = ((st.session_state.capital - BASE_CAPITAL) / BASE_CAPITAL) * 100
    st.subheader(f"📊 최종 성과: 자산 {st.session_state.capital:,.1f}억원 (수익률: {profit_rate:+.2f}%)")
    
    df_history = pd.DataFrame(st.session_state.history)
    
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(df_history[["연도", "선택전략", "주요품목", "투자액(억)", "수익(억)", "최종자산(억)"]], use_container_width=True)
    with col2:
        fig = px.line(df_history, x="연도", y="최종자산(억)", title="연도별 자산 추이", markers=True)
        st.plotly_chart(fig, use_container_width=True)
        
    if st.button("게임 다시 시작하기"):
        st.session_state.game_started = False
        st.session_state.current_turn = 1
        st.session_state.capital = BASE_CAPITAL
        st.session_state.history = []
        st.rerun()

else:
    event = YEAR_EVENTS[current_year]
    
    st.warning(f"### {current_year}년 주요 국제 사건: {event['title']}")
    st.write(f"**상황 설명:** {event['desc']}")
    
    prev_year = current_year - 1
    st.info(f"💡 **참고 (실제 국가 통계):** {prev_year}년 대비 {current_year}년 실제 한국 무역 수지 추이 → "
            f"수출: {HISTORICAL_DATA[current_year]['수출']}억$ ({HISTORICAL_DATA[current_year]['수출'] - HISTORICAL_DATA[prev_year]['수출']:+}억$) | "
            f"수입: {HISTORICAL_DATA[current_year]['수입']}억$ ({HISTORICAL_DATA[current_year]['수입'] - HISTORICAL_DATA[prev_year]['수입']:+}억$)")
    
    st.markdown("### 🎲 무역 전략 수립")
    
    with st.form("trade_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            strategy = st.selectbox(
                "무역 방향 선택",
                ["수출 중심 (공급망 확장)", "수입 중심 (원자재 확보)", "균형 무역 (위험 분산)"]
            )
            
        with col2:
            item = st.selectbox(
                "주요 무역 품목 선택",
                list(ITEMS.keys())
            )
            
        with col3:
            invest_ratio = st.slider(
                "투입 자본 비율 (%)",
                min_value=10, max_value=100, value=50, step=10,
                help="보유 자금 중 얼마를 이번 무역 건에 투입할지 결정합니다."
            )
            
        submit = st.form_submit_button("무역 실행 및 턴 종료")
        
    if submit:
        st.session_state.game_started = True
        invest_amount = st.session_state.capital * (invest_ratio / 100.0)
        item_info = ITEMS[item]
        
        margin = item_info["base_margin"]
        
        if "수출" in strategy:
            margin *= event["export_mod"]
        elif "수입" in strategy:
            margin *= (2.0 - event["import_mod"])
        else:
            margin *= (event["export_mod"] + event["import_mod"]) / 2.0
            
        gdp_effect = (HISTORICAL_DATA[current_year]["GDP성장률"] / 100.0)
        final_return_rate = margin + gdp_effect
        
        earned = invest_amount * (1 + final_return_rate)
        profit = earned - invest_amount
        
        st.session_state.capital += profit
        
        st.session_state.history.append({
            "연도": current_year,
            "선택전략": strategy,
            "주요품목": item,
            "투자액(억)": round(invest_amount, 1),
            "수익(억)": round(profit, 1),
            "최종자산(억)": round(st.session_state.capital, 1)
        })
        
        st.session_state.current_turn += 1
        st.rerun()

# 기록 테이블
if st.session_state.history:
    st.markdown("---")
    st.subheader("📜 지금까지의 무역 기록")
    st.table(pd.DataFrame(st.session_state.history))
