# JOKE_AGENT

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red)
![OpenRouter](https://img.shields.io/badge/OpenRouter-LLM-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

An AI-powered Joke Assistant built with Python, OpenRouter LLM, API Ninjas Jokes API, and Streamlit. The application uses LLM Function Calling (Tool Calling) to fetch real-time jokes from an external API and present them through both a Command-Line Interface (CLI) and a modern Streamlit web application.

---

## Overview

JOKE_AGENT combines the reasoning capabilities of a Large Language Model with external tools using Function Calling.

When a user requests a joke, the LLM automatically invokes the Joke API tool, retrieves a random joke from API Ninjas, and formats the response naturally. The project also maintains conversation history using local memory.

The application is available in two versions:

- Command-Line Interface (CLI)
- Streamlit Web Application

---

## Features

- AI-powered conversational joke assistant
- OpenRouter LLM with Function Calling
- Real-time joke retrieval using API Ninjas
- Persistent conversation memory
- Interactive Streamlit web interface
- Command-line application
- Multiple UI themes
- Local conversation history
- Graceful handling of unsupported requests

---

## Technology Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| LLM | OpenRouter |
| API | API Ninjas Jokes API |
| Web Framework | Streamlit |
| Environment | Python Dotenv |
| Storage | JSON |

---

## System Architecture

```text
                    User
                      │
                      ▼
            Streamlit UI / CLI
                      │
                      ▼
             Joke Assistant
                      │
         ┌────────────┴────────────┐
         ▼                         ▼
     OpenRouter LLM          Joke API Tool
         │                         │
         └────────────┬────────────┘
                      ▼
           API Ninjas Jokes API
                      │
                      ▼
           Formatted Joke Response
                      │
                      ▼
                    User
```

---

## Project Structure

```text
JOKE_AGENT/
│
├── main.py                # CLI application
├── streamlit_app.py       # Streamlit UI
├── tools.py               # Joke API integration
├── prompt.py              # System prompt
├── memory.py              # Memory management
├── memory.json            # Conversation history
├── .env                   # API keys
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/yourusername/JOKE_AGENT.git
```

Navigate to the project

```bash
cd JOKE_AGENT
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Setup

Create a `.env` file in the project root.

```env
OPENROUTER_API_KEY=your_openrouter_api_key
JOKES_API_KEY=your_api_ninjas_api_key
```

---

## API Keys

OpenRouter

https://openrouter.ai/

API Ninjas

https://api-ninjas.com/api/jokes

---

## Running the Application

### Command-Line Interface

```bash
python main.py
```

Example queries:

- Tell me a joke
- Make me laugh
- Another joke
- Random joke
- Tell me something funny

### Streamlit Web Application

```bash
streamlit run streamlit_app.py
```

The application will open at:

```
http://localhost:8501
```

---

## How It Works

1. The user enters a joke-related request.
2. OpenRouter interprets the prompt.
3. The model invokes the `get_joke()` tool using Function Calling.
4. The tool requests a random joke from API Ninjas.
5. The retrieved joke is returned to the LLM.
6. The LLM formats the final response.
7. Conversation history is stored locally in `memory.json`.

---

## Screenshots

### Home Page

<img width="1022" height="882" alt="Screenshot 2026-06-28 115329" src="https://github.com/user-attachments/assets/5704fb88-94b9-4a57-9f48-970cb03431a9" />


### Joke Response

*Example of a generated joke.*

<img width="895" height="861" alt="Screenshot 2026-06-28 115348" src="https://github.com/user-attachments/assets/6056b845-48c4-4534-a97e-ddae186aeebc" />


## Memory

Conversation history is stored locally in `memory.json`.

Delete or clear this file at any time to reset the assistant's memory.

---

## License

This project is licensed under the MIT License.

---

## Author

**Adithyaa Venkatesh**

GitHub: https://github.com/adithyaavenkatesh15

LinkedIn: https://www.linkedin.com/in/adithyaa-venkatesh-457aa42b4

---

## Acknowledgements

- OpenRouter
- API Ninjas
- Streamlit
- Python Community

---

## Support

If you found this project useful, consider giving it a star on GitHub. Your support helps improve the project and encourages future development.
