# Pet Adoption Matching Agent

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://iwtba4188-11320iss507300-assistant.streamlit.app/)
<a href="github.com/iwtba4188/11320ISS507300_Assistant/actions/workflows/tests.yml" target="_blank">
    <img src="https://github.com/iwtba4188/11320ISS507300_Assistant/actions/workflows/tests.yml/badge.svg" alt="Test Action Status">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/iwtba4188/11320ISS507300_Assistant" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/iwtba4188/11320ISS507300_Assistant.svg" alt="Test Coverage">
</a>

Find your perfect pet companion with Pet Adoption Matching Agent! This Streamlit app uses the Gemini API to provide pet consultancy and adoption matching services. Whether you're looking for advice on pet care and budget, or trying to find a new furry friend, this app has you covered.

## Features

- **Pet Consultancy**: Ask questions about pet care, behavior, and budgeting.
- **Adoption Matching**: Get matched with pets available for adoption based on your preferences.
- **Word Cloud**: Visualize the most common words in the adoption articles.
- **User-Friendly Interface**:
  - Status badge to indicate the thinking process of the agent.
  - Spinner to show when the agent is processing your request.
  - Streaming responses to keep you engaged while waiting for answers.

## Usage Cases

- Prompt examples for pet consultancy:
  - "How much does it cost to take care of a cat?"
  - "What are the common health issues in dogs?"
  - "How can I train my puppy to stop biting?"
- Prompt examples for adoption matching:
  - "I want to adopt a dog that is good with children and has low maintenance."
  - "What pets are available for adoption in my area?"
  - "Can you suggest a pet that fits my lifestyle as a busy professional?"
- Prompt examples for word cloud:
  - "What are the most common words in pet adoption articles?"
- Real Example:
  - ![Example1](https://github.com/iwtba4188/Pet-Adoption-Matching-Agent/blob/main/example/pet-func_call-with_dcard_crawler.pdf)
  - ![Example2](https://github.com/iwtba4188/Pet-Adoption-Matching-Agent/blob/main/example/pet-func_call-with_vector_search.pdf)
  - ![Example3](https://github.com/iwtba4188/Pet-Adoption-Matching-Agent/blob/main/example/pet-func_call-with_vector_search-2.pdf)

## How to Run It on Your Own Machine

1. Install the requirements

   ```sh
   $ pip install -r requirements.txt
   ```

   or

   ```sh
   $ uv sync
   ```

2. Set your Gemini API key

   You may need to set your Gemini API key in the `secrets.toml` file. You can copy the `secrets.toml.example` file and rename it to `secrets.toml`. Then, set your API key in the file.

   ```sh
   $ cp secrets.toml.example secrets.toml
   ```

   Then, open the `secrets.toml` file and set your API key.

3. Run the app

   ```sh
   $ streamlit run ./src/streamlit_app.py
   ```
