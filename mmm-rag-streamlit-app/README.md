# MMM RAG Chatbot

This project implements a Retrieval-Augmented Generation (RAG) Chatbot using Streamlit. The chatbot is designed to answer queries based on a dataset and provides an interactive user interface for seamless communication.

## Project Structure

```
mmm-rag-streamlit-app
├── src
│   ├── streamlit_app.py        # Main entry point for the Streamlit application
│   ├── agent
│   │   ├── __init__.py         # Marks the agent directory as a package
│   │   ├── agent.py            # Implementation of the chatbot agent
│   │   └── tools.py            # Tools and utilities for the agent
│   ├── qa
│   │   ├── __init__.py         # Marks the QA directory as a package
│   │   └── qa_chain.py         # Logic for the QA chain
│   ├── components
│   │   ├── chat_ui.py          # User interface components for chat functionality
│   │   └── sidebar.py           # Sidebar components for navigation and settings
│   ├── utils
│   │   ├── loader.py           # Utility functions for loading data
│   │   └── session_state.py    # Manages session state for the Streamlit app
│   └── config.py               # Configuration settings for the application
├── data
│   └── MMM Dummy Data.xlsx      # Dummy data used by the chatbot
├── tests
│   └── test_agent.py           # Unit tests for the agent functionality
├── .streamlit
│   └── config.toml             # Configuration settings for the Streamlit application
├── requirements.txt             # Lists dependencies required to run the project
└── README.md                    # Documentation for the project
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd mmm-rag-streamlit-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the Streamlit application, execute the following command in your terminal:
```
streamlit run src/streamlit_app.py
```

Open your web browser and navigate to `http://localhost:8501` to interact with the MMM RAG Chatbot.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.