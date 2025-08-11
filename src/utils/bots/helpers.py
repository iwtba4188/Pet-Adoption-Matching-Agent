from collections.abc import Generator

import streamlit as st

from utils.bots.ctx_mgr import CtxMgr


def display_chat_history(
    ctx: CtxMgr,
    user_image: str = "https://www.w3schools.com/howto/img_avatar.png",
) -> None:
    """
    Render past user and assistant messages from
    st.session_state.history using Streamlit chat messages.
    """
    histories = ctx.get_context()
    for history in histories:
        avatar = user_image if history["role"] == "user" else None
        st.chat_message(history["role"], avatar=avatar).markdown(history["content"])


def chat(ctx_history: CtxMgr, prompt: str, stream: Generator):
    """
    Post the user's prompt, invoke response streaming, and append messages to
    session state history.

    Arguments:
        prompt (str): Text entered by the user
    """
    user_image = "https://www.w3schools.com/howto/img_avatar.png"

    st.chat_message("user", avatar=user_image).write(prompt)
    ctx_history.add_context({"role": "user", "content": prompt})

    full_response = st.chat_message("assistant").write_stream(stream)

    if isinstance(full_response, str):
        full_response = [full_response]

    for response in full_response:
        ctx_history.add_context({"role": "assistant", "content": response})
