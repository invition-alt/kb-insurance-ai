
import streamlit as st

st.set_page_config(
    page_title="KB 실손보험 AI 계산기",
    page_icon="🏥",
    layout="centered"
)

st.title("🏥 KB 실손보험 보험금 계산기")
st.caption("4세대 실손보험 · 보험금 예상 계산 MVP")

st.info(
    "본 서비스는 포트폴리오용 예상 계산 서비스입니다. "
    "실제 보험금 지급 여부와 금액은 보험사의 심사 결과에 따라 달라집니다."
)

st.header("1. 보험 및 진료 정보")

st.selectbox("보험사", ["KB손해보험"])
st.selectbox("실손보험 세대", ["4세대"])

treatment_type = st.radio(
    "진료 유형", ["통원", "입원"], horizontal=True
)

coverage_type = st.radio(
    "의료비 구분", ["급여", "비급여"], horizontal=True
)

st.divider()
st.header("2. 의료비 입력")

st.caption(
    "아래에는 총 병원비가 아닌 약관상 보장대상에 해당하는 "
    "환자 부담 의료비를 입력하세요."
)

if treatment_type == "통원":

    if coverage_type == "급여":

        medical_cost = st.number_input(
            "급여 보장대상 의료비 (원)",
            min_value=0, value=100000, step=10000
        )

        hospital_type = st.selectbox(
            "의료기관 유형",
            ["의원급 의료기관·보건소 등",
             "상급종합병원·종합병원 등"]
        )

        coverage_limit = st.number_input(
            "가입한 통원 1회당 보장한도 (원)",
            min_value=1, max_value=200000,
            value=200000, step=10000
        )

    else:

        medical_cost = st.number_input(
            "비급여 보장대상 의료비 (원)",
            min_value=0, value=100000, step=10000
        )

        previous_visits = st.number_input(
            "해당 보험연도 이전까지 사용한 비급여 통원 횟수",
            min_value=0, max_value=100, value=0, step=1
        )

else:

    if coverage_type == "급여":

        medical_cost = st.number_input(
            "급여 보장대상 의료비 (원)",
            min_value=0, value=1000000, step=10000
        )

        insurance_type = st.selectbox(
            "보장 유형", ["상해급여", "질병급여"]
        )

        previous_copay = st.number_input(
            "이전까지 누적된 입원 본인부담금 20% (원)",
            min_value=0, value=0, step=10000
        )

        remaining_limit = st.number_input(
            "남은 연간 보험가입금액 (원)",
            min_value=0, max_value=50000000,
            value=50000000, step=100000
        )

    else:

        insurance_type = st.selectbox(
            "보장 유형", ["상해비급여", "질병비급여"]
        )

        medical_cost = st.number_input(
            "일반 비급여 입원 의료비 (병실료 제외, 원)",
            min_value=0, value=1000000, step=10000
        )

        room_cost = st.number_input(
            "상급병실료 차액 총액 (원)",
            min_value=0, value=200000, step=10000
        )

        hospital_days = st.number_input(
            "총 입원 일수",
            min_value=1, value=2, step=1
        )

        remaining_limit = st.number_input(
            "남은 연간 보험가입금액 (원)",
            min_value=0, max_value=50000000,
            value=50000000, step=100000
        )

st.divider()
st.header("3. 보험금 계산 결과")

if st.button("예상 보험금 계산하기", use_container_width=True):

    result = 0
    details = []
    formula = ""
    coverage_name = coverage_type

    if treatment_type == "통원" and coverage_type == "급여":

        minimum_deductible = (
            10000 if hospital_type == "의원급 의료기관·보건소 등"
            else 20000
        )

        deductible = max(
            minimum_deductible,
            int(medical_cost * 0.20)
        )

        before_limit = max(0, medical_cost - deductible)
        result = min(before_limit, coverage_limit)

        details = [
            f"보장대상 의료비: {medical_cost:,}원",
            f"적용 공제금액: {deductible:,}원",
            f"한도 적용 전 보험금: {before_limit:,}원",
            f"통원 1회 보장한도: {coverage_limit:,}원"
        ]

        formula = (
            f"{medical_cost:,}원 - {deductible:,}원 "
            f"= {before_limit:,}원"
        )

    elif treatment_type == "통원" and coverage_type == "비급여":

        deductible = max(30000, int(medical_cost * 0.30))
        before_limit = max(0, medical_cost - deductible)

        result = (
            0 if previous_visits >= 100
            else before_limit
        )

        details = [
            f"보장대상 비급여 의료비: {medical_cost:,}원",
            f"적용 공제금액: {deductible:,}원",
            f"기존 사용 횟수: {previous_visits}회",
            "연간 통원 한도: 100회"
        ]

        formula = (
            f"{medical_cost:,}원 - {deductible:,}원 "
            f"= {before_limit:,}원"
        )

    elif treatment_type == "입원" and coverage_type == "급여":

        current_copay = medical_cost * 0.20
        basic_benefit = medical_cost * 0.80

        annual_copay_limit = 2000000

        previous_excess = max(
            0, previous_copay - annual_copay_limit
        )

        current_excess = max(
            0, previous_copay + current_copay
            - annual_copay_limit
        )

        additional_benefit = current_excess - previous_excess

        total_benefit = basic_benefit + additional_benefit

        result = min(
            int(total_benefit), remaining_limit
        )

        details = [
            f"보장 유형: {insurance_type}",
            f"급여 입원 의료비: {medical_cost:,}원",
            f"기본 보상금액 (80%): {int(basic_benefit):,}원",
            f"추가 보상금액: {int(additional_benefit):,}원",
            f"남은 연간 보장한도: {remaining_limit:,}원"
        ]

        formula = (
            f"{int(basic_benefit):,}원 + "
            f"{int(additional_benefit):,}원 "
            f"= {int(total_benefit):,}원"
        )

    elif treatment_type == "입원" and coverage_type == "비급여":

        basic_benefit = int(medical_cost * 0.70)

        daily_room_cost = room_cost / hospital_days

        eligible_room_cost = (
            min(daily_room_cost, 100000) * hospital_days
        )

        room_benefit = int(eligible_room_cost * 0.50)

        total_benefit = basic_benefit + room_benefit

        result = min(total_benefit, remaining_limit)

        details = [
            f"보장 유형: {insurance_type}",
            f"일반 비급여 의료비: {medical_cost:,}원",
            f"일반 비급여 보상액 (70%): {basic_benefit:,}원",
            f"상급병실료 차액: {room_cost:,}원",
            f"1일 평균 상급병실료: {daily_room_cost:,.0f}원",
            f"상급병실료 보상액 (50%): {room_benefit:,}원",
            f"남은 연간 보장한도: {remaining_limit:,}원"
        ]

        formula = (
            f"{basic_benefit:,}원 + {room_benefit:,}원 "
            f"= {total_benefit:,}원"
        )

    st.success("보험금 계산이 완료되었습니다.")

    st.subheader("예상 보험금")

    st.metric(
        label="예상 지급 보험금",
        value=f"{result:,}원"
    )

    st.divider()
    st.subheader("입력 정보 요약")

    st.write(f"**진료 유형:** {treatment_type}")
    st.write(f"**의료비 구분:** {coverage_name}")

    st.divider()
    st.subheader("계산 상세 내역")

    for item in details:
        st.write(f"- {item}")

    st.markdown("**계산식**")
    st.code(formula)

    st.divider()
    st.subheader("약관 적용 기준")

    if treatment_type == "통원" and coverage_type == "급여":
        st.write(
            "급여 통원: 의료기관 유형에 따른 최소 공제금액과 "
            "보장대상 의료비의 20% 중 큰 금액을 공제하는 방식"
        )

    elif treatment_type == "통원" and coverage_type == "비급여":
        st.write(
            "비급여 통원: 3만원과 보장대상 의료비의 30% 중 "
            "큰 금액을 공제하고 연간 통원 횟수 한도를 적용하는 방식"
        )

    elif treatment_type == "입원" and coverage_type == "급여":
        st.write(
            "급여 입원: 보장대상 의료비의 80%를 기본 계산하고 "
            "연간 본인부담금 기준 추가 보상 계산을 반영한 방식"
        )

    else:
        st.write(
            "비급여 입원: 일반 비급여 의료비 70%와 "
            "상급병실료 차액 보상 기준을 분리해 계산하는 방식"
        )

    st.caption(
        "주의: 현재 계산은 MVP용 단순화 모델입니다. "
        "실제 계약의 가입금액, 연간 누적액, 보장 제외 항목, "
        "특약 및 약관상 세부 조건에 따라 결과가 달라질 수 있습니다."
    )
