import sys
import json
import os
import time
from google import genai
from google.genai import types

def main():
    input_file = "word_pairs.tsv"
    output_file = "output.tsv"

    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Please run make_seed.py first.")
        sys.exit(1)

    # Initialize the client. It automatically picks up the GEMINI_API_KEY environment variable.
    try:
        client = genai.Client()
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")
        print("Make sure the GEMINI_API_KEY environment variable is set.")
        sys.exit(1)

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {input_file}: {e}")
        sys.exit(1)

    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        parts = line.split("\t")
        if len(parts) != 2:
            print(f"Skipping invalid line: {line}")
            continue
            
        kansai_word = parts[0].strip()
        standard_word = parts[1].strip()

        prompt = f"""
以下の関西弁の単語とその標準語の同義語を元に、関西弁の様々な活用形（終止形、未然形、連用形など考えうる限りすべて）を生成し、それぞれに対応する標準語の活用形とペアにしてください。
結果は以下の構造のJSONフォーマットの配列で返してください。

関西弁: {kansai_word}
標準語: {standard_word}

JSONの構造例:
[
  {{"kansai": "ちゃう", "hyojungo": "違う"}},
  {{"kansai": "ちゃうかった", "hyojungo": "違った"}}
]
"""

        print(f"Generating conjugations for {kansai_word} ({standard_word})...")
        
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                ),
            )
        except Exception as e:
            print(f"Error calling Gemini API for {kansai_word}: {e}")
            print("Sleeping for 3 seconds before continuing...")
            time.sleep(3)
            continue

        try:
            data = json.loads(response.text)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response for {kansai_word}: {e}")
            print("Raw response:")
            print(response.text)
            print("Sleeping for 3 seconds before continuing...")
            time.sleep(3)
            continue

        output_lines = []
        for item in data:
            kansai = item.get("kansai", "")
            hyojungo = item.get("hyojungo", "")
            
            if not kansai or not hyojungo:
                continue
                
            # Column 1: Yomi (Kansai)
            # Column 2: Left context ID placeholder
            # Column 3: Right context ID placeholder
            # Column 4: Cost (3000)
            # Column 5: Hyouki (Kansai)
            left_id = f"{{{{{hyojungo}_left_id}}}}"
            right_id = f"{{{{{hyojungo}_right_id}}}}"
            cost = "3000"
            
            tsv_line = f"{kansai}\t{left_id}\t{right_id}\t{cost}\t{kansai}"
            output_lines.append(tsv_line)

        if output_lines:
            tsv_output = "\n".join(output_lines)
            
            # Append to output.tsv
            try:
                with open(output_file, "a", encoding="utf-8") as f:
                    f.write(tsv_output + "\n")
                print(f"Successfully appended {len(output_lines)} entries to {output_file}")
            except Exception as e:
                print(f"Error writing to {output_file}: {e}")

        print("Sleeping for 3 seconds to avoid API rate limits...\n")
        time.sleep(3)

if __name__ == "__main__":
    main()
