# Kansai Mozc Generator
さき言っとくと微妙です。

Gemini APIを活用して、関西弁の自然な活用形を網羅したMozc（Google日本語入力）用の辞書データを自動生成・追加するツール群です。
標準のIMEでは誤変換されがちな「ちゃうかったら」「いかへんかったら」などの複雑な関西弁フレーズを、ストレスなく一発変換できるようにします。

## 特徴
- **Gemini APIによる自動展開**: 少数のシード単語（例：ちゃう、あかん）から、考えうる限りの活用形（過去形、否定形、仮定形など）をAIが自動で生成します。
- **Mozcユーザー辞書完全対応**: 面倒なC++のソースビルド（依存関係の沼）を回避し、GUIから10秒でインポートできる形式を出力します。

## 必須環境
- Python 3.10+
- Gemini API Key (Google AI Studioで無料取得可能)
- Mozc (Fcitx5, IBus, 拡張機能など)

## 使い方

### 1. 環境設定
リポジトリをクローンし、必要なライブラリをインストールします。

```bash
git clone [https://github.com/yourusername/kansai_ime.git](https://github.com/yourusername/kansai_ime.git)
cd kansai_ime
python -m venv venv
source venv/bin/activate.fish
pip install google-generativeai python-dotenv
```

`.env` ファイルを作成し、Gemini APIキーを設定します。

```env
GEMINI_API_KEY=your_api_key_here
```

### 2. 辞書データの生成
以下のスクリプトを順番に実行し、ベースとなるデータを作成します。

```bash
# シード単語の作成
python scripts/make_seed.py

# Gemini APIを利用した活用形の自動生成（数分かかります）
python scripts/generate_tsv.py
```

### 3. ユーザー辞書フォーマットへの変換
生成されたTSVファイルを、Mozcのユーザー辞書ツールで読み込める形式（短縮よみ）に変換します。

```bash
awk -F'\t' '{print $1 "\t" $5 "\t短縮よみ"}' data/kansai_final.tsv > data/user_dict.txt
```

### 4. Mozcへのインポート
1. Fcitx5などの設定画面から「Mozc 辞書ツール」を開く。
2. `管理` -> `新規辞書のインポート` を選択。
3. ファイルに作成した `data/user_dict.txt` を指定。
4. 辞書名（例：関西弁辞書）を付け、フォーマット「自動判定」でインポート。

## 注意事項・Tips
* **学習のコツ**: インポート直後は文節の区切りでおかしくなることがあります。最初は単語ごとに区切って（例：「ちゃうかったら」でエンター）確定させると、Mozcが強力に学習して長文でも一発変換できるようになります。
* **システム辞書への組み込みについて**: `map_id.py` を使ってMozcのシステム辞書に直接インジェクションすることも可能ですが、Arch Linux等での古い依存関係（Python2, GTK2等）のビルド沼にハマるため、現在のユーザー辞書アプローチを推奨しています。
