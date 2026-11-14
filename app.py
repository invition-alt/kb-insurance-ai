
import streamlit as st

st.set_page_config(
    page_title="KB 실손보험 계산기",
    page_icon="🏥",
    layout="centered"
)

st.title("🏥 KB 실손보험 보험금 계산기")
st.write("의료비 정보를 입력하면 예상 보험금을 계산합니다.")

st.info(
    "본 서비스는 포트폴리오용 예상 계산 서비스입니다. "
    "실제 지급 여부와 금액은 보험사의 심사에 따라 달라집니다."
)

st.divider()

st.header("1. 보험 정보")
st.selectbox("보험사", ["KB손해보험"])
st.selectbox("실손보험 세대", ["4세대"])

st.divider()

st.header("2. 진료 정보")

treatment_type = st.radio(
    "진료 유형", ["통원", "입원"], horizontal=True
)

coverage_type = st.radio(
    "의료비 구분", ["급여", "비급여"], horizontal=True
)

st.divider()
st.header("3. 의료비 입력")

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
st.header("4. 예상 보험금 확인")

if st.button("보험금 계산하기", use_container_width=True):

    if treatment_type == "통원" and coverage_type == "급여":

        minimum_deductible = (
            10000 if hospital_type == "의원급 의료기관·보건소 등"
            else 20000
        )

        deductible = max(
            minimum_deductible,
            int(medical_cost * 0.20)
        )

        estimated_benefit = min(
            max(0, medical_cost - deductible),
            coverage_limit
        )

        st.subheader("예상 보험금 결과")
        st.metric("예상 보험금", f"{estimated_benefit:,}원")
        st.write(f"보장대상 의료비: {medical_cost:,}원")
        st.write(f"적용 공제금액: {deductible:,}원")
        st.write(f"가입한 보장한도: {coverage_limit:,}원")

    elif treatment_type == "통원" and coverage_type == "비급여":

        deductible = max(
            30000, int(medical_cost * 0.30)
        )

        benefit_before_limit = max(
            0, medical_cost - deductible
        )

        estimated_benefit = (
            0 if previous_visits >= 100
            else benefit_before_limit
        )

        st.subheader("예상 보험금 결과")
        st.metric("예상 보험금", f"{estimated_benefit:,}원")
        st.write(f"비급여 의료비: {medical_cost:,}원")
        st.write(f"적용 공제금액: {deductible:,}원")
        st.write(f"기존 사용 횟수: {previous_visits}회")

        if previous_visits >= 100:
            st.warning("연간 비급여 통원 100회 한도를 모두 사용했습니다.")

    elif treatment_type == "입원" and coverage_type == "급여":

        current_copay = medical_cost * 0.20
        basic_benefit = medical_cost * 0.80

        annual_copay_limit = 2000000

        previous_excess = max(
            0, previous_copay - annual_copay_limit
        )

        current_excess = max(
            0, previous_copay + current_copay - annual_copay_limit
        )

        additional_benefit = current_excess - previous_excess

        total_benefit = basic_benefit + additional_benefit

        estimated_benefit = min(
            int(total_benefit), remaining_limit
        )

        st.subheader("예상 보험금 결과")
        st.metric("예상 보험금", f"{estimated_benefit:,}원")
        st.write(f"보장 유형: {insurance_type}")
        st.write(f"기본 보상금액: {int(basic_benefit):,}원")
        st.write(f"추가 보상금액: {int(additional_benefit):,}원")
        st.write(f"남은 연간 보장한도: {remaining_limit:,}원")

    elif treatment_type == "입원" and coverage_type == "비급여":

        # 일반 비급여 입원 의료비의 70% 보상
        basic_benefit = int(medical_cost * 0.70)

        # 상급병실료 차액은 1일 평균 10만원 한도,
        # 해당 한도 내 금액의 50% 보상
        daily_room_cost = room_cost / hospital_days

        eligible_room_cost = min(
            daily_room_cost, 100000
        ) * hospital_days

        room_benefit = int(
            eligible_room_cost * 0.50
        )

        total_benefit = (
            basic_benefit + room_benefit
        )

        estimated_benefit = min(
            total_benefit, remaining_limit
        )

        st.subheader("예상 보험금 결과")
        st.metric("예상 보험금", f"{estimated_benefit:,}원")

        st.write(f"보장 유형: {insurance_type}")
        st.write(f"일반 비급여 입원 의료비: {medical_cost:,}원")
        st.write(f"일반 비급여 보상액 (70%): {basic_benefit:,}원")
        st.write(f"상급병실료 차액 총액: {room_cost:,}원")
        st.write(f"입원 일수: {hospital_days}일")
        st.write(f"1일 평균 상급병실료: {daily_room_cost:,.0f}원")
        st.write(f"상급병실료 보상액 (50%): {room_benefit:,}원")
        st.write(f"남은 연간 보장한도: {remaining_limit:,}원")

        st.caption(
            "약관상 일반 비급여 입원과 상급병실료 차액을 "
            "분리한 단순화 계산입니다. 실제 계약의 연간 한도, "
            "보장 제외 항목 및 기타 지급 조건을 확인해야 합니다."
        )
