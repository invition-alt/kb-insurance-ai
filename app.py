
import streamlit as st

st.set_page_config(
    page_title="KB 실손보험 계산기",
    page_icon="🏥",
    layout="centered"
)


def calculate_special(cost, visits, previous_paid, annual_limit,
                      previous_visits, visit_limit=None):
    """3대 비급여 1회당 공제 및 연간 한도 계산"""
    deductible = max(30000, int(cost * 0.30))
    benefit_per_visit = max(0, cost - deductible)

    remaining_money = max(0, annual_limit - previous_paid)

    if visit_limit is None:
        allowed_visits = visits
    else:
        remaining_visits = max(0, visit_limit - previous_visits)
        allowed_visits = min(visits, remaining_visits)

    calculated = benefit_per_visit * allowed_visits
    benefit = min(calculated, remaining_money)

    return {
        "deductible": deductible,
        "per_visit": benefit_per_visit,
        "allowed_visits": allowed_visits,
        "calculated": calculated,
        "remaining_money": remaining_money,
        "benefit": benefit
    }


st.title("🏥 KB 4세대 실손보험 계산기")
st.caption("급여·비급여·3대 비급여 통합 예상 보험금 계산")

st.info(
    "포트폴리오용 MVP입니다. 실제 보험금은 가입증권, "
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
st.header("2. 일반 의료비 입력")

st.subheader("급여 의료비")

medical_cost = st.number_input(
    "급여 보장대상 의료비 (원)",
    min_value=0,
    value=100000,
    step=10000
)

st.subheader("일반 비급여 의료비")

non_covered_cost = st.number_input(
    "일반 비급여 보장대상 의료비 (원)",
    min_value=0,
    value=100000,
    step=10000
)

st.caption(
    "일반 비급여에는 도수치료·체외충격파·증식치료, "
    "비급여 주사료, MRI/MRA 비용을 포함하지 마세요."
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
        "기존 비급여 통원 사용 횟수",
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
        "기존 급여 입원 본인부담금 20% 누적액 (원)",
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
st.header("4. 3대 비급여 특약 입력")

st.caption(
    "각 항목의 1회 의료비와 이번 치료 횟수를 입력하세요. "
    "이전까지 지급받은 보험금과 사용 횟수도 입력해야 잔여 한도를 계산할 수 있습니다."
)

# 도수치료 등
st.subheader("① 도수치료·체외충격파·증식치료")

therapy_cost = st.number_input(
    "해당 치료 1회당 비급여 의료비 (원)",
    min_value=0,
    value=0,
    step=10000,
    key="therapy_cost"
)

therapy_visits = st.number_input(
    "이번 치료 횟수",
    min_value=0,
    value=0,
    step=1,
    key="therapy_visits"
)

therapy_previous_paid = st.number_input(
    "기존 연간 지급 보험금 (원)",
    min_value=0,
    value=0,
    step=10000,
    key="therapy_paid"
)

therapy_previous_visits = st.number_input(
    "기존 연간 치료 횟수",
    min_value=0,
    value=0,
    step=1,
    key="therapy_previous"
)

therapy_improved = st.checkbox(
    "최초 10회 이후 추가 치료에 대해 증상 개선·병변 호전이 확인됨",
    value=False
)

st.divider()

# 비급여 주사료
st.subheader("② 비급여 주사료")

injection_cost = st.number_input(
    "주사치료 1회당 비급여 의료비 (원)",
    min_value=0,
    value=0,
    step=10000,
    key="injection_cost"
)

injection_visits = st.number_input(
    "이번 주사치료 횟수",
    min_value=0,
    value=0,
    step=1,
    key="injection_visits"
)

injection_previous_paid = st.number_input(
    "기존 연간 지급 보험금 (원)",
    min_value=0,
    value=0,
    step=10000,
    key="injection_paid"
)

injection_previous_visits = st.number_input(
    "기존 연간 주사치료 횟수",
    min_value=0,
    value=0,
    step=1,
    key="injection_previous"
)

st.caption(
    "항암제·항생제·희귀의약품을 위한 비급여 주사료는 "
    "이 특약이 아닌 일반 비급여 보상 대상일 수 있습니다."
)

st.divider()

# MRI/MRA
st.subheader("③ MRI·MRA")

mri_cost = st.number_input(
    "MRI·MRA 1회당 비급여 의료비 (원)",
    min_value=0,
    value=0,
    step=10000,
    key="mri_cost"
)

mri_visits = st.number_input(
    "이번 MRI·MRA 검사 횟수",
    min_value=0,
    value=0,
    step=1,
    key="mri_visits"
)

mri_previous_paid = st.number_input(
    "기존 연간 지급 보험금 (원)",
    min_value=0,
    value=0,
    step=10000,
    key="mri_paid"
)

st.divider()
st.header("5. 예상 보험금 계산")

if st.button("보험금 계산하기", use_container_width=True):

    급여보험금 = 0
    비급여보험금 = 0
    details = []

    # 일반 급여·비급여 계산
    if treatment_type == "통원":

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

        details.extend([
            f"급여 의료비: {medical_cost:,}원",
            f"급여 공제금액: {급여공제:,}원",
            f"급여 보상액: {급여보험금:,}원",
            f"일반 비급여 의료비: {non_covered_cost:,}원",
            f"일반 비급여 공제금액: {비급여공제:,}원",
            f"일반 비급여 보상액: {비급여보험금:,}원"
        ])

    else:

        기본급여보험금 = int(medical_cost * 0.80)
        현재본인부담금 = medical_cost * 0.20

        연간초과전 = max(0, previous_copay - 2000000)
        연간초과후 = max(
            0,
            previous_copay + 현재본인부담금 - 2000000
        )

        추가급여보험금 = int(연간초과후 - 연간초과전)

        급여계산액 = 기본급여보험금 + 추가급여보험금

        급여보험금 = min(
            급여계산액,
            급여잔여한도
        )

        일반비급여보험금 = int(non_covered_cost * 0.70)

        일평균병실료 = room_cost / hospital_days
        보상대상병실료 = min(
            일평균병실료,
            100000
        ) * hospital_days

        병실료보험금 = int(
            보상대상병실료 * 0.50
        )

        비급여계산액 = 일반비급여보험금 + 병실료보험금

        비급여보험금 = min(
            비급여계산액,
            비급여잔여한도
        )

        details.extend([
            f"급여 의료비: {medical_cost:,}원",
            f"급여 기본 보상액: {기본급여보험금:,}원",
            f"급여 추가 보상액: {추가급여보험금:,}원",
            f"급여 예상 보험금: {급여보험금:,}원",
            f"일반 비급여 의료비: {non_covered_cost:,}원",
            f"일반 비급여 보상액: {일반비급여보험금:,}원",
            f"상급병실료 보상액: {병실료보험금:,}원",
            f"일반 비급여 예상 보험금: {비급여보험금:,}원"
        ])

    # 3대 비급여 계산
    therapy_allowed = min(
        therapy_visits,
        max(0, 50 - therapy_previous_visits)
    )

    initial_remaining = max(
        0,
        10 - therapy_previous_visits
    )

    initial_current = min(
        therapy_allowed,
        initial_remaining
    )

    additional_current = therapy_allowed - initial_current

    if therapy_improved:
        therapy_eligible = initial_current + additional_current
    else:
        therapy_eligible = initial_current

    therapy_result = calculate_special(
        therapy_cost,
        therapy_eligible,
        therapy_previous_paid,
        3500000,
        therapy_previous_visits,
        50
    )

    injection_result = calculate_special(
        injection_cost,
        injection_visits,
        injection_previous_paid,
        2500000,
        injection_previous_visits,
        50
    )

    mri_result = calculate_special(
        mri_cost,
        mri_visits,
        mri_previous_paid,
        3000000,
        0,
        None
    )

    therapy_benefit = therapy_result["benefit"]
    injection_benefit = injection_result["benefit"]
    mri_benefit = mri_result["benefit"]

    special_total = (
        therapy_benefit
        + injection_benefit
        + mri_benefit
    )

    total_benefit = (
        급여보험금
        + 비급여보험금
        + special_total
    )

    # 결과 출력
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
            "일반 비급여 예상 보험금",
            f"{비급여보험금:,}원"
        )

    st.metric(
        "3대 비급여 예상 보험금",
        f"{special_total:,}원"
    )

    st.divider()
    st.subheader("3대 비급여 계산 상세")

    st.write("**① 도수치료·체외충격파·증식치료**")
    st.write(f"- 1회당 의료비: {therapy_cost:,}원")
    st.write(f"- 1회당 공제금액: {therapy_result['deductible']:,}원")
    st.write(f"- 보상 가능한 이번 치료 횟수: {therapy_eligible}회")
    st.write(f"- 기존 사용 횟수: {therapy_previous_visits}회")
    st.write(f"- 예상 보험금: {therapy_benefit:,}원")

    st.write("**② 비급여 주사료**")
    st.write(f"- 1회당 의료비: {injection_cost:,}원")
    st.write(f"- 1회당 공제금액: {injection_result['deductible']:,}원")
    st.write(f"- 보상 적용 횟수: {injection_result['allowed_visits']}회")
    st.write(f"- 예상 보험금: {injection_benefit:,}원")

    st.write("**③ MRI·MRA**")
    st.write(f"- 1회당 의료비: {mri_cost:,}원")
    st.write(f"- 1회당 공제금액: {mri_result['deductible']:,}원")
    st.write(f"- 검사 횟수: {mri_visits}회")
    st.write(f"- 예상 보험금: {mri_benefit:,}원")

    st.divider()
    st.subheader("전체 계산 내역")

    for item in details:
        st.write(f"- {item}")

    st.divider()
    st.subheader("적용 기준")

    st.write(
        "3대 비급여는 각각 연간 한도를 별도로 적용합니다. "
        "도수치료·체외충격파·증식치료는 합산 연 350만원 및 50회, "
        "비급여 주사료는 연 250만원 및 50회, "
        "MRI·MRA는 연 300만원 한도입니다."
    )

    st.write(
        "3대 비급여의 1회당 공제금액은 "
        "3만원과 보장대상 의료비의 30% 중 큰 금액입니다."
    )

    st.write(
        "도수치료 등은 최초 10회 이후 증상 개선이나 "
        "병변 호전이 확인된 경우 추가 보상을 적용하도록 "
        "단순화했습니다."
    )

    st.caption(
        "본 계산기는 업로드된 2021년 약관을 기준으로 만든 "
        "포트폴리오용 단순화 모델입니다. 실제 지급 여부는 "
        "가입증권, 특약 가입 여부, 보상 제외 사유, 누적 지급액, "
        "치료 인정 기준 및 보험사 심사에 따라 달라질 수 있습니다."
    )


    st.divider()
    st.subheader("약관 근거 및 적용 페이지")

    st.caption(
        "아래 페이지는 업로드된 약관 PDF 뷰어 기준입니다. "
        "실제 계약의 가입증권·특약 및 개정 약관에 따라 달라질 수 있습니다."
    )

    if medical_cost > 0:
        with st.expander("급여 의료비 근거", expanded=True):
            st.write(
                "- 근거: 보통약관 제3조(보험금의 지급사유) 및 제5조(보험금의 지급한도)"
            )
            if treatment_type == "통원":
                st.write(
                    "- 적용 내용: 급여 통원 의료비에서 의료기관 유형별 최소 공제금액과 "
                    "보장대상 의료비의 20% 중 큰 금액을 공제한 뒤, 1회 한도와 연간 잔여한도를 적용"
                )
            else:
                st.write(
                    "- 적용 내용: 급여 입원 의료비의 80%를 기본 보상하고, "
                    "연간 급여 본인부담금 200만원 초과분 관련 기준을 반영"
                )
            st.write("- PDF 위치: 11~12쪽(급여 보상 기준), 17쪽(급여 연간 한도)")

    if non_covered_cost > 0 or (treatment_type == "입원" and room_cost > 0):
        with st.expander("일반 비급여 의료비 근거", expanded=True):
            st.write(
                "- 근거: 보통약관의 비급여 보상 관련 조항 및 지급한도 조항"
            )
            if treatment_type == "통원":
                st.write(
                    "- 적용 내용: 3만원과 보장대상 의료비의 30% 중 큰 금액을 공제하고, "
                    "통원 1회 한도·연간 잔여한도·연 100회 제한을 적용"
                )
            else:
                st.write(
                    "- 적용 내용: 일반 비급여 입원 의료비의 70% 및 상급병실료 차액의 "
                    "50%(1일 평균 10만원 한도)를 기준으로 계산"
                )
            st.write("- PDF 위치: 39~40쪽")

    if therapy_cost > 0:
        with st.expander("도수치료·체외충격파·증식치료 근거", expanded=True):
            st.write(
                "- 근거: 3대 비급여 특별약관의 도수치료·체외충격파·증식치료 보상 규정"
            )
            st.write(
                "- 적용 내용: 1회당 3만원과 보장대상 의료비의 30% 중 큰 금액 공제, "
                "연간 350만원 및 합산 50회 한도"
            )
            st.write(
                "- 추가 조건: 최초 10회 이후에는 증상 개선 또는 병변 호전 확인 등 "
                "약관상 요건에 따라 추가 보상 여부 판단"
            )
            st.write("- PDF 위치: 43~44쪽")

    if injection_cost > 0:
        with st.expander("비급여 주사료 근거", expanded=True):
            st.write(
                "- 근거: 3대 비급여 특별약관의 비급여 주사료 보상 규정"
            )
            st.write(
                "- 적용 내용: 1회당 3만원과 보장대상 의료비의 30% 중 큰 금액 공제, "
                "연간 250만원 및 50회 한도"
            )
            st.write("- PDF 위치: 43~44쪽")

    if mri_cost > 0:
        with st.expander("MRI·MRA 근거", expanded=True):
            st.write(
                "- 근거: 3대 비급여 특별약관의 MRI·MRA 보상 규정"
            )
            st.write(
                "- 적용 내용: 1회당 3만원과 보장대상 의료비의 30% 중 큰 금액 공제, "
                "연간 300만원 한도"
            )
            st.write("- PDF 위치: 43~44쪽")
