import time
from unittest.mock import PropertyMock

import pandas as pd
import pytest
import streamlit as st
from pytest_mock import MockFixture
from streamlit.testing.v1 import AppTest

from utils.i18n import I18n

i18n = I18n(lang="en")


@pytest.mark.parametrize(
    "init_lang",
    ["en", "en-US", "zh-TW", "zh-CN", "zh-HK"],
)
@pytest.mark.parametrize(
    "page_path",
    [
        # "pets_gemini",
        # "pets_autogen",
        "word2vec-2d",
        "word2vec-3d",
        "word2vec-skip-gram",
        "word2vec-cbow",
    ],
)
def test_page_diff_langs(mocker: MockFixture, page_path: str, init_lang: str) -> None:
    # patch the property on the class
    mocker.patch.object(
        type(st.context), "locale", new_callable=PropertyMock, return_value=init_lang
    )

    at = AppTest.from_file("../src/streamlit_app.py", default_timeout=30).run()
    at.switch_page(f"./pages/{page_path}.py").run()

    time.sleep(5)

    print(at.title[0].value)
    print(at.selectbox)

    assert not at.exception


@pytest.mark.parametrize(
    "select_lang",
    ["browser_default", "en", "zh-TW", "zh-CN"],
)
def test_lang_selection(mocker: MockFixture, select_lang: str) -> None:
    i18n.set_lang(select_lang)

    # patch the property on the class
    mocker.patch.object(
        type(st.context), "locale", new_callable=PropertyMock, return_value="en"
    )

    at = AppTest.from_file("../src/streamlit_app.py", default_timeout=30).run()
    at.switch_page("./pages/pets_gemini.py").run()

    time.sleep(5)

    # print(f"Before: {at.chat_input[0].placeholder=}")
    at.selectbox(key="selected_lang").select(select_lang).run()
    # print(f"After: {at.chat_input[0].placeholder=}")
    # print(f"Ans: {i18n('pets.chat.input_placeholder')=}")

    assert at.chat_input[0].placeholder == i18n("pets.chat.input_placeholder")


# XXX: it's not possible to test the data_editor
#      in the current version of streamlit (1.44.0)
#      The alternative is to use the `st.dataframe` method
@pytest.mark.parametrize(
    "page_path",
    [
        "word2vec-2d",
        "word2vec-3d",
        "word2vec-cbow",
        "word2vec-skip-gram",
    ],
)
def test_week10_empty(mocker: MockFixture, page_path: str) -> None:
    i18n.set_lang("en")

    mocker.patch.object(
        type(st.context), "locale", new_callable=PropertyMock, return_value="en"
    )

    at = AppTest.from_file("../src/streamlit_app.py", default_timeout=30).run()
    at.switch_page(f"./pages/{page_path}.py").run()

    time.sleep(5)

    assert at.warning[0].value == i18n("week10.no_sentences")

    assert not at.exception


@pytest.mark.parametrize(
    "page_path",
    [
        "word2vec-2d",
        "word2vec-3d",
    ],
)
def test_week10_2d_3d_not_empty_has_selection(
    mocker: MockFixture, page_path: str
) -> None:
    mocker.patch.object(
        type(st.context), "locale", new_callable=PropertyMock, return_value="en"
    )

    sample_df = pd.DataFrame(
        [
            {"selected": True, "sentence": "Sample sentence is a sentence"},
            {"selected": True, "sentence": "Another sentence"},
        ],
        columns=["selected", "sentence"],
    )

    mocker.patch("utils.week10.df_input", return_value=sample_df)

    at = AppTest.from_file("../src/streamlit_app.py", default_timeout=30).run()
    at.switch_page(f"./pages/{page_path}.py").run()

    time.sleep(5)

    assert len(at.warning) == 0

    assert not at.exception


@pytest.mark.parametrize(
    "page_path",
    [
        "word2vec-cbow",
        "word2vec-skip-gram",
    ],
)
def test_week10_similarity_not_empty(mocker: MockFixture, page_path: str) -> None:
    mocker.patch.object(
        type(st.context), "locale", new_callable=PropertyMock, return_value="en"
    )

    sample_df = pd.DataFrame(
        [
            {"selected": True, "sentence": "Sample sentence is a sentence"},
            {"selected": True, "sentence": "Another sentence"},
        ],
        columns=["selected", "sentence"],
    )

    mocker.patch("utils.week10.df_input", return_value=sample_df)

    at = AppTest.from_file("../src/streamlit_app.py", default_timeout=30).run()
    at.switch_page(f"./pages/{page_path}.py").run()

    time.sleep(5)

    # check if the selectbox exists
    try:
        at.selectbox(key="select_similar_word")
    except KeyError as e:  # pragma: no cover
        raise AssertionError("select_similar_word not found") from e

    selectbox_similar_word = at.selectbox(key="select_similar_word")

    # check if the selectbox has the correct options
    select_similar_word_options = selectbox_similar_word.options
    expected_options = [
        word.lower()
        for sentence in sample_df["sentence"].tolist()
        for word in sentence.split()
        if len(word) > 1
    ]
    expected_options = list(set(expected_options))

    assert sorted(select_similar_word_options) == sorted(expected_options)

    # check selection of each option
    for word in expected_options:
        selectbox_similar_word.set_value(word).run()

        # if in stopword, only one dataframe should be shown
        if word in ["is"]:
            assert len(at.dataframe) == 1
        else:
            assert len(at.dataframe) == 2

    assert not at.exception


@pytest.mark.parametrize(
    "page_path",
    [
        "word2vec-2d",
        "word2vec-3d",
        "word2vec-cbow",
        "word2vec-skip-gram",
    ],
)
def test_week10_not_empty_no_selection(mocker: MockFixture, page_path: str) -> None:
    mocker.patch.object(
        type(st.context), "locale", new_callable=PropertyMock, return_value="en"
    )

    sample_df = pd.DataFrame(
        [
            {"selected": False, "sentence": "Sample sentence is a sentence"},
            {"selected": False, "sentence": "Another sentence"},
        ],
        columns=["selected", "sentence"],
    )

    mocker.patch("utils.week10.df_input", return_value=sample_df)

    at = AppTest.from_file("../src/streamlit_app.py", default_timeout=30).run()
    at.switch_page(f"./pages/{page_path}.py").run()

    time.sleep(5)

    assert at.warning[0].value == i18n("week10.no_sentences")

    assert not at.exception
