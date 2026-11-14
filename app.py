
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
    "실제 보험금 지급 여부와 금액은 보험사의 심사에 따라 달라집니다."
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
    hospital_type = st.selectbox(
        "의료기관 유형",
        [
            "의원급 의료기관·보건소 등",
            "상급종합병원·종합병원 등"
        ]
    )

    medical_cost = st.number_input(
        "급여 보장대상 의료비 (원)",
        min_value=0,
        value=100000,
        step=10000
    )

    coverage_limit = st.number_input(
        "가입한 통원 1회당 보장한도 (원)",
        min_value=1,
        max_value=200000,
        value=200000,
        step=10000
    )

else:
    st.warning("입원 보험금 계산 기능은 다음 단계에서 연결합니다.")

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

        eligible_benefit = max(
            0,
            medical_cost - deductible
        )

        estimated_benefit = min(
            eligible_benefit,
            coverage_limit
        )

        st.subheader("예상 보험금 결과")

        st.metric(
            "예상 보험금",
            f"{estimated_benefit:,}원"
        )

        st.write(f"보장대상 의료비: {medical_cost:,}원")
        st.write(f"최소 공제금액: {minimum_deductible:,}원")
        st.write(f"의료비의 20%: {percentage_deductible:,}원")
        st.write(f"적용 공제금액: {deductible:,}원")
        st.write(f"가입한 보장한도: {coverage_limit:,}원")

        st.success(
            f"예상 보험금은 {estimated_benefit:,}원입니다."
        )

        st.caption(
            "단순화된 급여 통원 계산 결과입니다. "
            "보장 제외 항목, 실제 계약 조건 및 누적 한도는 별도 확인이 필요합니다."
        )

    else:
        st.warning(
            "현재는 급여 통원 계산만 지원합니다. "
            "나머지 계산 기능은 다음 개발 단계에서 추가합니다."
        )
