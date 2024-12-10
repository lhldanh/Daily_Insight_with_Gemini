import streamlit as st
from streamlit_modal import Modal
from utils import *

def main():
    # Init
    st.title('Today\'news on VNExpress Recap')
    models_avaiable = list_of_model()
    model = ''

    model_selection_col, recap_col = st.columns([1, 1])

    if 'model_selection' not in st.session_state:
        st.session_state['model_selection'] = ''
    # Model selection
    with model_selection_col:

        modal = Modal("Choose a model", key="model_selection")

        open_modal = st.button("Choose a model")
        if open_modal:
            modal.open()

        if modal.is_open():
            
            with modal.container():
                option = st.selectbox(
                "Choose a model. If no option to select, please pull the model from ollama",
                models_avaiable,
                )
                model_selected = client.models.retrieve(option)

                if st.button("Save and Close", key="save_close_btn"):
                    # Save the text to session state
                    st.session_state['model_selection'] = model_selected
                    modal.close()

    if st.session_state['model_selection']:
        model = st.session_state["model_selection"]
        st.success(f"Your choice: {st.session_state['model_selection'].id}")

    # Recap button
    with recap_col:
        recap_btn = st.button("Recap Today's News")
        keyword = st.text_input('Enter the keyword')
    if recap_btn and model == '' and keyword == '':
        st.warning('Please choose a model and enter a keyword first')
    elif recap_btn and model == '':
        st.warning('Please choose a model')
    elif recap_btn and keyword == '':
        st.warning('Please enter a keyword')
    elif recap_btn:
        st.success('Waiting for today recap..')
        urls = search_vnexpress(keyword)
        st.success(f'Found {len(urls)} news today about {keyword}')
        for url in urls:
            title, content = fetch_news_content(url)
            st.write(f':blue[{title}]')
            summary_content = summary(content)
            st.write(summary_content)

if __name__ == "__main__":
    main()
