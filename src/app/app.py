import streamlit as st

st.set_page_config(page_title="Burnout Predictor", page_icon="🔥", layout="wide")

st.markdown(
    """
<style>
.stApp {
    background-image:
            linear-gradient(90deg, rgba(28,17,18,0.18), rgba(28,17,18,0.02)),
            url("https://media.licdn.com/dms/image/v2/D4E22AQH7p1CnOwEabg/feedshare-shrink_800/B4EZsKnzSsHcAg-/0/1765411773608?e=2147483647&v=beta&t=K0gdWtPo8xM6-neDxU2rBGx187LEoGCeTWvKpj29glU");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

.stMain {
    justify-content: center;
}

[data-testid="stAppViewContainer"] {
    background: transparent !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stMainBlockContainer"] {
    max-width: 1060px !important;
    padding-top: 3rem !important;
    padding-bottom: 3rem !important;
}

.st-key-hero_card {
    position: relative !important;
    overflow: hidden !important;
    min-height: 560px;

    border: 1px solid rgba(255,255,255,0.22) !important;
    border-radius: 24px !important;

    background:
    linear-gradient(
        90deg,
        rgba(28,17,18,0.88) 0%,
        rgba(28,17,18,0.82) 40%,
        rgba(28,17,18,0.65) 50%,
        rgba(28,17,18,0.30) 62%,
        rgba(28,17,18,0.00) 78%
    ) !important;

    box-shadow: 0 25px 70px rgba(0,0,0,0.55) !important;
    backdrop-filter: blur(8px);
}

.hero-left {
    padding: 48px 20px 50px 48px;
}

.eyebrow {
    color: rgba(255,255,255,0.48);
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.hero-title {
    color: white;
    font-size: 58px;
    font-weight: 600;
    line-height: 0.98;
    letter-spacing: -2px;
    margin-bottom: 22px;
}

.hero-title span {
    display: block;
    background: linear-gradient(90deg, #f58b61, #e74c3c, #c0392b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-description {
    color: rgba(255,255,255,0.68);
    font-size: 16px;
    line-height: 1.55;
    max-width: 440px;
    margin-bottom: 28px;
}

.features {
    display: flex;
    gap: 20px;
    margin-bottom: 30px;
}

.feature {
    display: flex;
    align-items: center;
    gap: 9px;
}

.feature-icon {
    width: 39px;
    height: 39px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 9px;
    background: rgba(255,255,255,0.08);
    color: #f28b68;
    font-size: 19px;
}

.feature-title {
    color: rgba(255,255,255,0.9);
    font-size: 11px;
}

.feature-text {
    color: rgba(255,255,255,0.4);
    font-size: 9px;
    margin-top: 3px;
}

.stButton {
    margin-top: 5px;
    padding-left: 50px;
}

.stButton > button {
    width: 305px !important;
    height: 58px !important;
    border: none !important;
    border-radius: 30px !important;
    background: linear-gradient(100deg, #f58b61, #e74c3c, #c0392b);
    color: white !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    box-shadow: 0 8px 25px rgba(230,105,115,0.22);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 30px rgba(230,105,115,0.35);
}

.disclaimer {
    color: rgba(255,255,255,0.28);
    font-size: 11px;
    margin-top: 16px;
    padding: 48px 20px 35px 48px
}

.hero-image {
    height: 560px;
    margin: -1px -12px -1px 0;
    position: relative;
    overflow: hidden;
    border-left: 1px solid rgba(255,255,255,0.12);
    background-size: cover;
    background-position: center;
}

.right-text {
    position: absolute;
    top: 125px;
    right: 35px;
    width: 150px;
    color: rgba(255,255,255,0.58);
    font-size: 12px;
    line-height: 1.6;
    letter-spacing: 2px;
    text-align: center;
    transform: rotate(-8deg);
}

.right-text span {
    display: block;
    font-size: 27px;
    margin-top: 5px;
}

.small-steps {
    position: absolute;
    right: 32px;
    bottom: 70px;
    color: rgba(255,255,255,0.38);
    font-size: 9px;
    letter-spacing: 2px;
    text-align: right;
}

@media (max-width: 800px) {
    [data-testid="stMainBlockContainer"] {
        padding: 1.5rem 1rem !important;
    }

    .hero-left {
        padding: 35px 25px;
    }

    .hero-title {
        font-size: 48px;
    }

    .features {
        flex-direction: column;
        gap: 12px;
    }

    .stButton > button {
        width: 100% !important;
    }

    .hero-image {
        height: 350px;
        border-left: none;
        border-top: 1px solid rgba(255,255,255,0.12);
    }
}
</style>
""",
    unsafe_allow_html=True,
)

with st.container(border=True, key="hero_card"):
    col1, col2 = st.columns([1.08, 0.92], gap="small")

    with col1:
        st.markdown(
            """
            <div class="hero-left">
            <div class="eyebrow">YOUR WELL-BEING MATTERS</div>
            <div class="hero-title">Burnout<span>Predictor</span></div>
            <div class="hero-description">
            A simple way to understand your risk of burnout based on your mental and physical well-being.
            Take a few minutes to answer some questions and get personalized insights.
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Get Started  →"):
            st.switch_page("pages/prediction.py")

        st.markdown(
            """
            <div class="disclaimer">
            This tool is not medically validated and should not be considered medical advice.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="hero-image">
        <div class="right-text">
        A HEALTHIER<br>
        YOU IS A HAPPIER<br>
        YOU
        <span>♡</span>
        </div>

        <div class="small-steps">
        SMALL STEPS<br>
        BIG CHANGES
        </div>
        </div>
        """,
            unsafe_allow_html=True,
        )
