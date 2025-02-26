import streamlit as st
import json

# カスタムCSSでメインコンテンツの幅を調整
def set_main_content_width():
    st.markdown(
        """
        <style>
        /* 全体のページ幅を調整 */
        [data-testid="stAppViewContainer"] {
            max-width: 100%;
            padding: 0;
        }
        /* メインコンテンツを中央に寄せる */
        [data-testid="stVerticalBlock"] {
            align-items: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# カスタムCSSでサイドバーの横幅を調整
def set_sidebar_width(width: int):
    st.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] {{
            min-width: {width}px;
            max-width: {width}px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# JSONデータの読み込み
@st.cache_data
def load_data(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

# サイドバーの横幅を設定
set_sidebar_width(400)  # ここでサイドバーの横幅を指定（ピクセル単位）
# メインコンテンツ幅を設定
set_main_content_width()

# JSONファイルのパス
data = []
for n in range(10):
    data += load_data(f"outputs/{2024-n}.json")

# アプリのタイトル
st.title("議事録ビューア")

# サイドバーに会議番号を選択するUI
meeting_ids = [meeting["meeting_id"] for meeting in data]
selected_meeting = st.sidebar.selectbox("会議番号を選択", meeting_ids)

# 選択された会議のデータを取得
meeting_data = next((meeting for meeting in data if meeting["meeting_id"] == selected_meeting), None)

# 会議データを表示
if meeting_data:
    # 会議番号のヘッダー表示
    st.header(f"会議番号: {meeting_data['meeting_id']}")

    # カテゴリ選択
    categories = [category["category"] for category in meeting_data["categories"]]
    selected_category = st.sidebar.selectbox("カテゴリを選択", categories)

    # 選択されたカテゴリのデータを取得
    category_data = next((cat for cat in meeting_data["categories"] if cat["category"] == selected_category), None)

    if category_data:
        st.subheader(f"カテゴリ: {category_data['category']}")

        # クラスタ選択
        cluster_keywords = [cluster["cluster_keywords"] for cluster in category_data["clusters"]]
        selected_cluster_keywords = st.sidebar.selectbox("キーワードを選択", cluster_keywords)

        # 選択されたクラスタのデータを取得
        selected_cluster = next(
            (
                cluster
                for cluster in category_data["clusters"]
                if cluster["cluster_keywords"] == selected_cluster_keywords
            ),
            None,
        )

        if selected_cluster:
            # 選択されたクラスタの情報を表示
            st.markdown(f"### キーワード: {selected_cluster_keywords}")
            for item in selected_cluster["items"]:
                emp = ''
                for n in range(44-len(item['head'])):
                    emp += '　'
                with st.expander(f"{item['head']}{emp}"):
                    st.write(f"{item['body']}")
                
        else:
            st.error("選択されたクラスタが見つかりません。")
else:
    st.error("データが見つかりませんでした。")
