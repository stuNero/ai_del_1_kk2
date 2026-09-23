"""CSS för prediction.py, utbrutet till egen fil för att hålla huvudfilen kortare."""

PREDICTION_CSS = """
    <style>

    .stApp {
        background-image: url("https://media.licdn.com/dms/image/v2/D4E22AQH7p1CnOwEabg/feedshare-shrink_800/B4EZsKnzSsHcAg-/0/1765411773608?e=2147483647&v=beta&t=K0gdWtPo8xM6-neDxU2rBGx187LEoGCeTWvKpj29glU");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    .stMain {
        justify-content: center;
    }

    [data-testid="stAppViewContainer"] {
        background: linear-gradient(90deg, rgba(28,17,18,0.18), rgba(28,17,18,0.02));
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .st-key-question_card[data-testid="stVerticalBlockBorderWrapper"],
    .st-key-question_card[data-testid="stVerticalBlock"],
    .st-key-result_card[data-testid="stVerticalBlockBorderWrapper"],
    .st-key-result_card[data-testid="stVerticalBlock"] {
        position: relative;
        isolation: isolate;
        border: 1px solid rgba(255, 255, 255, 0.22);
        border-radius: 24px;
        box-shadow: 0 25px 70px rgba(0, 0, 0, 0.55), 0 0 90px rgba(230, 105, 85, 0.12);
        overflow: hidden;
        padding: 48px 56px;
        animation: fadeSlideIn 0.4s ease-out;
        backdrop-filter: blur(8px);
    }

    @keyframes fadeSlideIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .st-key-question_card[data-testid="stVerticalBlockBorderWrapper"]::before,
    .st-key-question_card[data-testid="stVerticalBlock"]::before,
    .st-key-result_card[data-testid="stVerticalBlockBorderWrapper"]::before,
    .st-key-result_card[data-testid="stVerticalBlock"]::before {
        content: "";
        position: absolute;
        inset: 0;
        background: rgba(28, 17, 18, 0.78);
        z-index: 0;
        border-radius: 24px;
    }

    .st-key-question_card[data-testid="stVerticalBlockBorderWrapper"] > div,
    .st-key-question_card[data-testid="stVerticalBlock"] > div,
    .st-key-result_card[data-testid="stVerticalBlockBorderWrapper"] > div,
    .st-key-result_card[data-testid="stVerticalBlock"] > div {
        position: relative;
        z-index: 1;
    }

    .question-title {
        color: white;
        font-size: 34px;
        font-weight: 700;
        letter-spacing: -0.5px;
        text-align: center;
    }

    .question-description {
        color: rgba(255, 255, 255, 0.68);
        font-size: 16px;
        line-height: 1.55;
        text-align: center;
        margin-bottom: 28px;
    }

    .progress-label {
        color: rgba(255, 255, 255, 0.48);
        font-size: 12px;
        letter-spacing: 1px;
        text-align: right;
        margin-bottom: 8px;
    }

    [data-testid="stProgress"] div[role="progressbar"] {
        background-color: rgba(255, 255, 255, 0.18);
        border-radius: 10px;
        height: 10px;
        overflow: hidden;
    }

    [data-testid="stProgress"] div[role="progressbar"] > div,
    [data-testid="stProgress"] div[role="progressbar"] > div > div {
        border-radius: 10px;
        height: 100%;
        box-shadow: 0 0 12px rgba(230, 105, 85, 0.5);
    }

    [data-testid="stSelectbox"] > div > div {
        background-color: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.16);
        border-radius: 12px;
    }

    [data-testid="stSelectbox"] > div > div:focus-within {
        border-color: #e8845f;
        box-shadow: 0 0 0 2px rgba(230, 105, 85, 0.22);
    }

    [data-baseweb="radio"] div:first-child {
        border-color: rgba(230, 105, 85, 0.55);
    }

    [data-testid="stSlider"] [role="slider"] {
        background-color: #e8845f;
        box-shadow: 0 0 0 4px rgba(230, 105, 85, 0.2);
    }

    [data-testid="stSlider"] [data-testid="stThumbValue"],
    [data-testid="stSlider"] .StyledThumbValue {
        background: rgba(20, 12, 13, 0.92);
        color: #ffffff;
        font-weight: 700;
        border: 1px solid rgba(230, 105, 85, 0.5);
        border-radius: 8px;
        padding: 3px 8px;
    }

    [data-testid="stSlider"] [data-testid="stTickBarMin"],
    [data-testid="stSlider"] [data-testid="stTickBarMax"],
    [data-testid="stSlider"] .StyledTickBar * {
        color: rgba(255, 255, 255, 0.55);
        font-size: 13px;
    }

    .stButton > button {
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        background: rgba(255, 255, 255, 0.22);
        color: white;
        font-size: 15px;
        font-weight: 600;
        padding: 14px 0;
        transition: all 0.25s ease;
    }

    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: translateY(-1px);
    }

    .stButton > button:disabled {
        opacity: 0.35;
        border-color: rgba(255, 255, 255, 0.1);
        background: rgba(255, 255, 255, 0.06);
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(100deg, #f58b61, #e74c3c, #c0392b);
        border: none;
        box-shadow: 0 8px 25px rgba(230, 105, 85, 0.3);
    }

    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 12px 30px rgba(230, 105, 85, 0.4);
        transform: translateY(-2px);
    }

    .score-container {
        text-align: center;
        margin: 40px 0;
    }

    .score-value {
        display: inline-block;
        font-size: 64px;
        font-weight: 800;
    }

    .score-value-unit {
        color: #ffffff;
        font-weight: 400;
    }

    .score-eyebrow {
        color: rgba(255, 255, 255, 0.45);
        font-size: 12px;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .score-label {
        color: rgba(255, 255, 255, 0.68);
        font-size: 16px;
        margin-top: 10px;
    }

    .risk-summary-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }

    .risk-summary-label {
        color: rgba(255, 255, 255, 0.6);
        font-size: 14px;
    }

    .risk-summary-value {
        font-weight: 700;
        font-size: 14px;
    }

    .risk-track {
        width: 100%;
        height: 8px;
        background: rgba(255, 255, 255, 0.15);
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 24px;
    }

    .risk-fill {
        height: 100%;
        border-radius: 10px;
    }

    .risk-box {
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 24px;
    }

    .risk-box-title {
        font-weight: 700;
        font-size: 18px;
        margin-bottom: 6px;
    }

    .risk-box-message {
        color: rgba(255, 255, 255, 0.75);
        font-size: 15px;
        line-height: 1.5;
    }

    .recommendations-title {
        color: white;
        font-size: 24px;
        font-weight: 800;
        margin-bottom: 12px;
    }

    .recommendation-item {
        padding: 18px 0 18px 16px;
        border-left: 3px solid transparent;
        border-bottom: 1px solid rgba(255, 255, 255, 0.12);
        margin-bottom: 4px;
    }

    .recommendation-item:last-child {
        border-bottom: none;
        margin-bottom: 0;
    }

    .recommendation-title {
        color: #ffffff;
        font-weight: 700;
        font-size: 15px;
        margin-bottom: 4px;
    }

    .recommendation-description {
        color: rgba(255, 255, 255, 0.6);
        font-size: 14px;
    }

    h1, h2, h3, p {
        color: #ffffff;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
    }

    label {
        color: #ffffff;
    }

    .st-key-home_button button {
        background: transparent;
        border: none;
        color: rgba(255, 255, 255, 0.35);
        font-size: 12px;
        font-weight: 400;
        padding: 4px 8px;
        width: auto !important;
        box-shadow: none;
    }

    .st-key-home_button button:hover {
        color: rgba(255, 255, 255, 0.7);
        background: transparent;
        transform: none;
    }

    @media (max-width: 800px) {
        [data-testid="stMainBlockContainer"] {
            padding-top: 1rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .st-key-question_card[data-testid="stVerticalBlockBorderWrapper"],
        .st-key-question_card[data-testid="stVerticalBlock"] {
            padding: 30px 20px;
        }

        .question-title {
            font-size: 24px;
        }
    }
    </style>
"""
