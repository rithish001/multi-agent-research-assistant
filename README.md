# 🧠 Multi-Agent Research Assistant

> An autonomous AI research pipeline that searches the web, summarizes findings, fact-checks them, and produces structured reports — all streamed in real time.

Built with **LangGraph**, **FastAPI**, **Ollama**, **ChromaDB**, and **Tavily Search API**.

---

## 📸 Demo

> _Clone the repo, add your `.env`, then run `docker compose up` to see it live._

---

## 🏗️ Architecture

```
User Query
    │
    ▼
┌─────────────────────────────────┐
│       LangGraph Orchestrator    │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────┐     ┌─────────────────┐     ┌──────────────────────┐
│   Researcher Agent  │────▶│ Summarizer Agent │────▶│ Fact Checker Agent   │
│  (Tavily web search │     │ (condenses into  │     │ (cross-validates with│
│ + ChromaDB memory)  │     │  clear output)   │     │  a second web query) │
└─────────────────────┘     └─────────────────┘     └──────────────────────┘
                                                              │
                                                              ▼
                                                 ┌────────────────────────┐
                                                 │      Writer Agent      │
                                                 │ (structured final      │
                                                 │  report + stores to    │
                                                 │  ChromaDB memory)      │
                                                 └────────────────────────┘
                                                              │
                                                              ▼
                                                   Streamed to FastAPI
                                                   & Streamlit frontend
```

Each agent gets a structured prompt with explicit instructions, so the LLM has clear context at every step rather than passing raw text through blindly.

---

## ✨ Features

- **Multi-agent pipeline** — four specialised agents orchestrated by LangGraph, each with a distinct role and prompt
- **Real-time web search** — Tavily API with query trimming to stay within payload limits
- **Persistent RAG memory** — ChromaDB stores past research; relevant history is injected into the researcher's context automatically
- **Streaming API** — FastAPI `StreamingResponse` yields per-agent output as it happens, so users see progress in real time
- **Local LLM** — runs entirely on-device via Ollama (no OpenAI key required)
- **Streamlit UI** — quick interactive frontend for demos and testing
- **Modular structure** — agents, tools, memory, and API are fully separated for easy extension
- **Docker Compose** — one-command deployment for both backend and frontend
- **Benchmark harness** — latency and output tracking across a sample query set

---

## 🛠️ Tech Stack

| Layer | Technology | Role |
|---|---|---|
| Orchestration | LangGraph | Agent graph + state routing |
| LLM | Ollama (local) | Inference without cloud dependency |
| LLM integration | LangChain | Prompt building and chain management |
| Web search | Tavily API | Real-time, research-grade search results |
| Memory | ChromaDB | Persistent vector store for past queries |
| Embeddings | Ollama (`qwen2.5:0.5b`) | Local embedding generation |
| Backend | FastAPI | Streaming REST API |
| Frontend | Streamlit | Interactive demo UI |
| Deployment | Docker Compose | Containerised multi-service setup |

---

## 📂 Project Structure

```
multi_agent_research/
│
├── agents/
│   ├── researcher.py       # Combines web results + memory into research context
│   ├── summarizer.py       # Condenses research into clear summary
│   ├── fact_checker.py     # Validates summary against a second web query
│   └── writer.py           # Produces final structured report
│
├── api/
│   └── routes.py           # FastAPI streaming endpoint (/research/stream)
│
├── config/
│   └── llm_config.py       # Ollama model config
│
├── eval/
│   ├── sample_queries.json # Input queries for benchmarking
│   ├── results.json        # Benchmark output (latency + response previews)
│   └── benchmark.py        # Benchmark runner script
│
├── graph/
│   └── graph_builder.py    # LangGraph state machine definition
│
├── memory/
│   └── vector_store.py     # ChromaDB store/retrieve helpers
│
├── tools/
│   └── search_tool.py      # Tavily client + query trimmer
│
├── main.py                 # FastAPI app entrypoint
├── streamlit_app.py        # Streamlit demo UI
├── docker-compose.yml      # Multi-service Docker setup
├── Dockerfile              # Container image definition
├── requirements.txt
└── .env.example
```

---

## ⚙️ Setup

### Prerequisites

- [Docker](https://www.docker.com/) and Docker Compose
- [Ollama](https://ollama.com) installed and running locally
- A [Tavily API key](https://tavily.com) (free tier available)

### 1. Clone the repo

```bash
git clone https://github.com/rithish001/multi-agent-research-assistant.git
cd multi-agent-research-assistant
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env`:

```env
TAVILY_API_KEY=your_tavily_api_key_here
```

### 3. Pull the local model

```bash
ollama pull qwen2.5:0.5b
```

### 4. Start all services

```bash
docker compose up --build
```

| Service | URL |
|---|---|
| FastAPI backend | http://localhost:8000 |
| Streamlit frontend | http://localhost:8501 |

> **Note:** Ollama must be running on the host machine before starting the containers.

---

### Manual setup (without Docker)

<details>
<summary>Expand</summary>

```bash
pip install -r requirements.txt
uvicorn main:app --reload          # terminal 1
streamlit run streamlit_app.py     # terminal 2
```

</details>

---

## 🔌 API Usage

### POST `/research/stream`

Streams agent outputs as plain text, one agent at a time.

**Request**

```bash
curl -X POST http://localhost:8000/research/stream \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the latest breakthroughs in quantum computing?"}'
```

**Streamed response**

```
🔹 Agent: researcher
research:
[Researcher output with web results and memory context...]

🔹 Agent: summarizer
summary:
[Concise summary of research...]

🔹 Agent: fact_checker
checked:
[Verified content with inconsistencies flagged...]

🔹 Agent: writer
final:
[Structured final report...]
```

---

## 📊 Benchmarking

A lightweight benchmark harness is included under `eval/` to measure pipeline performance across a sample query set.

### Run the benchmark

```bash
python eval/benchmark.py
```

Results are saved to `eval/results.json` with the following fields per query:

| Field | Description |
|---|---|
| `query` | Input query string |
| `latency_seconds` | End-to-end pipeline time |
| `output_length` | Character count of the final report |
| `final_output` | First 500 characters of the writer's output |

### Sample output

```json
{
    "query": "What is the current state of fusion energy?",
    "latency_seconds": 14.32,
    "output_length": 1842,
    "final_output": "## Fusion Energy — State of Play\n\nAs of 2025, ..."
}
```

> To add your own queries, edit `eval/sample_queries.json` before running.

---

## 🧩 How It Works

1. **Researcher** retrieves relevant past queries from ChromaDB and runs a live Tavily web search. Both are injected into a structured prompt, and the LLM extracts factual, relevant information.

2. **Summarizer** receives the research output and condenses it into a clear, concise summary.

3. **Fact Checker** runs a second independent Tavily search and cross-validates the summary against fresh data, flagging any inconsistencies.

4. **Writer** generates the final structured report and stores it in ChromaDB so future similar queries can benefit from the result.

Each step is streamed to the client as it completes, so users see the pipeline running live rather than waiting for a single final response.

---

## 🗺️ Roadmap

- [x] Docker Compose setup for one-command deployment
- [x] Benchmark harness with latency + output tracking
- [ ] TypedDict state for stronger agent state typing
- [ ] Conditional routing (e.g. skip fact-check for low-stakes queries)
- [ ] Quality scoring in benchmark (accuracy / relevance rubric)
- [ ] Support for multiple local models per agent
- [ ] Export report as PDF or Markdown file
- [ ] Ollama as a Docker Compose service (fully self-contained stack)

---

## 📄 License

MIT
