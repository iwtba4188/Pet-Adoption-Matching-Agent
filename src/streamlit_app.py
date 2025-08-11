import pandas as pd
import streamlit as st

from utils.i18n import i18n

pd.set_option("future.no_silent_downcasting", True)


def sidebar_name_to_page_title(pg_title: str) -> str:
    """
    Convert sidebar page labels to corresponding page titles based on i18n translations.

    Arguments:
        pg_title (str): The sidebar page label to convert

    Returns:
        str: The corresponding page title for the given sidebar label
    """
    if pg_title == i18n("sidebar.page_label.pets.chat"):
        return i18n("pets.chat.page_title")
    # elif pg_title == i18n("sidebar.page_label.week10.2d"):
    #     return i18n("week10.2d.page_title")
    # elif pg_title == i18n("sidebar.page_label.week10.3d"):
    #     return i18n("week10.3d.page_title")
    # elif pg_title == i18n("sidebar.page_label.week10.skip_gram"):
    #     return i18n("week10.skip_gram.page_title")
    # elif pg_title == i18n("sidebar.page_label.week10.cbow"):
    #     return i18n("week10.cbow.page_title")
    else:
        return pg_title


def setup_pages() -> None:
    """
    Configure and setup the Streamlit application pages.

    Sets up navigation with localized page titles, configures page settings,
    and runs the selected page.

    Returns:
        None
    """
    # TODO: When switching to the new page, the page title is flicking from
    #       `pet_sidebar_page_title` to `pet_page_config_page_title`.
    #
    #       One possible solution is to set the page name in the `navigation` function,
    #       but it is in the streamlit library.
    #       Related issue:
    #       https://github.com/streamlit/streamlit/issues/8388#issuecomment-2146227406
    #
    #       Another one is to use `st.page_link`, but it's not as convenient as
    #       `st.navigation`.
    pages = {
        i18n("sidebar.section_label.home"): [
            st.Page(
                "pages/home.py",
                title=i18n("sidebar.page_label.home"),
                default=True,
            )
        ],
        i18n("sidebar.section_label.pet"): [
            # st.Page(
            #     "pages/pets_gemini.py",
            #     title=i18n("sidebar.page_label.pets.chat"),
            # ),
            st.Page(
                "pages/pets_autogen.py",
                title=i18n("sidebar.page_label.pets.autogen"),
            ),
        ],
        # i18n("sidebar.section_label.week10"): [
        #     st.Page(
        #         "pages/word2vec-2d.py",
        #         title=i18n("sidebar.page_label.week10.2d"),
        #     ),
        #     st.Page(
        #         "pages/word2vec-3d.py",
        #         title=i18n("sidebar.page_label.week10.3d"),
        #     ),
        #     st.Page(
        #         "pages/word2vec-skip-gram.py",
        #         title=i18n("sidebar.page_label.week10.skip_gram"),
        #     ),
        #     st.Page(
        #         "pages/word2vec-cbow.py",
        #         title=i18n("sidebar.page_label.week10.cbow"),
        #     ),
        # ],
    }

    pg = st.navigation(pages)

    st.set_page_config(
        page_title=sidebar_name_to_page_title(pg.title),
        layout="wide",
        initial_sidebar_state="auto",
        menu_items={
            "Get Help": "https://streamlit.io/",
            "Report a bug": "https://github.com/iwtba4188/11320ISS507300_Assistant",
            "About": i18n("menu_items.about"),
        },
        page_icon="img/favicon.ico",
    )

    pg.run()


def lang_code_2_text(lang: str) -> str:
    """
    Convert a language code to its corresponding text representation.

    Arguments:
        lang (str): The language code to convert

    Returns:
        str: The corresponding text representation of the language code
    """
    lang_code_text = {
        "browser_default": "Browser Default",
        "en": "English",
        "zh-TW": "繁體中文",
        "zh-CN": "简体中文",
    }

    return lang_code_text.get(lang, "Unknown")


def setup_lang() -> None:
    """
    Set the application language based on the user selection in the sidebar.

    Returns:
        None
    """
    selected_lang = st.session_state.get("selected_lang", "browser_default")

    if selected_lang == "browser_default":
        print(f"Browser default language: {st.context.locale}")
        i18n.set_default_lang(st.context.locale)
        # XXX: Waiting the rerun context error to be fixed in Streamlit
        # ref: https://github.com/streamlit/streamlit/issues/11111
        i18n.set_default_lang(st.context.locale if st.context.locale else "en")
    i18n.set_lang(selected_lang)


def setup_sidebar() -> None:
    """
    Configure and display the application sidebar.

    Sets up the sidebar with a language selector that allows users to change
    the application language.

    Returns:
        None
    """
    lang_options = ["browser_default", "en", "zh-TW", "zh-CN"]
    selected_lang = st.session_state.get("selected_lang", "browser_default")

    with st.sidebar:
        st.selectbox(
            "Language",
            lang_options,
            index=lang_options.index(selected_lang),
            format_func=lang_code_2_text,
            on_change=setup_lang,
            key="selected_lang",
        )


if __name__ == "__main__":
    setup_lang()
    setup_pages()
    setup_sidebar()
