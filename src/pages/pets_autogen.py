import os

import streamlit as st
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.conditions import TextMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.tools import AgentTool
from autogen_core.models import ModelInfo
from autogen_ext.models.openai import OpenAIChatCompletionClient

from utils.bots import display_chat_history
from utils.bots.ctx_mgr import CtxMgr
from utils.function_call import (
    content_wordcloud,
    # mock_crawling_dcard_article_content,
    # mock_crawling_dcard_urls,
    query_top_k_match_contents,
)
from utils.helpers import (
    error_badge,
    info_badge,
    read_file_content,
    st_spinner,
    str_stream,
    success_badge,
)
from utils.i18n import i18n

input_field_placeholder = i18n("pets.chat.input_placeholder")
user_name = "Shihtl"
ctx_history = CtxMgr("pets_gemini_history", [])
# ctx_content = CtxMgr("pets_gemini", deque(maxlen=10))


def page_init() -> None:
    """
    Set the Streamlit page title using the localized message and configured user name.
    """
    st.title(i18n("pets.chat.doc_title").format(user_name=user_name))
    st.markdown(
        """<style>
    div.stSpinner > div {
        padding-left: 55px;
    }
    img.wordcloud {
        padding-left: 55px;
        padding-bottom: 35px;
    }
</style>""",
        unsafe_allow_html=True,
    )


def init_agents() -> None:
    model_client = OpenAIChatCompletionClient(
        model="gemini-2.5-flash",
        model_info=ModelInfo(
            vision=True,
            function_calling=True,
            json_output=True,
            family="unknown",
            structured_output=True,
        ),
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    if "budget_assistant" not in st.session_state:
        st.session_state.budget_assistant = AssistantAgent(
            name="budget_assistant",
            model_client=model_client,
            system_message=read_file_content(
                "./src/static/BudgetAdvisor_Agent_Prompt.txt"
            ),
            description="A budget advisor agent that provides budget suggestions based on user needs.",
        )
    if "careguide_assistant" not in st.session_state:
        st.session_state.careguide_assistant = AssistantAgent(
            name="careguide_assistant",
            model_client=model_client,
            system_message=read_file_content("./src/static/CareGuide_Agent_Prompt.txt"),
            description="A care guide agent that provides care suggestions based on user needs.",
        )
    if "match_maker_assistant" not in st.session_state:
        st.session_state.match_maker_assistant = AssistantAgent(
            name="match_maker_assistant",
            model_client=model_client,
            system_message=read_file_content(
                "./src/static/Matchmaker_Agent_Prompt.txt"
            ),
            description="A match maker agent that provides match suggestions based on user needs.",
            tools=[query_top_k_match_contents],
        )

    if "head_assistant" not in st.session_state:
        st.session_state.head_assistant = AssistantAgent(
            name="head_assistant",
            model_client=model_client,
            tools=[
                # mock_crawling_dcard_urls,
                # mock_crawling_dcard_article_content,
                content_wordcloud,
                AgentTool(agent=st.session_state.budget_assistant),
                AgentTool(agent=st.session_state.careguide_assistant),
                AgentTool(agent=st.session_state.match_maker_assistant),
            ],
            system_message=read_file_content("./src/static/system_prompt.txt"),
        )
    if "assistant_team" not in st.session_state:
        termination_condition = TextMessageTermination("head_assistant")
        st.session_state.team = RoundRobinGroupChat(
            [st.session_state.head_assistant],
            termination_condition=termination_condition,
        )


async def autogen_response_stream(task: str):
    full_response = ""
    spinner_list = [
        (
            "gemini_response",
            st_spinner(text=i18n("pets.chat.spinner.gemini_response"), show_time=True),
        ),
    ]

    def record_then_yield(this_response):
        nonlocal full_response
        full_response += this_response
        yield str_stream(this_response)

    def add_spinner(spinner_name, spinner_text):
        spinner = st_spinner(text=spinner_text, show_time=True)
        spinner_list.append((spinner_name, spinner))
        return spinner

    def find_spinner_and_end(spinner_name):
        for name, spinner in spinner_list:
            if name == spinner_name:
                spinner.end()
                return True
        return False

    async for event in st.session_state.team.run_stream(task=task):
        print(event, end="\n\n")

        if isinstance(event, TaskResult):
            ctx_history.add_context({"role": "assistant", "content": full_response})
            return

        if event.source == "user":
            continue

        find_spinner_and_end("gemini_response")
        match event.type:
            case "TextMessage":
                find_spinner_and_end("rethink")
                yield record_then_yield(event.content)
            case "ThoughtEvent":
                yield record_then_yield(event.content)
            case "ToolCallRequestEvent":
                for func_call in event.content:
                    badge_str = info_badge(
                        i18n("pets.chat.spinner.func_call_text").format(
                            func_call_name=func_call.name
                        )
                    )
                    spinner_func_call_text = i18n(
                        "pets.chat.spinner.func_call_text"
                    ).format(func_call_name=func_call.name)
                    add_spinner(func_call.name, spinner_func_call_text)
                    yield record_then_yield(badge_str)
            case "ToolCallExecutionEvent":
                for result in event.content:
                    find_spinner_and_end(result.name)
                    if result.is_error:
                        badge_str = error_badge(
                            i18n("pets.chat.badge.func_call_error").format(
                                func_name=result.name
                            )
                        )
                    elif not result.is_error:
                        badge_str = success_badge(
                            i18n("pets.chat.badge.func_call_success").format(
                                func_name=result.name
                            )
                        )
                    yield record_then_yield(badge_str)

                    if result.name == "content_wordcloud":
                        st.markdown(result.content, unsafe_allow_html=True)
            case "ToolCallSummaryMessage":
                add_spinner("rethink", i18n("pets.chat.spinner.rethink_text"))
            case _:
                pass


def chat_init() -> None:
    st.chat_message("assistant").write_stream(
        autogen_response_stream(
            f"Please introduce yourself, using lang: {i18n.lang}, using default_lang if not applicable: {i18n.default_lang}"
            # "Please introduce yourself, using lang: english"
        )
    )

    st.session_state.team.reset()


def chat(prompt: str):
    """
    Post the user's prompt, invoke response streaming, and append messages to
    session state history.

    Arguments:
        prompt (str): Text entered by the user
    """
    user_image = "https://www.w3schools.com/howto/img_avatar.png"

    st.chat_message("user", avatar=user_image).write(prompt)
    ctx_history.add_context({"role": "user", "content": prompt})

    st.chat_message("assistant").write_stream(autogen_response_stream(prompt))


def chat_bot():
    """
    Render the chat interface and process user input in Streamlit.

    Creates a bordered container to display chat history and a chat input field.
    When the user submits a message, calls chat() inside the same container to
    render and stream the assistant's response.
    """
    chat_container = st.container(border=True)
    with chat_container:
        if ctx_history.empty():
            chat_init()
            pass
        else:
            display_chat_history(ctx_history)

    if prompt := st.chat_input(placeholder=input_field_placeholder, key="chat_bot"):
        with chat_container:
            chat(prompt=prompt)


if __name__ == "__main__":
    # XXX: warning: Task was destroyed but it is pending! ref: https://zhuanlan.zhihu.com/p/602955920
    page_init()
    init_agents()
    chat_bot()
