

import streamlit as st

st.set_page_config(
    page_title="KB 실손보험 계산기",
    page_icon="🏥",
    layout="centered"
)

st.title("🏥 KB 4세대 실손보험 계산기")
st.caption("급여·비급여 통합 예상 보험금 계산")

st.info(
    "포트폴리오용 MVP입니다. 실제 지급액은 가입증권, "
    "특약, 누적 지급액 및 보험사 심사에 따라 달라질 수 있습니다."
)

st.header("1. 보험 및 진료 정보")

insurance_type = st.radio(
    "진료 원인",
    ["상해", "질병"],
    horizontal=True
)

treatment_type = st.radio(
    "진료 유형",
    ["통원", "입원"],
    horizontal=True
)

st.divider()
st.header("2. 의료비 입력")

st.subheader("급여 의료비")

medical_cost = st.number_input(
    "급여 보장대상 의료비 (원)",
    min_value=0,
    value=100000,
    step=10000
)

st.subheader("비급여 의료비")

non_covered_cost = st.number_input(
    "일반 비급여 보장대상 의료비 (원)",
    min_value=0,
    value=100000,
    step=10000
)

st.caption(
    "일반 비급여 입력에는 도수치료·체외충격파·증식치료, "
    "비급여 주사료, MRI/MRA 등 3대 비급여 특약 항목을 포함하지 마세요."
)

if treatment_type == "통원":

    st.divider()
    st.subheader("3. 통원 정보")

    hospital_type = st.selectbox(
        "의료기관 유형",
        [
            "의원급 의료기관·보건소 등",
            "상급종합병원·종합병원 등"
        ]
    )

    급여한도 = st.number_input(
        "급여 통원 1회당 가입 보장한도 (원)",
        min_value=0,
        max_value=200000,
        value=200000,
        step=10000
    )

    비급여한도 = st.number_input(
        "비급여 통원 1회당 가입 보장한도 (원)",
        min_value=0,
        max_value=200000,
        value=200000,
        step=10000
    )

    previous_visits = st.number_input(
        "해당 보험연도 이전까지 사용한 비급여 통원 횟수",
        min_value=0,
        value=0,
        step=1
    )

    급여잔여한도 = st.number_input(
        "급여 연간 보장한도 잔액 (원)",
        min_value=0,
        max_value=50000000,
        value=50000000,
        step=100000
    )

    비급여잔여한도 = st.number_input(
        "비급여 연간 보장한도 잔액 (원)",
        min_value=0,
        max_value=50000000,
        value=50000000,
        step=100000
    )

else:

    st.divider()
    st.subheader("3. 입원 정보")

    room_cost = st.number_input(
        "상급병실료 차액 총액 (원)",
        min_value=0,
        value=0,
        step=10000
    )

    hospital_days = st.number_input(
        "총 입원 일수",
        min_value=1,
        value=1,
        step=1
    )

    previous_copay = st.number_input(
        "해당 보험연도 이전까지 누적된 급여 입원 본인부담금 20% (원)",
        min_value=0,
        value=0,
        step=10000
    )

    급여잔여한도 = st.number_input(
        "급여 연간 보장한도 잔액 (원)",
        min_value=0,
        max_value=50000000,
        value=50000000,
        step=100000
    )

    비급여잔여한도 = st.number_input(
        "비급여 연간 보장한도 잔액 (원)",
        min_value=0,
        max_value=50000000,
        value=50000000,
        step=100000
    )

st.divider()
st.header("4. 예상 보험금 계산")

if st.button("보험금 계산하기", use_container_width=True):

    급여보험금 = 0
    비급여보험금 = 0
    details = []

    if treatment_type == "통원":

        # 급여 통원
        최소공제 = (
            10000
            if hospital_type == "의원급 의료기관·보건소 등"
            else 20000
        )

        급여공제 = max(
            최소공제,
            int(medical_cost * 0.20)
        )

        급여계산액 = max(
            0,
            medical_cost - 급여공제
        )

        급여보험금 = min(
            급여계산액,
            급여한도,
            급여잔여한도
        )

        # 일반 비급여 통원
        비급여공제 = max(
            30000,
            int(non_covered_cost * 0.30)
        )

        비급여계산액 = max(
            0,
            non_covered_cost - 비급여공제
        )

        비급여보험금 = (
            min(비급여계산액, 비급여한도, 비급여잔여한도)
            if previous_visits < 100
            else 0
        )

        details = [
            f"급여 의료비: {medical_cost:,}원",
            f"급여 공제금액: {급여공제:,}원",
            f"급여 한도 적용 전 금액: {급여계산액:,}원",
            f"급여 통원 보상한도: {급여한도:,}원",
            f"비급여 의료비: {non_covered_cost:,}원",
            f"비급여 공제금액: {비급여공제:,}원",
            f"비급여 한도 적용 전 금액: {비급여계산액:,}원",
            f"기존 비급여 통원 사용 횟수: {previous_visits}회"
        ]

    else:

        # 급여 입원
        기본급여보험금 = int(medical_cost * 0.80)
        현재본인부담금 = medical_cost * 0.20

        연간초과전 = max(
            0,
            previous_copay - 2000000
        )

        연간초과후 = max(
            0,
            previous_copay + 현재본인부담금 - 2000000
        )

        추가급여보험금 = int(
            연간초과후 - 연간초과전
        )

        급여계산액 = (
            기본급여보험금 + 추가급여보험금
        )

        급여보험금 = min(
            급여계산액,
            급여잔여한도
        )

        # 일반 비급여 입원
        일반비급여보험금 = int(
            non_covered_cost * 0.70
        )

        일평균병실료 = room_cost / hospital_days

        보상대상병실료 = (
            min(일평균병실료, 100000) * hospital_days
        )

        병실료보험금 = int(
            보상대상병실료 * 0.50
        )

        비급여계산액 = (
            일반비급여보험금 + 병실료보험금
        )

        비급여보험금 = min(
            비급여계산액,
            비급여잔여한도
        )

        details = [
            f"급여 의료비: {medical_cost:,}원",
            f"급여 기본 보상액 (80%): {기본급여보험금:,}원",
            f"급여 추가 보상액: {추가급여보험금:,}원",
            f"급여 한도 적용 전 금액: {급여계산액:,}원",
            f"일반 비급여 의료비: {non_covered_cost:,}원",
            f"일반 비급여 보상액 (70%): {일반비급여보험금:,}원",
            f"상급병실료 차액: {room_cost:,}원",
            f"1일 평균 상급병실료: {일평균병실료:,.0f}원",
            f"상급병실료 보상액 (50%): {병실료보험금:,}원",
            f"비급여 한도 적용 전 금액: {비급여계산액:,}원"
        ]

    total_benefit = 급여보험금 + 비급여보험금

    st.success("계산이 완료되었습니다.")

    st.subheader("예상 보험금")

    st.metric(
        "총 예상 보험금",
        f"{total_benefit:,}원"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "급여 예상 보험금",
            f"{급여보험금:,}원"
        )

    with col2:
        st.metric(
            "비급여 예상 보험금",
            f"{비급여보험금:,}원"
        )

    st.divider()
    st.subheader("계산 상세 내역")

    for item in details:
        st.write(f"- {item}")

    st.divider()
    st.subheader("적용 기준")

    if treatment_type == "통원":
        st.write(
            "급여 통원: 의료기관별 최소 공제금액과 "
            "보장대상 의료비의 20% 중 큰 금액을 공제합니다."
        )
        st.write(
            "일반 비급여 통원: 3만원과 보장대상 의료비의 "
            "30% 중 큰 금액을 공제합니다. 연간 100회 한도를 적용합니다."
        )
    else:
        st.write(
            "급여 입원: 급여 의료비의 80%를 기본 계산하고, "
            "연간 급여 본인부담금 20%가 200만원을 초과하는 경우 "
            "초과분을 추가 계산합니다."
        )
        st.write(
            "일반 비급여 입원: 병실료를 제외한 비급여 의료비의 "
            "70%와 상급병실료 차액 보상액을 합산합니다."
        )

    st.caption(
        "본 계산기는 일반 급여·비급여의 단순화된 예상 계산 모델입니다. "
        "3대 비급여 특약, 보상 제외 항목, 실제 계약별 가입금액, "
        "누적 지급액 및 세부 약관 조건은 별도 확인이 필요합니다."
    )
