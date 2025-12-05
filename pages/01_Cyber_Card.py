import streamlit as st
import streamlit.components.v1 as components
import json
import sys
import os

# 引用工具库
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_available_datasets, load_data

st.set_page_config(page_title="Cinema Mode", layout="wide", page_icon="🍿")

# --- 侧边栏配置 ---
datasets = get_available_datasets()
if not datasets:
    st.error("No scripts found.")
    st.stop()

default_idx = 0
if "en_cinema_master.json" in datasets:
    default_idx = datasets.index("en_cinema_master.json")

selected_file = st.sidebar.selectbox("Active Protocol (Dataset):", datasets, index=default_idx)
word_data = load_data(selected_file)
json_data = json.dumps(word_data)

# --- 前端核心代码 (防弹内核版) ---
html_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
    :root {{
        --neon-gold: #ffd700; --neon-blue: #00f3ff; --neon-red: #ff0055;
        --neon-green: #0aff0a; --bg-dark: #050505;
    }}
    * {{ box-sizing: border-box; -webkit-tap-highlight-color: transparent; }}
    body {{
        background-color: var(--bg-dark); color: #fff;
        font-family: 'Helvetica Neue', sans-serif;
        display: flex; flex-direction: column; align-items: center;
        height: 100vh; margin: 0; overflow: hidden;
    }}

    /* --- 启动遮罩 (解决手机无声的关键) --- */
    #start-overlay {{
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.95); z-index: 9999;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        cursor: pointer;
    }}
    .start-btn {{
        border: 2px solid var(--neon-green); color: var(--neon-green);
        padding: 15px 40px; font-size: 20px; border-radius: 50px;
        text-transform: uppercase; letter-spacing: 2px;
        animation: pulse 1.5s infinite;
    }}
    @keyframes pulse {{ 0% {{ box-shadow: 0 0 0 0 rgba(10, 255, 10, 0.4); }} 70% {{ box-shadow: 0 0 0 20px rgba(10, 255, 10, 0); }} 100% {{ box-shadow: 0 0 0 0 rgba(10, 255, 10, 0); }} }}

    /* --- 顶部控制 --- */
    .top-bar {{ width: 90vw; max-width: 360px; margin-top: 15px; display: flex; justify-content: space-between; align-items: center; z-index: 100; }}
    .protocol-switch {{ display: flex; align-items: center; gap: 8px; }}
    .status-badge {{ font-size: 10px; padding: 4px 8px; border: 1px solid #333; border-radius: 4px; color: #666; }}
    
    /* --- 3D 场景 --- */
    .scene {{ width: 85vw; max-width: 340px; aspect-ratio: 2/3; max-height: 55vh; margin-top: 15px; perspective: 1200px; position: relative; }}
    .card {{ width: 100%; height: 100%; position: relative; transition: transform 0.6s; transform-style: preserve-3d; border-radius: 16px; }}
    .card.is-flipped {{ transform: rotateY(180deg); }}
    .card__face {{ position: absolute; width: 100%; height: 100%; backface-visibility: hidden; border-radius: 16px; overflow: hidden; }}
    
    .card__face--front {{ background: #111; background-size: cover; background-position: center; }}
    .front-overlay {{ width: 100%; height: 100%; background: linear-gradient(to bottom, transparent 50%, rgba(0,0,0,0.9) 90%); display: flex; flex-direction: column; justify-content: flex-end; align-items: center; padding-bottom: 30px; }}
    .word-title {{ font-family: 'Impact', sans-serif; font-size: 42px; text-transform: uppercase; color: #fff; text-shadow: 0 0 15px var(--neon-blue); margin: 0; }}
    .phonetic-tag {{ background: rgba(255,255,255,0.15); padding: 4px 8px; border-radius: 4px; font-family: monospace; margin-top: 5px; font-size: 14px; backdrop-filter: blur(4px); }}
    
    .card__face--back {{ background: #1a1a1d; transform: rotateY(180deg); display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; border: 1px solid #333; text-align: center; }}
    .definition {{ font-size: 18px; font-weight: bold; color: var(--neon-gold); margin-bottom: 20px; max-height: 60%; overflow-y: auto; }}
    .sentence {{ font-size: 14px; color: #888; font-style: italic; border-top: 1px solid #333; padding-top: 15px; width: 100%; }}

    /* --- 底部输入 --- */
    .bottom-area {{ width: 90vw; max-width: 360px; margin-top: 20px; position: relative; }}
    input {{ width: 100%; background: #111; border: 1px solid #333; border-radius: 8px; color: #fff; font-size: 20px; text-align: center; padding: 12px; outline: none; font-family: monospace; transition: 0.3s; }}
    input:focus {{ border-color: var(--neon-blue); }}
    input.correct {{ border-color: var(--neon-green); color: var(--neon-green); }}
    input.wrong {{ border-color: var(--neon-red); animation: shake 0.4s; }}
    .fav-btn {{ position: absolute; top: 15px; right: 15px; font-size: 30px; color: rgba(255,255,255,0.2); z-index: 10; }}
    .fav-btn.active {{ color: var(--neon-red); text-shadow: 0 0 10px var(--neon-red); }}

    @keyframes shake {{ 0%, 100% {{transform: translateX(0);}} 25% {{transform: translateX(-5px);}} 75% {{transform: translateX(5px);}} }}
</style>
</head>
<body>

    <div id="start-overlay">
        <div class="start-btn">TAP TO START</div>
        <div style="margin-top:20px; font-size:12px; color:#666">ACTIVATE NEURAL LINK</div>
    </div>

    <div class="hud-bar">
        <div class="protocol-switch">
            <input type="checkbox" id="plan-toggle"> <span style="font-size:10px; color:#888">PROTOCOL</span>
        </div>
        <div id="day-indicator" class="status-badge">READY</div>
    </div>

    <div class="scene">
        <div class="fav-btn" id="fav-btn">♥</div>
        <div class="card" id="card">
            <div class="card__face card__face--front" id="front-bg">
                <div class="front-overlay">
                    <div class="word-title" id="display-word"></div>
                    <div class="phonetic-tag" id="display-phonetic"></div>
                </div>
            </div>
            <div class="card__face card__face--back">
                <div style="color:#444; font-size:9px; letter-spacing:2px; margin-bottom:10px">DEFINITION</div>
                <div class="definition" id="display-cn"></div>
                <div class="sentence" id="display-sentence"></div>
            </div>
        </div>
    </div>

    <div class="bottom-area">
        <input type="text" id="spelling-input" placeholder="TYPE HERE..." autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">
    </div>

<script>
    const allWords = {json_data};
    let state = {{
        activeQueue: allWords,
        currentIndex: 0,
        favorites: [],
        learnedIDs: [],
        lastLoginDate: ""
    }};
    
    let currentAudio = null;
    let isProcessing = false; // 关键锁
    let isFlipped = false;
    const synth = window.speechSynthesis;

    // DOM Refs
    const els = {{
        card: document.getElementById('card'),
        frontBg: document.getElementById('front-bg'),
        input: document.getElementById('spelling-input'),
        overlay: document.getElementById('start-overlay'),
        word: document.getElementById('display-word'),
        phonetic: document.getElementById('display-phonetic'),
        cn: document.getElementById('display-cn'),
        sent: document.getElementById('display-sentence'),
        favBtn: document.getElementById('fav-btn')
    }};

    // --- 1. 启动逻辑 ---
    els.overlay.addEventListener('click', () => {{
        // 手机端必须在点击事件中解锁音频
        // 播放一个空的音频对象，欺骗浏览器已经交互过了
        const silent = new Audio();
        silent.play().catch(() => {{}});
        
        els.overlay.style.display = 'none';
        init(); // 正式启动
    }});

    function init() {{
        try {{
            const saved = localStorage.getItem('cinema_data_v2');
            if (saved) state = {{ ...state, ...JSON.parse(saved) }};
        }} catch(e) {{}}
        renderCard();
    }}

    function saveState() {{
        localStorage.setItem('cinema_data_v2', JSON.stringify(state));
    }}

    // --- 2. 核心渲染 (防卡死设计) ---
    function renderCard() {{
        // 越界保护：如果队列空了或索引超了
        if (!state.activeQueue || state.activeQueue.length === 0) return;
        if (state.currentIndex >= state.activeQueue.length) state.currentIndex = 0;

        const data = state.activeQueue[state.currentIndex];
        
        // 填充数据
        els.word.textContent = data.word;
        els.phonetic.textContent = data.phonetic || "";
        els.cn.textContent = data.cn || "No definition.";
        els.sent.textContent = data.sentence || "";
        
        // 图片
        if (data.image) els.frontBg.style.backgroundImage = `url('${{data.image}}')`;
        else els.frontBg.style.backgroundColor = '#111';

        // 收藏
        if (state.favorites.includes(data.id)) els.favBtn.classList.add('active');
        else els.favBtn.classList.remove('active');

        // 重置状态
        els.card.classList.remove('is-flipped');
        isFlipped = false;
        els.input.value = '';
        els.input.className = '';
        els.input.disabled = false; // 确保输入框解锁
        els.input.focus();
        isProcessing = false; // 解锁逻辑

        // 自动发音 (带延时)
        setTimeout(() => playAudio(data, false), 500);
    }}

    // --- 3. 健壮的音频系统 (Robust Audio) ---
    function playAudio(data, isForcedChain, nextStepCallback) {{
        const audioUrl = data.audio;
        const text = data.word;

        // 定义播放完毕后的操作
        const onDone = () => {{
            if (nextStepCallback) nextStepCallback();
        }};

        // A. 尝试播放 MP3
        if (audioUrl && audioUrl.startsWith('http')) {{
            if (currentAudio) {{ currentAudio.pause(); currentAudio = null; }}
            currentAudio = new Audio(audioUrl);
            
            // 关键：如果出错，立刻降级到 TTS，不卡死
            currentAudio.onerror = () => {{
                console.log("MP3 error, switching to Robot");
                playRobot(text, onDone);
            }};
            
            // 关键：如果加载完毕，播放
            currentAudio.onended = onDone;
            
            currentAudio.play().catch(e => {{
                console.log("Autoplay blocked or network error", e);
                // 如果被浏览器拦截，尝试 TTS，或者直接跳过
                playRobot(text, onDone);
            }});
        }} else {{
            // B. 没有 MP3，使用机器音
            playRobot(text, onDone);
        }}
    }}

    function playRobot(text, callback) {{
        if (synth.speaking) synth.cancel();
        const u = new SpeechSynthesisUtterance(text);
        u.lang = 'en-US'; u.rate = 0.9;
        u.onend = callback;
        u.onerror = callback; // 即使出错也执行回调，防止卡死
        synth.speak(u);
    }}

    // --- 4. 输入交互 (Time-based Safety) ---
    els.input.addEventListener('input', (e) => {{
        if (isProcessing) return;
        const target = state.activeQueue[state.currentIndex].word.toLowerCase();
        const val = e.target.value.toLowerCase().trim();
        els.input.className = '';

        if (val === target) {{
            isProcessing = true;
            els.input.classList.add('correct');
            els.input.disabled = true; // 锁住输入框
            
            const currentData = state.activeQueue[state.currentIndex];

            // 🔊 强制发音逻辑 (带超时保护)
            // 设置一个 2.5秒 的安全定时器。万一音频回调失效，2.5秒后强制切卡
            const safetyTimer = setTimeout(() => {{
                nextCard();
            }}, 2500);

            // 尝试正常播放流程
            playAudio(currentData, true, () => {{
                // 如果音频正常播完，清除安全定时器，立即切换 (更顺滑)
                clearTimeout(safetyTimer);
                // 停顿一下再切
                setTimeout(nextCard, 300);
            }});

        }} else if (!target.startsWith(val)) {{
            els.input.classList.add('wrong');
        }}
    }});

    function nextCard() {{
        state.currentIndex++;
        renderCard();
    }}

    // --- 其他事件 ---
    els.card.addEventListener('click', () => {{
        isFlipped = !isFlipped;
        els.card.classList.toggle('is-flipped');
    }});
    
    els.favBtn.addEventListener('click', (e) => {{
        e.stopPropagation();
        const id = state.activeQueue[state.currentIndex].id;
        if (state.favorites.includes(id)) state.favorites = state.favorites.filter(x => x !== id);
        else state.favorites.push(id);
        saveState();
        renderCard();
    }});

</script>
</body>
</html>
"""

components.html(html_code, height=850, scrolling=False)