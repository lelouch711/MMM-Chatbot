from streamlit import sidebar

def display_sidebar():
    sidebar.title("MMM RAG Chatbot")
    sidebar.header("Navigation")
    sidebar.markdown("Use this sidebar to navigate through the chatbot features.")
    
    sidebar.subheader("Settings")
    sidebar.checkbox("Enable Notifications", value=True)
    sidebar.selectbox("Select Language", options=["English", "Spanish", "French"])
    
    sidebar.subheader("About")
    sidebar.info("This chatbot uses Retrieval-Augmented Generation (RAG) to provide answers.")
    
    sidebar.markdown("### Contact")
    sidebar.markdown("For support, please reach out to [support@example.com](mailto:support@example.com).")