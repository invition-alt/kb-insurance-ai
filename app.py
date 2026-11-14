import streamlit as st

st.set_page_config(
    page_title="KB 실손보험 계산기",
    page_icon="🏥",
    layout="centered"
)

st.title("🏥 KB 실손보험 보험금 계산기")

st.write(
    "의료비를 입력하면 예상 보험금을 확인할 수 있는 서비스입니다."
)

st.info(
    "본 서비스는 보험금 예상 계산을 위한 포트폴리오 프로젝트입니다. "
    "실제 지급 여부와 금액은 보험사의 심사에 따라 달라집니다."
)

st.divider()

st.header("1. 보험 정보")

insurance_company = st.selectbox(
    "보험사", ["KB손해보험"]
)

insurance_generation = st.selectbox(
    "실손보험 세대", ["4세대"]
)

st.divider()

st.header("2. 진료 정보")

treatment_type = st.radio(
    "진료 유형", ["통원", "입원"]
)

coverage_type = st.radio(
    "의료비 구분", ["급여", "비급여"]
)

medical_cost = st.number_input(
    "총 의료비 (원)",
    min_value=0,
    value=100000,
    step=10000
)

if treatment_type == "통원":
    hospital_type = st.selectbox(
        "의료기관 유형", ["의원", "병원"]
    )
else:
    hospital_type = None

st.divider()

st.header("3. 예상 보험금 확인")

if st.button("보험금 계산하기", use_container_width=True):
    st.write("보험사:", insurance_company)
    st.write("보험 세대:", insurance_generation)
    st.write("진료 유형:", treatment_type)
    st.write("의료비 구분:", coverage_type)
    st.write(f"총 의료비: {medical_cost:,}원")

    st.warning("보험금 계산 기능을 연결할 예정입니다.")

    st.caption(
        "현재는 웹사이트 기본 구조를 확인하기 위한 버전입니다."
    )
