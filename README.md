# 🧠 Second Brain

**Second Brain** is an intelligent learning companion that decomposes complex subjects into simple, interactive roadmaps. By leveraging LLM agents and Directed Acyclic Graphs (DAGs), it helps you build a structured knowledge base and provides curated resources for every step of your learning journey.

## ✨ Features

- **LLM-Powered Decomposition**: Automatically break down any topic into logical sub-topics and prerequisites.
- **Interactive Roadmaps**: Visualize your learning path using dynamic graphs powered by `streamlit-agraph`.
- **Resource Gathering**: Automatically fetches theory summaries, recommended courses, and YouTube tutorials for each topic.
- **Persistent Memory**: Saves your progress and global "Second Brain" graph, allowing you to build on previous learning sessions.

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- API Keys for:
  - **Groq**: For LLM-powered planning and content generation.
  - **Exa**: For web search and resource discovery.
  - **YouTube**: For fetching relevant video tutorials.

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd dsa_second_brain
   ```

2. **Install dependencies**:
   Using `pip`:
   ```bash
   pip install -r requirements.txt
   ```
   Or using `uv` (recommended):
   ```bash
   uv sync
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in the root directory (or copy `.env example`):
   ```bash
   cp ".env example" .env
   ```
   Fill in your API keys in the `.env` file:
   ```env
   GROQ_API_KEY=your_groq_key
   EXA_API_KEY=your_exa_key
   YOUTUBE_API_KEY=your_youtube_key
   ```

### Running the App

Start the Streamlit application locally:
```bash
streamlit run app.py
```

### Running with Docker

You can also run the application using Docker:

```bash
cd docker
docker-compose up --build
```
The application will be available at `http://localhost:8501`.

## 📂 Project Structure

- `app.py`: The main Streamlit application and UI logic.
- `src/`: Core source code.
  - `agents/`: LLM agents for planning and execution.
  - `tools/`: External tool integrations (Exa, YouTube, etc.).
  - `memory/`: State management and persistence.
  - `core/`: Fundamental data structures (Graph, Node).
- `db/`: Local storage for saved states and caches.
- `docker/`: Docker configuration for deployment.

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Graph Visualization**: [streamlit-agraph](https://github.com/ChrisSmedley/streamlit-agraph)
- **LLM**: [Groq](https://groq.com/) 
- **Search**: [Exa AI](https://exa.ai/)
- **Data Handling**: [Pydantic](https://docs.pydantic.dev/)
