import sys
import os
from google import genai

def main():
    # Initialize the client. It automatically picks up the GEMINI_API_KEY environment variable.
    try:
        client = genai.Client()
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")
        print("Make sure the GEMINI_API_KEY environment variable is set.")
        sys.exit(1)

    prompt = "PCやスマホのタイピングで変換事故が起きやすい関西弁の単語トップ50（動詞、形容詞、助動詞など）を出力してください。結果はヘッダーなしのTSV形式（関西弁\t標準語）の文字列のみで返してください。"

    print("Generating top 50 Kansai dialect words prone to typing conversion errors...")
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        sys.exit(1)

    output_file = "word_pairs.tsv"
    try:
        # Clean up the response text in case the model wraps it in markdown code blocks
        text = response.text.strip()
        if text.startswith("```tsv"):
            text = text[6:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print(f"Successfully saved to {output_file}")
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")

if __name__ == "__main__":
    main()
