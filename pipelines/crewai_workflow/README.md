# CrewAI Workflow

A multi-agent policy generation system using CrewAI. Four specialized agents collaborate sequentially to research, draft, review, and finalize a professional policy document on any topic.

> **Environment setup:** See the [root README](../../README.md) for Python version requirements, venv creation, and dependency installation.

---

## Architecture

```
User Topic (CLI or Streamlit)
    │
    ▼
┌─────────────────────────────────────────────┐
│                  CrewAI Crew                │
│                                             │
│  ┌─────────────────────┐                    │
│  │  Policy Research    │  → research_topic  │
│  │  Analyst            │  → generate_content│
│  └──────────┬──────────┘                    │
│             │ research output               │
│  ┌──────────▼──────────┐                    │
│  │  Policy Writer      │  → generate_content│
│  └──────────┬──────────┘                    │
│             │ draft policy                  │
│  ┌──────────▼──────────┐                    │
│  │  Compliance &       │  → research_topic  │
│  │  Legal Reviewer     │  → generate_content│
│  └──────────┬──────────┘                    │
│             │ compliance notes              │
│  ┌──────────▼──────────┐                    │
│  │  Policy Editor &    │  → generate_content│
│  │  Formatter          │                    │
│  └──────────┬──────────┘                    │
└─────────────┼───────────────────────────────┘
              │
              ▼
    Final Policy Document
```

---

## Agents

| Agent | Role | Responsibility |
|-------|------|----------------|
| Policy Research Analyst | Researcher | Web searches for current best practices, legal requirements, and real examples |
| Policy Writer | Writer | Drafts a structured policy document from research output |
| Compliance & Legal Reviewer | Reviewer | Checks for legal gaps, missing clauses, and risk exposure |
| Policy Editor & Formatter | Editor | Produces the final polished, publication-ready document |

---

## Tools

Both tools are available to all agents:

| Tool | Description |
|------|-------------|
| `research_topic` | Searches the web via Tavily for current, accurate information |
| `generate_content` | Calls the LLM to generate or structure content |

---

## Running

### CLI — any topic

```bash
python -m pipelines.crewai_workflow.src.crewai_version "Create a parental leave policy for a US startup"
python -m pipelines.crewai_workflow.src.crewai_version "Write a remote work policy for a global tech company"
python -m pipelines.crewai_workflow.src.crewai_version "Draft a data privacy policy for a healthcare SaaS"
```

### Default topic (no argument)

```bash
python -m pipelines.crewai_workflow.src.crewai_version
```

Runs with the default topic: *Create a Work From Home policy for US-based tech companies*

### Streamlit UI

```bash
streamlit run app/main.py
```

Navigate to **Page 5 — CrewAI** in the sidebar. Enter any policy topic and click Run.

---

## Key Design Decisions

**Dynamic topics** — the pipeline accepts any policy topic via CLI argument or Streamlit input. It is not hardcoded to a specific use case.

**Real web search** — agents call `research_topic` to retrieve live information from the web rather than relying on LLM training data.

**Retry logic** — the pipeline automatically retries on Groq rate limit errors with increasing wait times (30s, 60s, 90s).

**Centralized model config** — the LLM model is configured via `.env`. Set `CREWAI_MODEL` to override the default:

```env
DEFAULT_MODEL=llama-3.3-70b-versatile
CREWAI_MODEL=groq/llama-3.3-70b-versatile  # optional override
```

---

## File Structure

```
crewai_workflow/
├── src/
│   ├── crewai_version.py    # Crew definition, agents, tasks, execution
│   └── shared_tools.py      # research_topic and generate_content tools
└── README.md
```

---

## Notes

- CrewAI workflows are token-heavy — each agent makes multiple LLM calls. The Groq free tier (12K TPM) may throttle mid-run. Built-in retry logic handles this automatically.
- Sequential execution means each agent receives the previous agent's output as context.
- All shared utilities (`llm_utils`, `web_search_utils`) are imported from `shared/utils/` — no code duplication.