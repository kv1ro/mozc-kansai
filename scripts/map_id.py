import re
import sys
import os

input_file = "output.tsv" 
output_file = "kansai_final.tsv"

if not os.path.exists(input_file):
    input_file = "data/output.tsv"
    output_file = "data/kansai_final.tsv"

def get_id(placeholder):
    if "違" in placeholder or "おる" in placeholder or "せや" in placeholder:
        return "573" 
    elif "だめ" in placeholder or "本当" in placeholder:
        return "442"
    else:
        return "781"

with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

with open(output_file, "w", encoding="utf-8") as f:
    for line in lines:
        line = re.sub(r'\{\{([^_]+)_(left|right)_id\}\}', lambda m: get_id(m.group(1)), line)
        f.write(line)

print(f"{output_file} に数字化された綺麗なTSVを出力しました！")
