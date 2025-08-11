import os
import time
from unittest.mock import PropertyMock

import pytest
import streamlit as st
from pytest_mock import MockFixture
from streamlit.testing.v1 import AppTest


def test_chat(mocker: MockFixture) -> None:
    # Avoid 429 Too Many Requests error
    time.sleep(60)

    # patch the property on the class
    mocker.patch.object(
        type(st.context), "locale", new_callable=PropertyMock, return_value="en"
    )

    at = AppTest.from_file("../src/streamlit_app.py", default_timeout=120).run()
    at.switch_page("./pages/pets_gemini.py").run()
    at.secrets["gemini_api_key"] = os.getenv("GEMINI_API_KEY")

    time.sleep(10)

    # check simple chat
    prompt = "你好，我想領養一隻貓，幫我查詢目前等待領養的貓咪資訊（非常簡短的），我住公寓，家裡只有我，我會長時間在家，極度簡短的回答。"
    at.chat_input(key="chat_bot").set_value(prompt).run()

    assert len(at.chat_message) >= 2
    assert at.chat_message[1].children[0].value == prompt

    # check history print
    prompt = "沒問題，我會參考你給的結果，謝謝你"
    at.chat_input(key="chat_bot").set_value(prompt).run()
    assert len(at.chat_message) >= 4
    assert at.chat_message[3].children[0].value == prompt

    assert not at.exception


@pytest.mark.timeout(180 + 60)
def test_chat_autogen(mocker: MockFixture) -> None:
    # Avoid 429 Too Many Requests error
    time.sleep(60)

    # patch the property on the class
    mocker.patch.object(
        type(st.context), "locale", new_callable=PropertyMock, return_value="en"
    )

    at = AppTest.from_file("../src/streamlit_app.py", default_timeout=120).run()
    at.switch_page("./pages/pets_autogen.py").run()
    at.secrets["gemini_api_key"] = os.getenv("GEMINI_API_KEY")

    time.sleep(10)

    # check simple chat
    prompt = "請極度精簡回答。調用 agent tool 時，task 內容加入「請極度精簡回答」。我想領養一隻貓，請幫我找 dcard 上面的領養文章，匹配並整理該貓咪的資訊。我住在公寓，家裡只有我，長時間在家工作，沒有其他寵物，也沒有小孩。以前養過貓，經驗豐富。"
    at.chat_input(key="chat_bot").set_value(prompt).run()

    assert len(at.chat_message) >= 2
    assert at.chat_message[1].children[0].value == prompt

    # Avoid 429 Too Many Requests error
    time.sleep(60)
    # check history print
    prompt = "請根據我的需求整理一下預算和照護的建議。"
    at.chat_input(key="chat_bot").set_value(prompt).run()
    assert len(at.chat_message) >= 4
    assert at.chat_message[3].children[0].value == prompt

    assert not at.exception


@pytest.mark.timeout(180 + 60)
def test_chat_autogen_word_cloud(mocker: MockFixture) -> None:
    # Avoid 429 Too Many Requests error
    time.sleep(60)

    # patch the property on the class
    mocker.patch.object(
        type(st.context), "locale", new_callable=PropertyMock, return_value="en"
    )

    at = AppTest.from_file("../src/streamlit_app.py", default_timeout=120).run()
    at.switch_page("./pages/pets_autogen.py").run()
    at.secrets["gemini_api_key"] = os.getenv("GEMINI_API_KEY")

    time.sleep(10)

    # check simple chat
    prompt = "幫我查詢最近兩篇 dcard 文章，然後將其內容畫成 wordcloud"
    at.chat_input(key="chat_bot").set_value(prompt).run()

    assert not at.exception
