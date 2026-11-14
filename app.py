
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
    "진료 유형",
    ["통원", "입원"],
    horizontal=True
)

coverage_type = st.radio(
    "의료비 구분",
    ["급여", "비급여"],
    horizontal=True
)

st.divider()

st.header("3. 의료비 입력")

if treatment_type == "통원":

    if coverage_type == "급여":
        medical_cost = st.number_input(
            "급여 보장대상 의료비 (원)",
            min_value=0,
            value=100000,
            step=10000
        )

        hospital_type = st.selectbox(
            "의료기관 유형",
            [
                "의원급 의료기관·보건소 등",
                "상급종합병원·종합병원 등"
            ]
        )

        coverage_limit = st.number_input(
            "가입한 통원 1회당 보장한도 (원)",
            min_value=1,
            max_value=200000,
            value=200000,
            step=10000
        )

    else:
        medical_cost = st.number_input(
            "비급여 보장대상 의료비 (원)",
            min_value=0,
            value=100000,
            step=10000
        )

        previous_visits = st.number_input(
            "해당 보험연도 이전까지 사용한 비급여 통원 횟수",
            min_value=0,
            max_value=100,
            value=0,
            step=1
        )

else:

    medical_cost = st.number_input(
        "보장대상 의료비 (원)",
        min_value=0,
        value=1000000,
        step=10000
    )

    if coverage_type == "급여":

        insurance_type = st.selectbox(
            "보장 유형",
            ["상해급여", "질병급여"]
        )

        previous_copay = st.number_input(
            "해당 보험연도 이전까지 누적된 입원 본인부담금 20% (원)",
            min_value=0,
            value=0,
            step=10000
        )

        remaining_limit = st.number_input(
            "해당 보장 유형의 남은 연간 보험가입금액 (원)",
            min_value=0,
            max_value=50000000,
            value=50000000,
            step=100000
        )

st.divider()

st.header("4. 예상 보험금 확인")

if st.button("보험금 계산하기", use_container_width=True):

    if treatment_type == "통원" and coverage_type == "급여":

        if hospital_type == "의원급 의료기관·보건소 등":
            minimum_deductible = 10000
        else:
            minimum_deductible = 20000

        percentage_deductible = int(medical_cost * 0.20)

        deductible = max(
            minimum_deductible,
            percentage_deductible
        )

        benefit_before_limit = max(
            0,
            medical_cost - deductible
        )

        estimated_benefit = min(
            benefit_before_limit,
            coverage_limit
        )

        st.subheader("예상 보험금 결과")
        st.metric("예상 보험금", f"{estimated_benefit:,}원")

        st.write(f"보장대상 의료비: {medical_cost:,}원")
        st.write(f"적용 공제금액: {deductible:,}원")
        st.write(f"가입한 보장한도: {coverage_limit:,}원")

    elif treatment_type == "통원" and coverage_type == "비급여":

        minimum_deductible = 30000
        percentage_deductible = int(medical_cost * 0.30)

        deductible = max(
            minimum_deductible,
            percentage_deductible
        )

        benefit_before_limit = max(
            0,
            medical_cost - deductible
        )

        if previous_visits >= 100:
            estimated_benefit = 0
            st.warning("해당 보험연도의 비급여 통원 100회 한도를 모두 사용했습니다.")
        else:
            estimated_benefit = benefit_before_limit

        st.subheader("예상 보험금 결과")
        st.metric("예상 보험금", f"{estimated_benefit:,}원")

        st.write(f"비급여 보장대상 의료비: {medical_cost:,}원")
        st.write(f"최소 공제금액: {minimum_deductible:,}원")
        st.write(f"의료비의 30%: {percentage_deductible:,}원")
        st.write(f"적용 공제금액: {deductible:,}원")
        st.write(f"기존 사용 횟수: {previous_visits}회")
        st.write(f"이번 통원 후 사용 횟수: {previous_visits + 1}회")

        st.caption(
            "비급여 통원 1회 기준의 단순화된 계산입니다. "
            "연간 보험가입금액 한도, 보장 제외 항목 및 실제 계약 조건은 "
            "별도로 확인해야 합니다."
        )

    elif treatment_type == "입원" and coverage_type == "급여":

        current_copay = medical_cost * 0.20
        basic_benefit = medical_cost * 0.80

        annual_copay_limit = 2000000

        previous_excess = max(
            0,
            previous_copay - annual_copay_limit
        )

        current_excess = max(
            0,
            previous_copay + current_copay - annual_copay_limit
        )

        additional_benefit = current_excess - previous_excess

        total_benefit = basic_benefit + additional_benefit

        estimated_benefit = min(
            int(total_benefit),
            remaining_limit
        )

        st.subheader("예상 보험금 결과")
        st.metric("예상 보험금", f"{estimated_benefit:,}원")

        st.write(f"보장 유형: {insurance_type}")
        st.write(f"보장대상 의료비: {medical_cost:,}원")
        st.write(f"기본 보상금액 (80%): {int(basic_benefit):,}원")
        st.write(f"이번 입원 본인부담금 20%: {int(current_copay):,}원")
        st.write(f"기존 누적 본인부담금: {previous_copay:,}원")
        st.write(f"200만원 초과분 추가 보상: {int(additional_benefit):,}원")
        st.write(f"남은 연간 보장한도: {remaining_limit:,}원")

    else:

        st.warning("비급여 입원 계산 기능은 다음 단계에서 추가합니다.")
