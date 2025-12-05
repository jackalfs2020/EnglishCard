import json
import urllib.parse
import random
import os

# --- 🏭 工厂配置 ---
SOURCE_FOLDER = "raw_source"
OUTPUT_FILE = "data/en_cinema_master.json"
WORDS_PER_FILE_LIMIT = 400 

# --- 🎬 AI 导演配置 ---
MOVIE_PREFIXES = ["The", "Mission:", "Project:", "Operation:", "Chronicles of", "Legacy of", "Dark", "Silent", "Protocol:"]
MOVIE_SUFFIXES = ["Identity", "Ultimatum", "Redemption", "Legacy", "Inception", "Saga", "Files", "Paradox", "Rising"]
CINEMA_PROMPT = "cinematic movie shot from a hollywood blockbuster, IMAX quality, dramatic lighting, highly detailed, 8k, realistic, masterpiece, scene depicting: "

def generate_fake_movie_title(word):
    style = random.choice(["prefix", "suffix", "simple"])
    if style == "prefix": return f"{random.choice(MOVIE_PREFIXES)} {word.capitalize()}"
    elif style == "suffix": return f"{word.capitalize()} {random.choice(MOVIE_SUFFIXES)}"
    else: return f"{word.capitalize()}: The Movie"

def process_batch():
    if not os.path.exists("data"): os.makedirs("data")
    if not os.path.exists(SOURCE_FOLDER):
        print(f"❌ 错误：找不到 '{SOURCE_FOLDER}' 文件夹！")
        return

    final_master_list = []
    global_id_counter = 1
    
    files = [f for f in os.listdir(SOURCE_FOLDER) if f.endswith(".json")]
    files.sort()
    
    print(f"📂 发现 {len(files)} 个剧本文件，AI 导演组准备开机...")

    for filename in files:
        file_path = os.path.join(SOURCE_FOLDER, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
        except Exception as e:
            continue

        if isinstance(raw_data, dict):
            temp_list = []
            for w, d in raw_data.items():
                temp_list.append({"word": w, "definition": d})
            raw_data = temp_list

        current_batch = raw_data[:WORDS_PER_FILE_LIMIT]

        for item in current_batch:
            word = item.get("word") or item.get("headword") or "Unknown"
            if word == "Unknown": continue

            # --- 🔍 1. 深度挖掘真人发音 (核心修复) ---
            audio_url = ""
            phonetic_text = item.get("phonetic", "")
            
            # 遍历 phonetics 数组寻找音频
            if "phonetics" in item and isinstance(item["phonetics"], list):
                for p in item["phonetics"]:
                    # 优先找有 audio 且不为空的
                    if "audio" in p and p["audio"]:
                        audio_url = p["audio"]
                    # 顺便找音标
                    if "text" in p and not phonetic_text:
                        phonetic_text = p["text"]
                    
                    # 如果找到了音频，就不找了，直接跳出
                    if audio_url: break
            
            if not phonetic_text: phonetic_text = "/.../"

            # --- 2. 挖掘含义 ---
            definition = "No definition found."
            sentence = f"The word '{word}' implies a complex meaning."
            
            if "meanings" in item and isinstance(item["meanings"], list):
                try:
                    def_obj = item["meanings"][0].get("definitions", [])[0]
                    definition = def_obj.get("definition", definition)
                    if "example" in def_obj: sentence = def_obj["example"]
                except: pass
            elif "definition" in item:
                 definition = item["definition"]
            
            # --- 3. 生成视觉 ---
            short_def = definition[:80]
            prompt = f"{CINEMA_PROMPT} {word}, visual representation of {short_def}"
            encoded_prompt = urllib.parse.quote(prompt)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=720&height=1080&nologo=true&seed={word}_{global_id_counter}"

            new_obj = {
                "id": global_id_counter,
                "word": word,
                "phonetic": phonetic_text,
                "audio": audio_url, # ✅ 新增：MP3链接
                "cn": definition,
                "sentence": sentence,
                "emoji": "🎬",
                "image": image_url,
                "origin": f"Film: {generate_fake_movie_title(word)}"
            }
            
            final_master_list.append(new_obj)
            global_id_counter += 1

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_master_list, f, ensure_ascii=False, indent=2)

    print(f"✅ 杀青！已修复音频数据。数据已保存至: {OUTPUT_FILE}")

if __name__ == "__main__":
    process_batch()