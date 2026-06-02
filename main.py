import os
import json
import asyncio
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from dotenv import load_dotenv
from mistralai.client import Mistral

load_dotenv()

app = FastAPI(title="Mistral AI Deployment Strategist Demo")

_context_path = os.path.join(os.path.dirname(__file__), "context.md")
with open(_context_path, "r") as f:
    ROLE_CONTEXT = f.read()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])
MODEL = "mistral-large-latest"

# ─── Role preamble (injected into every agent) ───────────────────────────────

BASE_PREAMBLE = f"""You are an expert agent inside a live AI Deployment Strategist workflow demo,
built to showcase the Mistral AI platform in a job interview context.

=== ROLE CONTEXT ===
{ROLE_CONTEXT}
=== END ROLE CONTEXT ===

CRITICAL INSTRUCTIONS:
- Produce REAL, SPECIFIC, QUANTIFIED outputs — never use [placeholder] brackets
- Reference the company by name throughout using their actual profile
- Demonstrate the competencies of an AI Deployment Strategist at every step
- Show deep knowledge of Mistral AI's unique advantages: open weights, EU sovereignty,
  on-premise deployment, multilingual support (Spanish, Catalan, Basque), EU AI Act compliance
- Be executive-grade: precise, confident, commercially minded
- Format with clean markdown — this renders live in a UI
"""

# ─── Agent Definitions ───────────────────────────────────────────────────────

AGENTS = [
    {
        "name": "Account Strategist",
        "color": "#FF7000",
        "system": """You are a senior AI Deployment Strategist at Mistral AI conducting an initial
discovery session with a new enterprise customer operating in Spain.

You apply the MEDDPICC qualification framework rigorously. You identify where AI creates
step-change business value, surface economic buyers and champions, and frame the art of the
possible in language that resonates with both C-level and technical audiences.

You know the Spanish enterprise market: procurement cycles, GDPR/EU AI Act sensitivity,
regional language complexity (Castilian, Catalan, Basque), and the strong preference for
European vendors for data-sensitive workloads. Mistral's open-weight models and EU-native
infrastructure are a rare competitive advantage here.""",

        "user_prompt": """Using the company profile researched above, produce the discovery brief
an AI Deployment Strategist would share with their AE and leadership after a first executive meeting.
Use their real profile, inferred pain points, and sector-specific AI opportunities.

## 🔍 Discovery Brief: {company}

### Executive Summary
[3 crisp sentences: who they are, why they are talking to Mistral now, what is at stake]

### MEDDPICC Qualification

**Metrics** (economic impact we must tie to)
- [Metric 1 — current baseline vs target, with a number]
- [Metric 2 — current baseline vs target, with a number]
- [Metric 3 — current baseline vs target, with a number]

**Economic Buyer**
[Name/title archetype, what they care about, how to approach them]

**Decision Criteria** (ranked)
1. [Most important criterion for this company]
2. [Second criterion]
3. [Third criterion]

**Decision Process**
[Realistic procurement timeline, who signs off, likely blockers]

**Pain**
[The explicit, quantified pain — what happens if they do nothing in 12 months]

**Champion**
[Who is our internal champion and why they need this to succeed]

**Competition**
[Who else is being evaluated — OpenAI/Azure/AWS/Palantir — and how Mistral wins]

### Priority Use Cases (ranked by impact × feasibility)

| # | Use Case | Current Pain | AI Impact | Mistral Advantage |
|---|----------|-------------|-----------|-------------------|
| 1 | [specific use case] | [real numbers] | [quantified] | [why Mistral specifically] |
| 2 | [specific use case] | [real numbers] | [quantified] | [why Mistral specifically] |
| 3 | [specific use case] | [real numbers] | [quantified] | [why Mistral specifically] |

### Recommended First Move
[Which use case to lead with, why, and how to structure the next conversation]

### Mistral's Differentiated Position vs Competition
- [Reason 1 specific to this company's situation]
- [Reason 2 specific to this company's situation]
- [Reason 3 specific to this company's situation]""",
    },

    {
        "name": "Value Engineer",
        "color": "#FF3C00",
        "system": """You are a Value Engineer at Mistral AI. You turn customer pain into a compelling,
quantified business case that makes a CFO approve the investment.

You build conservative, defensible ROI models — not optimistic projections. You calculate
FTE savings, process efficiency gains, cost avoidance, and revenue uplift. You can build
a payback period analysis and identify KPIs to track in a pilot.

You are fluent in CFO language: NPV, IRR, payback period, capex vs opex. You cite sector
benchmarks to anchor numbers. You make the financial case undeniable without over-promising.""",

        "user_prompt": """Using the discovery brief and company profile, build the business case for
this company's Mistral AI investment. This will be presented to their CFO and board.

## 📊 Business Case: Mistral AI for {company}

### Investment Summary
| Item | Value |
|------|-------|
| Total 3-Year Investment (Mistral licenses + implementation) | €X |
| Total 3-Year Value Generated | €X |
| Net ROI | X% |
| Payback Period | X months |
| Year-1 Net Value | €X |

### Use Case 1: [Top Priority Use Case Name]
**Current state:** [specific numbers from the company profile]

**Mistral solution:** [which Mistral model/product, how it integrates, on-prem vs API]

**Financial model:**
| Metric | Current | With Mistral | Delta |
|--------|---------|-------------|-------|
| [KPI 1] | X | X | -X |
| [KPI 2] | X | X | -X |
| Annual saving | — | — | €X |

**Year 1 savings: €X | Year 3 cumulative: €X**

### Use Case 2: [Second Priority Use Case Name]
**Current state:** [specific numbers]

**Mistral solution:** [specific model and integration approach]

**Financial model:**
| Metric | Current | With Mistral | Delta |
|--------|---------|-------------|-------|
| [KPI 1] | X | X | -X |
| [KPI 2] | X | X | -X |
| Annual saving | — | — | €X |

**Year 1 savings: €X | Year 3 cumulative: €X**

### Risk-Adjusted Scenarios
| Scenario | 3-Year ROI | Probability |
|----------|-----------|------------|
| Conservative | X% | 30% |
| Base | X% | 50% |
| Optimistic | X% | 20% |

### Pilot KPIs
| KPI | Baseline | Pilot Target | How Measured |
|-----|---------|-------------|--------------|
| [KPI 1] | X | X | [method] |
| [KPI 2] | X | X | [method] |
| [KPI 3] | X | X | [method] |

### The CFO Closer
[One punchy paragraph with the single most compelling financial argument for the CFO,
anchored to a number that is hard to ignore]""",
    },

    {
        "name": "PoV Architect",
        "color": "#CC2000",
        "system": """You are a Solutions Architect at Mistral AI specialising in Proofs of Value (PoVs)
for regulated European enterprises operating in Spain.

You design PoVs that prove business value in 6 weeks, de-risk technical integration, and
give the customer something to show their board. You are pragmatic — no gold-plating.

You know Mistral's products deeply:
- mistral-large-latest for complex reasoning
- mistral-embed for semantic search and RAG
- Mistral open weights (Mistral 7B, Mixtral 8x7B) for on-premise/sovereignty requirements
- Le Chat Enterprise for internal knowledge management
- La Plateforme for fast API prototyping

You build things that actually ship.""",

        "user_prompt": """Design a 6-week Proof of Value for the top priority use case identified above.
Make it specific to this company's technical environment and business context.

## 🏗️ PoV Design: {company} — [Top Use Case]

### PoV Objective & Success Criteria
**Objective:** [One sentence — what will be proven]

**Success criteria (must achieve ALL to proceed to production):**
| KPI | Baseline | PoV Target | Measurement |
|-----|---------|-----------|-------------|
| [KPI 1] | X | X | [how measured] |
| [KPI 2] | X | X | [how measured] |
| [KPI 3] | X | X | [how measured] |
| GDPR/AI Act compliance | — | 100% | Architecture audit |

### Technical Architecture

```
[ASCII diagram showing: data sources → Mistral stack → output/integration]
[Show on-prem vs cloud boundary clearly if relevant]
[Include the specific Mistral models used at each step]
```

### Tech Stack
| Layer | Technology | Why |
|-------|-----------|-----|
| LLM | [Mistral model] | [specific reason for this company] |
| [Layer] | [tech] | [reason] |
| [Layer] | [tech] | [reason] |
| Infrastructure | [cloud/on-prem] | [GDPR/sovereignty reasoning] |

### 6-Week Timeline
| Weeks | Phase | Key Tasks | Deliverable |
|-------|-------|-----------|-------------|
| 1–2 | Foundation | [tasks] | [deliverable] |
| 3–4 | Intelligence | [tasks] | [deliverable] |
| 5–6 | Validation | [tasks] | [deliverable] |

### Mistral Prompt Strategy
1. **[Use case step 1]:** [prompt approach, structured output format, confidence scoring]
2. **[Use case step 2]:** [RAG / chain-of-thought / etc.]

### Resources Required
- Mistral: [roles, time commitment, on-site vs remote]
- Customer: [roles needed from their side]
- Duration: 6 weeks | Cost to customer: €0 (Mistral-funded PoV)""",
    },

    {
        "name": "Executive Storyteller",
        "color": "#FF5500",
        "system": """You are the AI Deployment Strategist presenting to this company's executive committee.
20 minutes, 10 slides. Your audience: CTO, CFO, a business sponsor, and Legal/Compliance.

You are a master of executive communication:
- Executives buy outcomes, not technology
- Fear of falling behind competitors is as powerful as ROI
- Legal/compliance needs to hear "sovereignty" in the first 2 minutes
- The business champion needs to feel this is their initiative
- Preempt objections — never react to them

You structure every presentation: Burning Platform → Vision → Proof → Path → Call to Action.
You are concise, confident, and never over-promise.""",

        "user_prompt": """Write the board presentation narrative for {company}.
This is what an AI Deployment Strategist actually says in the room.

## 🎤 Executive Presentation: AI Deployment Strategy
### {company} × Mistral AI

---

### Slide 1: The Burning Platform *(60 seconds)*
[Opening hook with a number that makes the CFO lean forward.
Competitive threat, the regulatory clock, or the cost of inaction.]

---

### Slide 2: What Your Competitors Are Doing
[Concrete intelligence on sector peers and their AI moves.
What does 18 months behind mean in business terms for this company?]

---

### Slide 3: The Vision — What "AI-Native" Looks Like
[Paint the picture: what this company looks like in 24 months.
Before vs after for their most painful day-to-day process.]

---

### Slide 4: Why Now, Why Mistral
[Address the elephant: "Why not OpenAI / Microsoft?"
Three reasons specific to this company: sovereignty, language, open weights.]

---

### Slide 5: The Business Case *(CFO's slide)*
[ROI summary — 3 rows max. Headline number. Payback period.
One sentence: the most capital-efficient transformation available right now.]

---

### Slide 6: How It Works — Simply
[Architecture explained to a non-technical board. Zero jargon.
"Your [documents/data] go in. [Decisions/insights] come out. Your data never leaves [country/datacenter]."]

---

### Slide 7: The PoV — Proof Before Commitment
[De-risk the ask. 6 weeks. Funded by Mistral. Three success metrics.
"You don't pay for the pilot. You pay when you're convinced."]

---

### Slide 8: Addressing Your Concerns
**1. Data sovereignty / GDPR:** [sharp 2-sentence answer]
**2. "We've heard AI promises before":** [sharp 2-sentence answer]
**3. Change management / adoption:** [sharp 2-sentence answer]

---

### Slide 9: The Path Forward
[3-phase roadmap in under 15 words. Visual simplicity.
PoV (6 wks) → Production (Q[X]) → Platform Expansion (Year 2)]

---

### Slide 10: The Ask
[One clear ask. One number. One next step. Easy to say yes today.]

---

### Elevator Pitch *(30 seconds)*
[The version you'd tell the CTO in the lift]

### Handling the Hardest Question
**If the CFO asks: "What happens if this doesn't work?"**
[Honest, reassuring, commercially sound — 3 sentences]""",
    },

    {
        "name": "Deployment Strategist",
        "color": "#FF7000",
        "system": """You are the AI Deployment Strategist who owns this account after the PoV succeeds.
Your job: turn a pilot win into a multi-year strategic partnership.

You think in playbooks: pilot → production → platform expansion. You track KPIs monthly.
You proactively surface expansion opportunities before the customer asks. You make Mistral
indispensable to this account.

You monitor leading indicators, not just lagging ones. You manage political risk. You have
an executive sponsor cadence. You know how to turn a happy customer into a reference account
that generates pipeline across the sector.""",

        "user_prompt": """The PoV succeeded. {company} is ready to commit. Build the deployment and
expansion playbook that an AI Deployment Strategist owns for this account.

## 🚀 Deployment & Expansion Playbook: {company}

### Phase 1: Production Deployment *(Months 1–3)*
**Objective:** [Core use case live in production at full scale]

| Week | Milestone | Owner | Success Metric |
|------|-----------|-------|---------------|
| 1–2 | [milestone] | [role] | [metric] |
| 3–4 | [milestone] | [role] | [metric] |
| 5–8 | [milestone] | [role] | [metric] |
| 9–12 | [milestone] | [role] | [metric] |

**Top 2 risks and mitigations:**
1. [Risk — likelihood — mitigation]
2. [Risk — likelihood — mitigation]

---

### Phase 2: Expanded Deployment *(Months 4–6)*
[What gets added beyond the initial PoV scope, incremental value, key dependency]
**Incremental annual value: €X**

---

### Phase 3: Platform Expansion *(Months 7–18)*

| New Use Case | Stakeholder | Value Hook | Est. Annual ARR |
|-------------|-------------|-----------|----------------|
| [use case] | [owner] | [one-line hook] | €X |
| [use case] | [owner] | [one-line hook] | €X |
| [use case] | [owner] | [one-line hook] | €X |

**ARR Trajectory:**
- Post-PoV production: €X ARR
- Phase 2: €X ARR
- Phase 3 full platform: €X ARR
- **3-Year account value: €X**

---

### Monthly KPI Dashboard

| KPI | Baseline | Month 3 | Month 12 | Status |
|-----|---------|---------|---------|--------|
| [KPI 1] | X | X | X | 🔵 |
| [KPI 2] | X | X | X | 🔵 |
| [KPI 3] | X | X | X | 🔵 |

---

### Executive Cadence
- **Monthly:** [Operational review — who, agenda focus]
- **Quarterly:** [Strategic review — who, agenda focus]
- **Bi-annual:** [Board update — what story you tell]

---

### Expansion Conversation Script *(Month 4)*
[How you frame the Phase 3 conversation with the business champion —
making it feel like their idea, not an upsell]

---

### Reference Customer Strategy
[Why this company becomes Mistral's showcase in this sector in Spain,
what metrics they will share publicly, and how Mistral uses this account
to generate pipeline with 3 named sector peers]""",
    },
]


def build_preamble(company_profile: str) -> str:
    return f"""{BASE_PREAMBLE}

=== TARGET COMPANY PROFILE ===
{company_profile}
=== END COMPANY PROFILE ===
"""


async def stream_pipeline(company_name: str, company_profile: str):
    preamble = build_preamble(company_profile)
    conversation_history = []

    for agent in AGENTS:
        user_prompt = agent["user_prompt"].replace("{company}", company_name)
        system_msg = preamble + "\n\n" + agent["system"]
        messages = [{"role": "system", "content": system_msg}]

        if conversation_history:
            history_text = "\n\n---\n\n".join(
                f"### {e['agent']} Output:\n{e['content']}"
                for e in conversation_history
            )
            messages.append({
                "role": "user",
                "content": f"Full pipeline context so far:\n\n{history_text}\n\n---\n\nNow complete your task:\n\n{user_prompt}"
            })
        else:
            messages.append({"role": "user", "content": user_prompt})

        yield f"data: {json.dumps({'agent': agent['name'], 'type': 'start', 'color': agent['color']})}\n\n"

        full_response = ""
        for chunk in client.chat.stream(model=MODEL, messages=messages):
            delta = chunk.data.choices[0].delta.content
            if delta:
                full_response += delta
                yield f"data: {json.dumps({'agent': agent['name'], 'type': 'chunk', 'chunk': delta, 'color': agent['color']})}\n\n"

        conversation_history.append({"agent": agent["name"], "content": full_response})
        yield f"data: {json.dumps({'agent': agent['name'], 'type': 'done'})}\n\n"

    yield f"data: {json.dumps({'type': 'complete'})}\n\n"


async def research_company(company_name: str) -> str:
    """Use Mistral to research the company and build a structured profile."""
    messages = [
        {
            "role": "system",
            "content": """You are a business intelligence analyst. Given a company name,
produce a concise but rich company profile focused on their Spain presence and AI readiness.
Be factual and specific. If you are not certain of a number, give a reasonable estimate and flag it.
Format as structured text that other agents can use as ground truth."""
        },
        {
            "role": "user",
            "content": f"""Research {company_name} and produce a structured company profile.
Focus on their operations in Spain specifically.

Provide:
- Company overview (sector, size, global revenue, employees)
- Spain presence (offices, employees in Spain, Spain revenue if known)
- Core business operations in Spain
- Known technology stack or digital maturity signals
- Top 3 likely business challenges where AI could help
- Key competitors in Spain
- Regulatory context relevant to them (GDPR, sector-specific rules, EU AI Act exposure)
- Any known AI or digital transformation initiatives
- Likely key stakeholders (by role archetype: CTO, CFO, COO, DPO, etc.)

Be specific with numbers where possible. Flag estimates clearly.
This profile will be used to run a live Mistral AI deployment strategy simulation."""
        }
    ]

    response = await asyncio.to_thread(
        client.chat.complete, model=MODEL, messages=messages
    )
    return response.choices[0].message.content


@app.post("/research-company")
async def research_company_endpoint(request: Request):
    body = await request.json()
    company_name = body.get("company", "").strip()
    if not company_name:
        return {"error": "Company name required"}

    async def stream():
        yield f"data: {json.dumps({'type': 'researching', 'company': company_name})}\n\n"
        profile = await research_company(company_name)
        yield f"data: {json.dumps({'type': 'profile_ready', 'profile': profile})}\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.post("/run-pipeline")
async def run_pipeline(request: Request):
    body = await request.json()
    company_name = body.get("company", "Unknown Company")
    company_profile = body.get("profile", "No profile available.")

    return StreamingResponse(
        stream_pipeline(company_name, company_profile),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive", "X-Accel-Buffering": "no"}
    )


@app.get("/about")
async def serve_about():
    return FileResponse("about.html")


@app.get("/")
async def serve_index():
    return FileResponse("index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
