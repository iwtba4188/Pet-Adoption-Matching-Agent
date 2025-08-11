import json
import os
import sys

import pandas as pd
from tqdm import tqdm


def vectorize_document(document: str) -> list[float]:
    """
    Vectorizes a given document using a pre-trained model.

    Args:
        document (str): The text document to vectorize.

    Returns:
        list[float]: A list of floats representing the vectorized document.
    """
    import os

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    result = client.models.embed_content(
        model="models/text-embedding-004",
        contents=document,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
    )

    return result.embeddings[0].values


def process_csv_vectorization(csv_path: str):
    """
    處理 CSV 文件的向量化

    Args:
        csv_path (str): CSV 文件路徑
    """
    print(f"讀取 CSV 文件: {csv_path}")

    # 讀取 CSV 文件
    df = pd.read_csv(csv_path)
    print(f"CSV 文件包含 {len(df)} 筆記錄")
    print(f"現有欄位: {df.columns.tolist()}")

    # 檢查是否已經有 vectorize 欄位
    if "vectorize" not in df.columns:
        print("新增 'vectorize' 欄位")
        df["vectorize"] = ""
    else:
        print("'vectorize' 欄位已存在")

    # 檢查哪些記錄需要向量化（vectorize 欄位為空的記錄）
    need_vectorize = df["vectorize"] == ""
    records_to_process = need_vectorize.sum()

    if records_to_process == 0:
        print("所有記錄都已經向量化完成")
        return

    print(f"需要向量化的記錄數: {records_to_process}")

    # 確保有 GEMINI_API_KEY
    if not os.environ.get("GEMINI_API_KEY"):
        print("錯誤: 請設置 GEMINI_API_KEY 環境變數")
        return

    # 處理需要向量化的記錄
    processed_count = 0

    for idx in tqdm(df[need_vectorize].index, desc="向量化進度"):
        try:
            content = df.loc[idx, "content"]
            if pd.isna(content) or content == "":
                print(f"跳過空內容記錄 {idx}")
                continue

            # 向量化文檔
            vector = vectorize_document(str(content))

            # 將向量轉換為 JSON 字符串存儲
            df.loc[idx, "vectorize"] = json.dumps(vector)

            processed_count += 1

            # 每處理 10 筆記錄就保存一次（避免意外丟失進度）
            if processed_count % 10 == 0:
                print(f"已處理 {processed_count} 筆記錄，保存中間結果...")
                df.to_csv(csv_path, index=False)

        except Exception as e:
            print(f"處理記錄 {idx} 時發生錯誤: {e}")
            continue

    # 最終保存
    print("保存最終結果...")
    df.to_csv(csv_path, index=False)
    print(f"向量化完成！共處理了 {processed_count} 筆記錄")

    # 驗證結果
    df_final = pd.read_csv(csv_path)
    vectorized_count = (df_final["vectorize"] != "").sum()
    print(f"最終統計: {vectorized_count}/{len(df_final)} 筆記錄已向量化")


if __name__ == "__main__":
    csv_file_path = (
        r"D:\GitHub\11320ISS507300_Assistant\src\static\article_contents.csv"
    )

    if not os.path.exists(csv_file_path):
        print(f"錯誤: 找不到文件 {csv_file_path}")
        sys.exit(1)

    process_csv_vectorization(csv_file_path)
