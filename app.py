import streamlit as st
from streamlit_modal import Modal


def main():
    st.title('Today Recap')
    col_enter_api, col_welcome = st.columns([1, 1])
    with col_enter_api:
        if 'api_key' not in st.session_state:
            st.session_state['api_key'] = ''

        # Create the modal
        modal = Modal("Set Gemini API Key", key="api_key_modal")

        open_modal = st.button("Set Gemini API Key")
        if open_modal:
            modal.open()

        if modal.is_open():
            with modal.container():
                st.write(
                    "[Click to see how to get gemini API key](https://aistudio.google.com/app/apikey)")
                text = st.text_input('Enter gemini key:', key="modal_input")

                # Modified button handling
                if st.button("Save and Close", key="save_close_btn"):
                    # Save the text to session state
                    st.session_state['api_key'] = text
                    # Close the modal
                    modal.close()

        gemini_api_key = ''
        if st.session_state['api_key']:
            gemini_api_key = st.session_state["api_key"]
            st.success(
                f"Current API Key: {st.session_state.api_key[:4]}******")

    with col_welcome:
        st.write("Description...")

    recap_btn = st.button("Recap Today's Meeting")

    if recap_btn and gemini_api_key:
        st.write("Recap button clicked and API key is set.")
    else:
        st.warning("Please set your Gemini API key first.")


if __name__ == "__main__":
    main()
