import base64
import re
from collections import Counter
from io import BytesIO

# import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

# import numpy as np
import torch
from ckip_transformers.nlp import CkipPosTagger, CkipWordSegmenter

# from matplotlib.figure import Figure
# from PIL import Image
# from scipy.ndimage import gaussian_gradient_magnitude
# from wordcloud import ImageColorGenerator, WordCloud
from wordcloud import WordCloud


def build_word_freq_dict(content: str | list[str]) -> dict:
    if isinstance(content, list):
        content = " ".join(content)

    # Text Cleaning
    content = re.sub(r"\s+", "", content)  # Remove multiple spaces & newlines
    content = re.sub(r"[^\w\s]", "", content)  # Remove punctuation

    # Tokenization with CKIP tagger
    device = 0 if torch.cuda.is_available() else -1
    print(f"Using device: {'CUDA' if device == 0 else 'CPU'}")

    # Initialize CKIP models with GPU acceleration if available
    ws = CkipWordSegmenter(model="bert-base", device=device)
    pos = CkipPosTagger(model="bert-base", device=device)

    # Process the text with CKIP
    ws_results = ws([content])  # No recommend_dictionary in newer versions
    pos_results = pos(ws_results)

    # Extract tokens and their POS tags
    tokens = ws_results[0]  # Get the tokens from the first (and only) sentence
    pos_tags = pos_results[0]  # Get the POS tags from the first sentence

    # Extract nouns, verbs, and adjectives
    desired_tags = {"Na", "Nb", "Nc", "VA", "VB", "VH", "VK", "VL"}
    filtered_tokens = [
        token
        for token, tag in zip(tokens, pos_tags, strict=False)
        if tag in desired_tags and len(token) >= 2
    ]

    # Remove Stopwords
    stopwords = set(
        """
    我們 你們 他們 這個 那個 一個 這些 那些
    沒有 因為 所以 但是 如果 然而 並且 至於 例如
    或者 無論 既然 由於 儘管 雖然 因此 其中 向 當 從 以來 以至 以上 以及 並非 然後
    而且 而已 或者 並未 既不 何況 不僅 而是 既然 既是 既不 不但 不過 不如 不僅 不僅僅
    既而 就算 除非 不然 否則 或許 縱然 縱使 假如 假設 假若 儘管 縱令 若是 即便 雖說
    雖然 只要 只有 盡管 即使 既是 就算 然而 儘管 可是 只是 但是 雖說 雖然 這樣 那樣
    這麼 那麼 例如 所以 但是 需要 可以 都是 一直 一些 就是 只能 一定 完全 是否 不是
    看到 非常 很多 之前 希望 需要 可能 知道 人 有
    """.split()
    )

    clean_tokens = [
        word for word in filtered_tokens if word.strip() and word not in stopwords
    ]

    # Count Frequency & Select Top 150 Words
    word_freq = Counter(clean_tokens)
    top_dict = dict(word_freq.most_common(150))
    print(top_dict)

    return top_dict


# def draw_wordcloud_cat(word_freq: dict) -> str:
#     # Load the cat image
#     cat_image_path = "./src/static/chatgpt_cat_2.png"
#     cat_image = np.array(Image.open(cat_image_path))

#     # Subsample the image for faster processing
#     cat_image = cat_image[::1, ::1]  # No subsampling to retain full resolution

#     # Scale up the cat image by 3x
#     cat_image = np.kron(cat_image, np.ones((3, 3, 1)))

#     # Create a mask from the cat image
#     cat_mask = cat_image.copy()
#     cat_mask[cat_mask.sum(axis=2) == 0] = 255

#     # Perform edge detection to enhance boundaries
#     edges = np.mean(
#         [gaussian_gradient_magnitude(cat_image[:, :, i] / 255.0, 2) for i in range(3)],
#         axis=0,
#     )
#     cat_mask[edges > 0.08] = 255

#     # Increase saturation for better color vibrancy
#     cat_image_hsv = mcolors.rgb_to_hsv(cat_image / 255.0)
#     cat_image_hsv[:, :, 1] = np.clip(
#         cat_image_hsv[:, :, 1] * 1.8, 0, 1
#     )  # Increase saturation
#     cat_image_hsv[:, :, 2] = np.clip(
#         cat_image_hsv[:, :, 2] * 1.5, 0, 1
#     )  # Slightly increase brightness
#     cat_image = (mcolors.hsv_to_rgb(cat_image_hsv) * 255).astype(np.uint8)

#     # Further enhance colors for deep blue and purple optimization
#     cat_image_hsv = mcolors.rgb_to_hsv(cat_image / 255.0)

#     # Increase saturation and brightness for deep blue and purple hues
#     # hue = cat_image_hsv[:, :, 0]
#     saturation = cat_image_hsv[:, :, 1]
#     value = cat_image_hsv[:, :, 2]

#     # Identify deep blue and purple hues (hue range for blue and purple)
#     # blue_purple_mask = (hue > 0.5) & (hue < 0.8)
#     # saturation[blue_purple_mask] = np.clip(saturation[blue_purple_mask] * 2, 0, 1)
#     # value[blue_purple_mask] = np.clip(value[blue_purple_mask] * 2, 0, 1)

#     # Apply the adjustments back
#     cat_image_hsv[:, :, 1] = saturation
#     cat_image_hsv[:, :, 2] = value
#     cat_image = (mcolors.hsv_to_rgb(cat_image_hsv) * 255).astype(np.uint8)

#     # Set non-cat areas to pure white
#     cat_image_hsv = mcolors.rgb_to_hsv(cat_image / 255.0)

#     # Identify non-cat areas (where the mask is white)
#     non_cat_mask = cat_mask.sum(axis=2) == 255 * 3

#     # Set saturation and brightness to maximum for non-cat areas
#     cat_image_hsv[non_cat_mask, 1] = 0  # No saturation (pure white)
#     cat_image_hsv[non_cat_mask, 2] = 1  # Full brightness (pure white)

#     # Convert back to RGB
#     cat_image = (mcolors.hsv_to_rgb(cat_image_hsv) * 255).astype(np.uint8)

#     # Adjust the WordCloud settings for a black background and optimized colors
#     wc = WordCloud(
#         font_path="./src/static/font/Noto_Sans_TC/static/NotoSansTC-Regular.ttf",
#         max_words=2000,
#         mask=cat_mask,
#         max_font_size=400,  # Increase max font size for higher resolution
#         random_state=42,
#         relative_scaling=0,
#         background_color="white",  # Set background to white
#         contour_width=1,
#         width=cat_image.shape[1] * 3,  # Increase width for higher resolution
#         height=cat_image.shape[0] * 3,  # Increase height for higher resolution
#     )

#     # Generate the word cloud from frequencies
#     wc.generate_from_frequencies(word_freq)

#     # Recolor the word cloud based on the optimized cat image
#     image_colors = ImageColorGenerator(cat_image)
#     wc.recolor(color_func=image_colors)

#     # After generating the word cloud, fill non-mask areas with white
#     output_image = np.array(wc.to_image())

#     # Identify non-mask areas (where the mask is white)
#     non_mask_areas = cat_mask.sum(axis=2) == 255 * 3

#     # Set non-mask areas to white in the output image
#     output_image[non_mask_areas] = [255, 255, 255]

#     # Display the word cloud
#     plt.figure(figsize=(16, 9))
#     plt.imshow(output_image, interpolation="bilinear")
#     plt.axis("off")

#     figfile = BytesIO()
#     plt.savefig(figfile, format="png")
#     figfile.seek(0)
#     figdata_png = base64.b64encode(figfile.getvalue())  # 将图片转为base64
#     figdata_str = str(figdata_png, "utf-8")  # 提取base64的字符串，不然是b'xxx'

#     # return f'<img src="data:image/png;base64,{figdata_str}"/>'
#     return f'<img src="data:image/png;base64,{figdata_str}"/>'


# def draw_wordcloud(word_freq: dict) -> Figure:
#     wordcloud = WordCloud(
#         font_path="./src/static/font/Noto_Sans_TC/static/NotoSansTC-Regular.ttf",
#         width=1600,
#         height=800,
#         background_color="white",
#         max_words=150,
#         scale=2,
#         max_font_size=400,
#         prefer_horizontal=0.7,
#         collocations=False,
#     ).generate_from_frequencies(word_freq)

#     plt.figure(figsize=(10, 5))
#     plt.imshow(wordcloud, interpolation="bilinear")
#     plt.axis("off")
#     plt.tight_layout(pad=0)

#     return plt.gcf()


def test_md_draw_wordcloud(word_freq: dict) -> str:
    wordcloud = WordCloud(
        font_path="./src/static/font/Noto_Sans_TC/static/NotoSansTC-Regular.ttf",
        width=1600,
        height=800,
        background_color="white",
        max_words=150,
        scale=2,
        max_font_size=400,
        prefer_horizontal=0.7,
        collocations=False,
    ).generate_from_frequencies(word_freq)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)

    figfile = BytesIO()
    plt.savefig(figfile, format="png")
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())  # 将图片转为base64
    figdata_str = str(figdata_png, "utf-8")  # 提取base64的字符串，不然是b'xxx'

    return f'<img class="wordcloud" src="data:image/png;base64,{figdata_str}"/>'
