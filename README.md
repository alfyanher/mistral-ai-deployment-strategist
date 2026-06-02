# Mistral AI — Enterprise Deployment Strategist Demo

> A live multi-agent AI pipeline that simulates a complete enterprise engagement — from discovery to deployment — built entirely on Mistral AI. Created as an interview showcase for the **AI Deployment Strategist** role at Mistral AI.

---

## What This Does

You type any company name with operations in Spain. Five specialised AI agents then simulate the full lifecycle of a real Mistral AI enterprise engagement — the same workflow an AI Deployment Strategist executes on the job:

| Agent | What it does |
|---|---|
| 🔍 **Account Strategist** | Researches the company, runs a MEDDPICC qualification, identifies top pain points and use cases |
| 📊 **Value Engineer** | Builds a quantified business case — ROI model, payback period, CFO-ready financial tables |
| 🏗️ **PoV Architect** | Designs a 6-week on-premise Proof of Value using Mistral open weights for EU data sovereignty |
| 🎤 **Executive Storyteller** | Writes the 10-slide board presentation narrative — burning platform to call to action |
| 🚀 **Deployment Strategist** | Builds the production deployment timeline, KPI dashboard, and 18-month account expansion playbook |

Every agent receives the full output of all previous agents as context, so the outputs build coherently — just like a real engagement handoff.

Responses stream live token-by-token via Server-Sent Events. When the pipeline completes, you can export the full engagement as a formatted PDF report.

---

## Why It Was Built

The AI Deployment Strategist role sits at the intersection of business strategy, AI innovation, and hands-on deployment. This project demonstrates each of the four core competencies from the job description:

- **Strategic Discovery** — MEDDPICC qualification, executive workshop simulation
- **AI Solution Design** — on-prem architecture, EU AI Act compliance, Mistral open weights
- **Value Realization** — ROI modelling, payback period, KPI dashboards
- **Cross-functional Collaboration** — full context chaining across 5 specialist agents

Rather than claiming these skills, the project shows them running live.

---

## Spain Market Context

The agents are trained to surface Mistral's specific competitive advantages in the Spanish market:

- **EU Sovereignty** — Mistral's open weights enable full on-premise deployment; data never leaves Spain
- **Multilingual** — Native support for Spanish, Catalan, and Basque
- **NextGenerationEU Funding** — Spain has €70B+ in EU digital transformation funds available for AI pilots
- **SME Opportunity** — 99.8% of Spanish businesses are SMEs, underserved by US hyperscalers

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | `mistral-large-latest` via Mistral La Plateforme API |
| Backend | Python · FastAPI · Server-Sent Events (SSE) |
| Frontend | Vanilla HTML/CSS/JS (single file, no build step) |
| PDF Export | jsPDF (client-side, no server dependency) |
| Company Research | Mistral API (real-time, on every query) |
| Agent chaining | Full conversation history passed to each agent |

---

## Project Structure

```
mistral-sample/
├── main.py          # FastAPI backend — 5 agents, SSE streaming, company research endpoint
├── index.html       # Single-file frontend — search, pipeline UI, PDF export
├── about.html       # Project summary page (/about route)
├── context.md       # Role context and Spain market data injected into every agent
├── requirements.txt # Python dependencies
└── .env             # API key (not committed — see setup below)
```

---

## Setup & Run

### 1. Clone the repo

```bash
git clone https://github.com/alfyanher/mistral-ai-deployment-strategist.git
cd mistral-ai-deployment-strategist
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your Mistral API key

Create a `.env` file in the project root:

```
MISTRAL_API_KEY=your_key_here
```

Get your API key at [console.mistral.ai](https://console.mistral.ai).

### 4. Start the server

```bash
uvicorn main:app --reload
```

### 5. Open the app

Go to [http://localhost:8000](http://localhost:8000)

---

## How to Use

1. Type a company name in the search bar — suggestions include Santander, BBVA, Telefónica, Inditex, MAPFRE, and 15+ others
2. Any company with Spain operations works — not just the suggestions
3. Click **Analyse** (or press Enter)
4. Watch five agents think and write in real time
5. Use **Expand all / Collapse all** to navigate the results
6. Click **Export Full Report as PDF** for a shareable, formatted report

The **"mistral-large-latest · Live API"** pill in the top bar opens a modal showing the full tech stack and Mistral API documentation links.

The **"About this project"** link opens `/about` — a plain-language explanation of what the project does and why it was built.

---

## Agent Architecture

Each agent has:
- A **system prompt** defining its role, expertise, and output style
- A **user prompt** with a structured template that forces quantified, specific outputs
- Access to the **full output history** of every preceding agent

The pipeline runs sequentially: Account Strategist → Value Engineer → PoV Architect → Executive Storyteller → Deployment Strategist. Each agent's output becomes part of the next agent's context, so the PoV Architect knows the business case, the Executive Storyteller knows the architecture, and the Deployment Strategist knows everything.

Company research is a separate pre-pipeline step: before any agent runs, Mistral researches the target company and builds a structured profile covering their Spain operations, technology stack, likely pain points, and regulatory exposure. This profile is injected into every agent's system prompt.

---

## PDF Export

The PDF export generates a clean, human-readable report (white background, black text, under 10 pages) with:

- Cover page with company name, pipeline stages, and date
- Executive summary with key tables
- One section per agent — highlights only, no code
- Recommended immediate next steps
- Generated entirely client-side with jsPDF — no server required

---

## Built With

- [Mistral AI](https://mistral.ai) — `mistral-large-latest` model
- [La Plateforme](https://console.mistral.ai) — Mistral's API platform
- [FastAPI](https://fastapi.tiangolo.com)
- [jsPDF](https://github.com/parallax/jsPDF)
- [marked.js](https://marked.js.org) — markdown rendering in the browser

---

## Disclaimer

Company data is researched in real time by Mistral AI and may contain estimates. All strategic recommendations are AI-generated and should be validated by a qualified human strategist before use in a real client engagement. This project is a demonstration tool, not a production business intelligence system.
