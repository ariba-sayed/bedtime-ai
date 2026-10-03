import streamlit as st
import time
import re
from html import escape
from story_agent import generate_story


def sanitize_story(text: str) -> str:
    """Remove HTML/fenced-markup from model output before rendering."""
    if not text:
        return ""

    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'^.*```.*$', '', text, flags=re.M)
    text = text.replace('`', '')
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    return text.strip()


header_left, header_right = st.columns([7, 3])

if "story_generated" not in st.session_state:
    st.session_state.story_generated = False

if "story" not in st.session_state:
    st.session_state.story = ""

if "language" not in st.session_state:
    st.session_state.language = "English"

with header_left:
    st.markdown(
        """
        <div class="brand">
            🌙 DreamTales
        </div>
        """,
        unsafe_allow_html=True
    )
# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="DreamTales",
    page_icon="🌙",
    layout="centered",
    initial_sidebar_state="collapsed"
)


    
# -----------------------------
# CUSTOM STYLING
# -----------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Nunito:wght@400;500;600;700;800&display=swap');

.stApp {
    background:
        radial-gradient(circle at 15% 15%, rgba(120, 91, 180, 0.18), transparent 25%),
        radial-gradient(circle at 85% 20%, rgba(65, 92, 160, 0.15), transparent 25%),
        linear-gradient(145deg, #080b24 0%, #111337 45%, #17133b 100%);
    color: #f8f3e8;
    min-height: 100vh;
}
.language-toggle {
    text-align: right;
    margin-bottom: 10px;
}

.language-toggle span {
    color: #aaa;
    font-size: 14px;
    margin-left: 10px;
}

.language-toggle .active {
    color: #ffffff;
    font-weight: 600;
}
.block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Hide Streamlit chrome */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

/* -----------------------------
   NIGHT SKY
----------------------------- */

.sky {
    text-align: center;
    height: 105px;
    position: relative;
    margin-bottom: 5px;
}

.moon {
    font-size: 55px;
    filter: drop-shadow(0 0 18px rgba(255, 238, 180, 0.35));
}

.star {
    position: absolute;
    font-size: 13px;
    opacity: 0.8;
}

.s1 { left: 18%; top: 10px; }
.s2 { left: 30%; top: 52px; }
.s3 { right: 20%; top: 18px; }
.s4 { right: 32%; top: 60px; }
.s5 { left: 10%; top: 70px; }
.s6 { right: 10%; top: 72px; }

/* -----------------------------
   TITLE
----------------------------- */

.logo {
    text-align: center;
    font-family: 'DM Serif Display', serif;
    font-size: 52px;
    letter-spacing: 1px;
    color: #fff7df;
    margin-top: -5px;
    margin-bottom: 0;
}

.subtitle {
    text-align: center;
    font-family: 'Nunito', sans-serif;
    color: #c8c5df;
    font-size: 17px;
    margin-bottom: 25px;
}

/* -----------------------------
   SETUP CARD
----------------------------- */

.setup-card {
    background: rgba(24, 26, 64, 0.78);
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 24px;
    padding: 26px 30px 22px 30px;
    box-shadow: 0 18px 50px rgba(0, 0, 0, 0.25);
    margin-bottom: 15px;
}

.card-heading {
    font-family: 'DM Serif Display', serif;
    font-size: 25px;
    color: #fff3d0;
    margin-bottom: 5px;
}

.card-description {
    font-family: 'Nunito', sans-serif;
    color: #aaa9c5;
    font-size: 14px;
    margin-bottom: 18px;
}

/* -----------------------------
   STREAMLIT INPUTS
----------------------------- */

.stTextInput label,
.stNumberInput label,
.stSelectbox label {
    color: #dedcf0 !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
}

.stTextInput input,
.stNumberInput input {
    background: rgba(8, 10, 35, 0.75) !important;
    color: #fff7e8 !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    border-radius: 12px !important;
}

.stTextInput input::placeholder {
    color: #777793 !important;
}

.stSelectbox [data-baseweb="select"] {
    background: rgba(8, 10, 35, 0.75) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
}

.stSelectbox [data-baseweb="select"] * {
    color: #fff7e8 !important;
}

/* -----------------------------
   BUTTON
----------------------------- */

.stButton > button {
    width: 100%;
    border-radius: 14px;
    border: none;
    padding: 12px 18px;
    background: linear-gradient(135deg, #8c70d8, #b07bd8);
    color: white;
    font-family: 'Nunito', sans-serif;
    font-size: 16px;
    font-weight: 800;
    box-shadow: 0 8px 25px rgba(130, 95, 190, 0.30);
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 30px rgba(130, 95, 190, 0.40);
}

/* -----------------------------
   GENERATING SCREEN
----------------------------- */

.generating {
    text-align: center;
    padding: 65px 20px;
}

.generating-moon {
    font-size: 55px;
    margin-bottom: 15px;
}

.generating-title {
    font-family: 'DM Serif Display', serif;
    font-size: 31px;
    color: #fff2d0;
}

.generating-text {
    color: #aaa9c5;
    font-family: 'Nunito', sans-serif;
    margin-top: 8px;
}

/* -----------------------------
   STORY PAGE
----------------------------- */

.story-header {
    text-align: center;
    margin-bottom: 18px;
}

.story-label {
    color: #a99be0;
    font-family: 'Nunito', sans-serif;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.story-title {
    font-family: 'DM Serif Display', serif;
    color: #fff3d0;
    font-size: 39px;
    line-height: 1.1;
    margin: 5px 0;
}

.story-subtitle {
    color: #aaa9c5;
    font-family: 'Nunito', sans-serif;
    font-size: 14px;
}

/* Storybook paper */

.storybook {
    background: #f8f0df;
    color: #302a36;
    border-radius: 20px;
    padding: 38px 42px;
    box-shadow:
        0 25px 60px rgba(0,0,0,0.35),
        inset 0 0 0 1px rgba(100,70,40,0.08);
    margin-bottom: 20px;
}

.storybook h2 {
    font-family: 'DM Serif Display', serif;
    color: #493c59;
    font-size: 27px;
    margin-bottom: 20px;
}

.storybook p {
    font-family: Georgia, serif;
    font-size: 17px;
    line-height: 1.8;
    margin-bottom: 18px;
}

.storybook .dropcap {
    float: left;
    font-family: 'DM Serif Display', serif;
    font-size: 54px;
    line-height: 42px;
    padding-right: 7px;
    color: #8060a9;
}

/* -----------------------------
   SECTION HEADINGS
----------------------------- */

.section-title {
    font-family: 'DM Serif Display', serif;
    color: #fff2d0;
    font-size: 24px;
    margin: 20px 0 10px 0;
}

.small-text {
    color: #aaa9c5;
    font-family: 'Nunito', sans-serif;
    font-size: 14px;
}

/* -----------------------------
   CHOICE CARDS
----------------------------- */

.choice-card {
    background: rgba(30, 31, 70, 0.8);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 16px;
    padding: 15px;
    text-align: center;
    color: #eee9f8;
    font-family: 'Nunito', sans-serif;
    font-weight: 700;
    margin-bottom: 8px;
}

/* -----------------------------
   FOOTER
----------------------------- */

.footer {
    text-align: center;
    color: #777694;
    font-family: 'Nunito', sans-serif;
    font-size: 12px;
    margin-top: 28px;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# SESSION STATE
# -----------------------------

if "story_generated" not in st.session_state:
    st.session_state.story_generated = False

if "child_name" not in st.session_state:
    st.session_state.child_name = ""

if "age" not in st.session_state:
    st.session_state.age = 0

if "animal" not in st.session_state:
    st.session_state.animal = ""

if "character" not in st.session_state:
    st.session_state.character = ""

if "setting" not in st.session_state:
    st.session_state.setting = ""

if "mood" not in st.session_state:
    st.session_state.mood = ""

if "selected_language" not in st.session_state:
    st.session_state.selected_language = "English"

# -----------------------------
# NIGHT SKY
# -----------------------------

st.markdown("""
<div class="sky">
    <span class="star s1">✦</span>
    <span class="star s2">✧</span>
    <span class="star s3">✦</span>
    <span class="star s4">✧</span>
    <span class="star s5">·</span>
    <span class="star s6">✦</span>
    <div class="moon">🌙</div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# SETUP PAGE
# =========================================================

if not st.session_state.story_generated:

    st.markdown(
        '<div class="logo">DreamTales</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Tonight, a little adventure begins...</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="setup-card">
        <div class="card-heading">✨ Who is tonight's hero?</div>
        <div class="card-description">
            Tell us a little about them and we'll create a magical bedtime adventure.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # First row
    col1, col2 = st.columns(2)

    with col1:
        child_name = st.text_input(
            "Child's name",
            placeholder="e.g. Aanya"
        )

    with col2:
        age = st.number_input(
            "Age",
            min_value=2,
            max_value=12,
            value=6
        )

    # Second row
    col1, col2 = st.columns(2)

    with col1:
        animal = st.selectbox(
            "Favorite animal",
            [
                "🐰 Rabbit",
                "🐱 Cat",
                "🐶 Dog",
                "🦊 Fox",
                "🐻 Bear",
                "🦄 Unicorn",
                "🐼 Panda",
                "🐯 Tiger",
                "🐉 Dragon",
                "✨ Something else"
            ]
        )

    with col2:
        character = st.selectbox(
            "Favorite character type",
            [
                "👑 Brave princess",
                "⚔️ Young knight",
                "🧙 Little wizard",
                "🧚 Curious fairy",
                "🚀 Space explorer",
                "🧜 Ocean adventurer",
                "🐉 Friendly dragon",
                "✨ Something else"
            ]
        )

    # Setting
    setting = st.selectbox(
        "🌎 Where should tonight's adventure happen?",
        [
            "🌲 A magical forest",
            "🏰 An enchanted castle",
            "🌊 An underwater kingdom",
            "🚀 A distant planet",
            "🧚 A tiny fairy village",
            "☁️ A kingdom above the clouds",
            "✨ Somewhere else"
        ]
    )

    custom_setting = ""

    if setting == "✨ Somewhere else":
        custom_setting = st.text_input(
            "Describe the place",
            placeholder="e.g. a city made entirely of candy"
        )

    # Mood
    mood = st.selectbox(
        "💫 What should the story feel like?",
        [
            "😄 Funny",
            "✨ Magical",
            "🗺️ Adventurous",
            "🌙 Calm",
            "💛 Heartwarming",
            "✨ Something else"
        ]
    )

    custom_mood = ""

    if mood == "✨ Something else":
        custom_mood = st.text_input(
            "Describe the mood",
            placeholder="e.g. mysterious but cozy"
        )

    # Length
    length = st.selectbox(
        "📖 Story length",
        [
            "Short",
            "Medium",
            "Long"
        ]
    )

    st.write("")

    # -----------------------------
    # CREATE STORY
    # -----------------------------

    if st.button("✨ Begin Tonight's Adventure"):

        if not child_name.strip():
            st.warning("Tell us the hero's name first 🌙")
            st.stop()

        # Clean user inputs
        safe_name = escape(child_name.strip())
        safe_animal = escape(animal)
        safe_character = escape(character)

        if setting == "✨ Somewhere else":
            safe_setting = escape(custom_setting.strip() or "a mysterious magical place")
        else:
            safe_setting = escape(setting)

        if mood == "✨ Something else":
            safe_mood = escape(custom_mood.strip() or "magical")
        else:
            safe_mood = escape(mood)

        st.markdown("""
        <div class="generating">
            <div class="generating-moon">🌙</div>
            <div class="generating-title">Creating your story...</div>
            <div class="generating-text">
                ✦ Finding a magical world
            </div>
        </div>
        """, unsafe_allow_html=True)

        time.sleep(0.7)

        st.session_state.child_name = child_name.strip()
        st.session_state.age = age
        st.session_state.favorite_animal = animal
        st.session_state.favorite_character = character
        st.session_state.setting = setting
        st.session_state.mood = mood
        st.session_state.story_length = length
        st.session_state.language = "English"
        st.session_state.selected_language = "English"

        story = generate_story(
            child_name=st.session_state.child_name,
            age=st.session_state.age,
            favorite_animal=st.session_state.favorite_animal,
            favorite_character=st.session_state.favorite_character,
            setting=st.session_state.setting,
            mood=st.session_state.mood,
            length=st.session_state.story_length,
            language=st.session_state.language
        )

        story = sanitize_story(story)
        st.session_state.story = story
        st.session_state.story_generated = True

        paragraphs = [
            paragraph.strip()
            for paragraph in story.split("\n")
            if paragraph.strip()
        ]

        story_html = ""

        for i, paragraph in enumerate(paragraphs):
            safe_paragraph = escape(paragraph)
            if i == 0:
                story_html += (
                    f'<p><span class="dropcap">'
                    f'{escape(child_name.strip()[0])}'
                    f'</span>{safe_paragraph}</p>'
                )
            else:
                story_html += f"<p>{safe_paragraph}</p>"

        st.session_state.story = story_html
        st.session_state.story_name = safe_name
        st.session_state.story_length = length

        time.sleep(0.5)
        st.rerun()


# =========================================================
# STORY PAGE
# =========================================================

else:

    story_name = st.session_state.get("story_name", "Tonight's Hero")

    st.markdown("""
    <div class="story-header">
        <div class="story-label">Tonight's Dream</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f'<div class="story-title">{story_name}\'s Magical Adventure</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="story-subtitle">A story made just for tonight</div>',
        unsafe_allow_html=True
    )

    st.write("")

    st.markdown(
        f"""
        <div class="storybook">
            <h2>🌙 The Adventure Begins</h2>
            {st.session_state.story}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">🎧 Listen to the story</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="small-text">Choose a voice for tonight\'s bedtime story.</div>',
        unsafe_allow_html=True
    )

    voice = st.selectbox(
        "Voice",
        [
            "🌙 Gentle storyteller",
            "🧚 Magical fairy",
            "🐻 Warm bedtime voice",
            "✨ Dreamy narrator"
        ],
        label_visibility="collapsed"
    )

    st.button("▶ Play Story")

    st.markdown(
        '<div class="footer">✨ Every night can be a new little dream.</div>',
        unsafe_allow_html=True
    )