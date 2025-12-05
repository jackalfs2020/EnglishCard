import json
import urllib.parse
import random
import os

# --- 🏭 工厂配置 ---
SOURCE_FOLDER = "raw_source"
OUTPUT_FILE = "data/en_cinema_master.json"

# ✅ 按照你的计划：26个文件 * 150词 = 3900词 (约等于2个月的量)
WORDS_PER_FILE_LIMIT = 150 

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

        # 截取前 150 个
        current_batch = raw_data[:WORDS_PER_FILE_LIMIT]

        for item in current_batch:
            word = item.get("word") or item.get("headword") or "Unknown"
            if word == "Unknown": continue

            # --- 🔍 核心修复：挖掘真人 MP3 ---
            audio_url = ""
            phonetic_text = item.get("phonetic", "")
            
            if "phonetics" in item and isinstance(item["phonetics"], list):
                for p in item["phonetics"]:
                    if "audio" in p and p["audio"]:
                        audio_url = p["audio"]
                    if "text" in p and not phonetic_text:
                        phonetic_text = p["text"]
                    if audio_url: break # 找到一个就够了
            
            if not phonetic_text: phonetic_text = "/.../"

            # --- 挖掘含义 ---
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
            
            # --- 生成视觉 ---
            short_def = definition[:80]
            prompt = f"{CINEMA_PROMPT} {word}, visual representation of {short_def}"
            encoded_prompt = urllib.parse.quote(prompt)
            # 加入 id 确保图片稳定
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=720&height=1080&nologo=true&seed={word}_{global_id_counter}"

            new_obj = {
                "id": global_id_counter,
                "word": word,
                "phonetic": phonetic_text,
                "audio": audio_url, # ✅ 确保这一行存在！
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

    print(f"✅ 杀青！已生成 {len(final_master_list)} 个单词（含真人发音）。")
    print(f"💾 数据已保存至: {OUTPUT_FILE}")

if __name__ == "__main__":
    process_batch()