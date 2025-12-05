import streamlit as st
import streamlit.components.v1 as components
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_available_datasets, load_data

st.set_page_config(page_title="Cinema Mode", layout="wide", page_icon="🍿")

datasets = get_available_datasets()
if not datasets:
    st.error("No scripts found. Please run visual_converter.py first!")
    st.stop()

default_idx = 0
if "en_cinema_master.json" in datasets:
    default_idx = datasets.index("en_cinema_master.json")

selected_file = st.sidebar.selectbox("Active Protocol (Dataset):", datasets, index=default_idx)
word_data = load_data(selected_file)
json_data = json.dumps(word_data)

html_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
    :root {{ --neon-gold: #ffd700; --neon-blue: #00f3ff; --neon-red: #ff0055; --neon-green: #0aff0a; --bg-dark: #050505; }}
    * {{ box-sizing: border-box; -webkit-tap-highlight-color: transparent; }}
    body {{ background-color: var(--bg-dark); color: #fff; font-family: 'Helvetica Neue', sans-serif; display: flex; flex-direction: column; align-items: center; height: 100vh; margin: 0; overflow: hidden; }}
    
    .hud-bar {{ width: 90vw; max-width: 360px; margin-top: 15px; display: flex; justify-content: space-between; align-items: center; font-family: monospace; font-size: 11px; color: #666; z-index: 100; }}
    .status-badge {{ padding: 4px 8px; border-radius: 4px; background: #111; border: 1px solid #333; color: #888; }}
    .status-badge.active {{ border-color: var(--neon-green); color: var(--neon-green); }}
    .status-badge.alert {{ border-color: var(--neon-red); color: var(--neon-red); }}
    .protocol-switch {{ display: flex; align-items: center; gap: 8px; cursor: pointer; }}
    .switch-track {{ width: 30px; height: 16px; background: #333; border-radius: 10px; position: relative; transition: 0.3s; }}
    .switch-knob {{ width: 12px; height: 12px; background: #888; border-radius: 50%; position: absolute; top: 2px; left: 2px; transition: 0.3s; }}
    input:checked + .switch-track {{ background: var(--neon-blue); }}
    input:checked + .switch-track .switch-knob {{ transform: translateX(14px); background: #fff; }}
    input {{ display: none; }}

    .scene {{ width: 85vw; max-width: 340px; aspect-ratio: 2/3; max-height: 55vh; margin-top: 15px; position: relative; perspective: 1200px; }}
    .card {{ width: 100%; height: 100%; position: relative; transition: transform 0.6s cubic-bezier(0.2, 0.8, 0.2, 1); transform-style: preserve-3d; cursor: pointer; border-radius: 16px; box-shadow: 0 15px 40px rgba(0,0,0,0.6); }}
    .card.is-flipped {{ transform: rotateY(180deg); }}
    .card__face {{ position: absolute; width: 100%; height: 100%; backface-visibility: hidden; border-radius: 16px; overflow: hidden; -webkit-mask-image: -webkit-radial-gradient(white, black); }}
    .fav-btn {{ position: absolute; top: 15px; right: 15px; font-size: 28px; color: rgba(255,255,255,0.2); z-index: 10; cursor: pointer; }}
    .fav-btn.active {{ color: var(--neon-red); text-shadow: 0 0 10px var(--neon-red); }}
    .card__face--front {{ background-color: #151515; background-size: cover; background-position: center; }}
    .front-overlay {{ width: 100%; height: 100%; background: linear-gradient(to bottom, transparent 40%, rgba(0,0,0,0.8) 80%, #000 100%); display: flex; flex-direction: column; justify-content: flex-end; align-items: center; padding-bottom: 30px; }}
    .word-title {{ font-family: 'Impact', sans-serif; font-size: 40px; text-transform: uppercase; color: #fff; text-shadow: 0 0 15px var(--neon-blue); margin: 0; text-align: center; }}
    .phonetic-tag {{ background: rgba(255,255,255,0.1); color: #ddd; padding: 4px 10px; border-radius: 6px; font-family: monospace; margin-top: 8px; font-size: 12px; backdrop-filter: blur(4px); }}
    .card__face--back {{ background: #1a1a1d; transform: rotateY(180deg); display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 25px; border: 1px solid #333; text-align: center; }}
    .def-label {{ color: var(--neon-blue); font-size: 9px; letter-spacing: 2px; margin-bottom: 15px; }}
    .definition {{ font-size: 18px; font-weight: 600; color: var(--neon-gold); margin-bottom: 20px; max-height: 50%; overflow-y: auto; }}
    .sentence {{ font-style: italic; color: #888; font-size: 13px; border-top: 1px solid #333; padding-top: 15px; }}
    
    .bottom-area {{ width: 90vw; max-width: 360px; position: relative; margin-top: 20px; }}
    input[type=text] {{ display: block; width: 100%; background: #111; border: 1px solid #333; border-radius: 8px; color: #fff; font-size: 20px; text-align: center; padding: 12px; outline: none; font-family: 'Courier New', monospace; transition: 0.3s; }}
    input[type=text]:focus {{ border-color: var(--neon-blue); }}
    input[type=text].correct {{ border-color: var(--neon-green); color: var(--neon-green); background: rgba(10,255,10,0.05); }}
    input[type=text].wrong {{ border-color: var(--neon-red); animation: shake 0.4s; }}
    .mission-info {{ margin-top: 10px; font-size: 10px; color: #555; text-align: center; font-family: monospace; display: flex; justify-content: center; gap: 15px; }}
    .mission-info span.highlight {{ color: var(--neon-gold); }}
    @keyframes shake {{ 0%, 100% {{transform: translateX(0);}} 25% {{transform: translateX(-5px);}} 75% {{transform: translateX(5px);}} }}
    .loader {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: #444; font-size: 10px; }}
</style>
</head>
<body>
    <div class="hud-bar">
        <label class="protocol-switch">
            <input type="checkbox" id="plan-toggle">
            <div class="switch-track"><div class="switch-knob"></div></div>
            <span id="plan-label" style="font-size:10px;">THE PROTOCOL</span>
        </label>
        <div id="day-indicator" class="status-badge">FREE MODE</div>
    </div>
    <div class="scene">
        <div class="fav-btn" id="fav-btn">♥</div>
        <div class="card" id="card">
            <div class="card__face card__face--front" id="front-bg">
                <div class="loader">INITIALIZING...</div>
                <div class="front-overlay">
                    <div class="word-title" id="display-word"></div>
                    <div class="phonetic-tag" id="display-phonetic"></div>
                </div>
            </div>
            <div class="card__face card__face--back">
                <div class="def-label">DEFINITION</div>
                <div class="definition" id="display-cn"></div>
                <div class="sentence" id="display-sentence"></div>
            </div>
        </div>
    </div>
    <div class="bottom-area">
        <input type="text" id="spelling-input" placeholder="AWAITING INPUT..." autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">
        <div class="mission-info" id="mission-info"></div>
    </div>

<script>
    const allWords = {json_data};
    let state = {{
        isPlanActive: false,
        learnedIDs: [],
        favorites: [],
        todayReviewPool: [],
        todayNewPool: [],
        activeQueue: [],
        currentIndex: 0,
        dailyProgress: {{ review: 0, new: 0 }},
        lastLoginDate: ""
    }};

    let isFlipped = false;
    let isProcessing = false;
    // 用于播放真人语音的 Audio 对象
    let currentAudio = null;
    const synth = window.speechSynthesis;

    const DAILY_NEW_GOAL = 50;
    const DAILY_REVIEW_GOAL = 50;

    const els = {{
        card: document.getElementById('card'),
        frontBg: document.getElementById('front-bg'),
        input: document.getElementById('spelling-input'),
        favBtn: document.getElementById('fav-btn'),
        planToggle: document.getElementById('plan-toggle'),
        dayInd: document.getElementById('day-indicator'),
        missionInfo: document.getElementById('mission-info'),
        displayWord: document.getElementById('display-word'),
        displayPhonetic: document.getElementById('display-phonetic'),
        displayCn: document.getElementById('display-cn'),
        displaySent: document.getElementById('display-sentence'),
    }};

    function init() {{
        loadState();
        const todayStr = new Date().toDateString();
        if (state.lastLoginDate !== todayStr) resetDailyTasks(todayStr);
        if (state.isPlanActive) {{
            els.planToggle.checked = true;
            generateProtocolQueue();
        }} else {{
            state.activeQueue = allWords;
            updateUI("FREE MODE");
        }}
        renderCard();
    }}

    function loadState() {{
        try {{
            const saved = localStorage.getItem('cinema_protocol_state');
            if (saved) state = {{ ...state, ...JSON.parse(saved) }};
        }} catch(e) {{}}
    }}
    function saveState() {{ localStorage.setItem('cinema_protocol_state', JSON.stringify(state)); }}

    function resetDailyTasks(todayStr) {{
        state.lastLoginDate = todayStr;
        state.dailyProgress = {{ review: 0, new: 0 }};
        state.todayReviewPool = [];
        state.todayNewPool = [];
        saveState();
    }}

    function generateProtocolQueue() {{
        const today = new Date();
        const dayOfWeek = today.getDay();
        const isWeekend = (dayOfWeek === 0 || dayOfWeek === 6);

        if (isWeekend) {{
            updateUI("⚖️ JUDGMENT DAY");
            state.activeQueue = allWords.filter(w => state.learnedIDs.includes(w.id));
            if (state.activeQueue.length === 0) state.activeQueue = [allWords[0]];
            state.activeQueue.sort(() => Math.random() - 0.5);
        }} else {{
            const reviewTarget = Math.min(state.learnedIDs.length, DAILY_REVIEW_GOAL);
            const reviewRemaining = reviewTarget - state.dailyProgress.review;
            if (reviewRemaining > 0) {{
                updateUI("⚔️ PHASE 1: REVIEW");
                if (state.todayReviewPool.length === 0) {{
                    const learnedWords = allWords.filter(w => state.learnedIDs.includes(w.id));
                    state.todayReviewPool = learnedWords.sort(() => Math.random() - 0.5).slice(0, reviewTarget);
                }}
                state.activeQueue = state.todayReviewPool;
            }} else {{
                updateUI("🚀 PHASE 2: NEW WORDS");
                if (state.todayNewPool.length === 0) {{
                    const unlearned = allWords.filter(w => !state.learnedIDs.includes(w.id));
                    state.todayNewPool = unlearned.slice(0, DAILY_NEW_GOAL);
                }}
                state.activeQueue = state.todayNewPool;
            }}
        }}
        state.currentIndex = 0;
    }}

    function updateUI(modeText) {{
        els.dayInd.textContent = modeText;
        if (modeText.includes("JUDGMENT")) els.dayInd.className = "status-badge alert";
        else if (modeText.includes("PHASE")) els.dayInd.className = "status-badge active";
        else els.dayInd.className = "status-badge";
        if (state.isPlanActive) {{
            els.missionInfo.innerHTML = `<span>REV: <span class="highlight">${{state.dailyProgress.review}}/${{DAILY_REVIEW_GOAL}}</span></span> <span>NEW: <span class="highlight">${{state.dailyProgress.new}}/${{DAILY_NEW_GOAL}}</span></span>`;
        }} else {{
            els.missionInfo.innerHTML = `<span>FREE ROAM MODE</span>`;
        }}
    }}

    function preloadNextImage() {{
        const nextIdx = (state.currentIndex + 1) % state.activeQueue.length;
        const nextData = state.activeQueue[nextIdx];
        if (nextData && nextData.image) {{ const img = new Image(); img.src = nextData.image; }}
    }}

    function renderCard() {{
        if (!state.activeQueue || state.activeQueue.length === 0) return;
        if (state.currentIndex >= state.activeQueue.length) {{
             if(state.isPlanActive) {{ generateProtocolQueue(); if (state.currentIndex >= state.activeQueue.length) state.currentIndex = 0; }} 
             else {{ state.currentIndex = 0; }}
        }}
        const data = state.activeQueue[state.currentIndex];
        
        els.displayWord.textContent = data.word;
        els.displayPhonetic.textContent = data.phonetic || "";
        els.displayCn.textContent = data.cn || "Processing...";
        els.displaySent.textContent = data.sentence || "";
        
        els.frontBg.style.backgroundImage = data.image ? `url('${{data.image}}')` : 'none';
        els.frontBg.style.backgroundColor = data.image ? 'transparent' : '#111';

        if (state.favorites.includes(data.id)) els.favBtn.classList.add('active');
        else els.favBtn.classList.remove('active');

        els.card.classList.remove('is-flipped');
        isFlipped = false;
        els.input.value = '';
        els.input.className = '';
        els.input.disabled = false;
        els.input.focus();
        isProcessing = false;
        
        setTimeout(() => speak(null), 500);
    }}

    function markAsMastered(wordId) {{
        if (!state.learnedIDs.includes(wordId)) state.learnedIDs.push(wordId);
        if (state.isPlanActive) {{
            const today = new Date(); const dayOfWeek = today.getDay();
            if (dayOfWeek !== 0 && dayOfWeek !== 6) {{
                const isReviewing = state.todayReviewPool.some(w => w.id === wordId);
                const isLearning = state.todayNewPool.some(w => w.id === wordId);
                if (isReviewing && state.dailyProgress.review < DAILY_REVIEW_GOAL) state.dailyProgress.review++;
                else if (isLearning && state.dailyProgress.new < DAILY_NEW_GOAL) state.dailyProgress.new++;
            }}
        }}
        saveState();
        if (state.isPlanActive) updateUI(els.dayInd.textContent);
    }}

    // --- 🔊 核心：双模态发音引擎 (Dual-Mode Audio Engine) ---
    function speak(onEndCallback) {{
        const data = state.activeQueue[state.currentIndex];
        const text = data.word;
        const audioUrl = data.audio; // 获取 MP3 链接

        // 1. 优先尝试真人 MP3
        if (audioUrl && audioUrl.startsWith('http')) {{
            if (currentAudio) {{ currentAudio.pause(); currentAudio = null; }}
            currentAudio = new Audio(audioUrl);
            if (onEndCallback) {{
                currentAudio.onended = onEndCallback;
            }}
            currentAudio.play().catch(e => {{
                console.log("MP3 Play failed, falling back to Robot.", e);
                speakRobot(text, onEndCallback); // 失败则降级
            }});
        }} else {{
            // 2. 降级为机械音
            speakRobot(text, onEndCallback);
        }}
    }}

    function speakRobot(text, onEndCallback) {{
        if (synth.speaking) synth.cancel();
        const u = new SpeechSynthesisUtterance(text);
        u.lang = 'en-US'; u.rate = 0.9;
        if(onEndCallback) u.onend = onEndCallback;
        synth.speak(u);
    }}

    els.input.addEventListener('input', (e) => {{
        if (isProcessing) return;
        const target = state.activeQueue[state.currentIndex].word.toLowerCase();
        const val = e.target.value.toLowerCase().trim();
        els.input.className = '';

        if (val === target) {{
            isProcessing = true;
            els.input.classList.add('correct');
            els.input.disabled = true;
            preloadNextImage();
            markAsMastered(state.activeQueue[state.currentIndex].id);

            // 强制发音两遍
            speak(() => {{
                setTimeout(() => {{
                    speak(() => {{
                        state.currentIndex++;
                        renderCard();
                    }});
                }}, 300);
            }});
        }} else if (!target.startsWith(val)) {{
            els.input.classList.add('wrong');
        }}
    }});

    els.planToggle.addEventListener('change', (e) => {{
        state.isPlanActive = e.target.checked;
        saveState();
        state.currentIndex = 0;
        if (state.isPlanActive) generateProtocolQueue();
        else {{ state.activeQueue = allWords; updateUI("FREE MODE"); }}
        renderCard();
    }});

    els.card.addEventListener('click', () => {{
        isFlipped = !isFlipped;
        els.card.classList.toggle('is-flipped');
    }});

    els.favBtn.addEventListener('click', (e) => {{
        e.stopPropagation();
        const id = state.activeQueue[state.currentIndex].id;
        if(state.favorites.includes(id)) state.favorites = state.favorites.filter(x => x !== id);
        else state.favorites.push(id);
        saveState();
        renderCard();
    }});

    // 手机软键盘回车支持
    els.input.addEventListener('keyup', (e) => {{
        if (e.key === 'Enter') speak(null);
    }});
    
    document.addEventListener('keydown', (e) => {{
        if (isProcessing) return;
        if (e.key === 'Tab') {{ e.preventDefault(); state.currentIndex++; renderCard(); }}
        if (e.key === ' ' && document.activeElement !== els.input) {{ e.preventDefault(); els.card.click(); }}
    }});

    init();
</script>
</body>
</html>
"""
components.html(html_code, height=850, scrolling=False)