import streamlit as st


def page_init() -> None:
    st.title("Welcome to the Pet Adoption App")
    st.write("This app is designed to help you find your perfect pet!")
    st.markdown(
        """
        ### Features
        - **Pet Consultancy**: Ask questions about pet care, behavior, and budgeting.
        - **Adoption Matching**: Get matched with pets available for adoption based on your preferences.
        - **Word Cloud**: Visualize the most common words in the adoption articles.
        - **User-Friendly Interface**:
            - Status badge to indicate the thinking process of the agent.
            - Spinner to show when the agent is processing your request.
            - Streaming responses to keep you engaged while waiting for answers.

        ### How to Use
        1. Navigate through the sidebar to explore agent features.
        2. Use the chat interface to ask questions or get pet recommendations.
        """
    )


if __name__ == "__main__":
    page_init()
