from collections import deque
from typing import Any

import streamlit as st


class CtxMgr:
    def __init__(
        self,
        name: str,
        init_container,
    ) -> None:
        self._name = f"{name}_ctx"
        if self._name not in st.session_state:
            st.session_state[self._name] = init_container

    @property
    def name(self) -> str:
        """
        Return the name of the context in st.session_state.
        """
        return self._name

    def add_context(self, content: Any) -> None:
        """
        Append a content item to st.session_state[self.ctx_name], initializing it as a deque of max
        length 20 if needed.
        """
        if self._name not in st.session_state:
            st.session_state[self._name] = deque(maxlen=20)
        st.session_state[self._name].append(content)

    def clear_context(self) -> None:
        """
        Clear the context in st.session_state[self.ctx_name].
        """
        st.session_state[self._name].clear()

    def get_context(self) -> Any:
        """
        Retrieve the current context from st.session_state[self.ctx_name].
        """
        return list(st.session_state[self._name])

    def empty(self) -> bool:
        return len(st.session_state[self._name]) == 0
