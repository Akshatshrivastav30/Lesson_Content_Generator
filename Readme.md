Markdown# 🎓 Self-Evaluating Lesson Content Generator

An agentic system built with **LangGraph**, **LangChain**, and **Groq (GPT-OSS-120B)** that automatically generates, evaluates, and regenerates introductory learning content tailored for non-English-medium, 12th-grade graduates in India.

The core of this system is a strict **Generate → Evaluate → Regenerate** feedback loop that ensures lessons clear quality benchmarks—covering clarity, everyday Indian analogies, zero unexplained jargon, and sentence accessibility—before human delivery.

---

## 🏗️ System Architecture & Workflow

```text
       [ User Prompt / Topic ]
                  │
                  ▼
         ┌─────────────────┐
         │  generator_node │ ◄──────────────────────┐
         └────────┬────────┘                        │
                  │ (Lesson Draft)                  │
                  ▼                                 │
         ┌─────────────────┐                        │
         │  evaluator_node │                        │
         └────────┬────────┘                        │
                  │                                 │
                  ▼                                 │
     [ route_after_evaluation ]                     │
     ┌────────────┴───────────┐                     │
     │                        │                     │
[ Pass: Approved ]  [ Fail: Retries < 3 ]───────────┤
     │                        │ (Feedback History)  │
     ▼                        ▼                     │
   (END)           [ increment_retry_node ]─────────┘
                              │
                    [ Retries >= 3 Exceeded ]
                              │
                              ▼
                            (END)
Key Componentsgenerator_node: Drafts beginner-friendly content using ChatGroq. Integrates feedback history on retries to fix previous failure points.evaluator_node: Judges the draft against a strict 5-point binary rubric (Accuracy, Accessibility, Analogy, Jargon, Flow). Logs reason and actionable fixes on failure.route_after_evaluation: Conditional edge controlling state transitions. Loops back to generator if retries remain; otherwise terminates cleanly.📋 Evaluation RubricEvery lesson draft is evaluated on a strict PASS/FAIL basis across 5 dimensions:DimensionCriteriaAccuracy & GroundednessContent must be technically sound and accurate.AccessibilitySentences strictly concise (under 12–15 words per sentence).AnalogyTeaches using everyday Indian context (e.g., local vendors, notebooks).Jargon-FreeEvery technical term/acronym (e.g., RAG) MUST be defined inline immediately.Teaching FlowLogical progression through What it is, Why it matters, How it works, and Summary.🛠️ Prerequisites & Setup1. RequirementsPython: 3.10+Groq API Key: Obtainable from the Groq Console.2. Installation & Virtual EnvironmentBash# Clone the repository
git clone [https://github.com/your-username/self-evaluating-lesson-generator.git](https://github.com/your-username/self-evaluating-lesson-generator.git)
cd self-evaluating-lesson-generator

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
3. Environment VariablesCreate a .env file in the root directory:Code snippetGROQ_API_KEY=your_groq_api_key_here
🚀 Running the PipelineExecute the main agentic loop:Bashpython main.py
Example Output StructureUpon execution, the terminal outputs status logs, draft iterations, and audit details:Approved Execution: Prints full approved lesson structured into beginner-friendly sections.Audit Trail: Outputs attempt logs with specific criteria failures and generated remediation feedback.📂 Project StructurePlaintext.
├── config/
│   └── persona.py         # Target learner persona prompt definition
├── src/
│   ├── graph/
│   │   ├── nodes.py       # LangGraph nodes (Generator, Evaluator, Router)
│   │   └── state.py       # TypedDict AgentState & RejectionEntry schemas
│   └── schemas/
│       ├── evaluation.py  # Structured Pydantic evaluation output schema
│       └── lesson.py      # Lesson draft structure schema
├── .env                   # Environment variables (GROQ_API_KEY)
├── main.py                # Entry point & graph execution app
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation

---

### 📤 Git Push Commands

Run these terminal commands to stage the new `README.md` and push it to your repository:

```bash
# 1. Stage README.md
git add README.md

# 2. Commit changes
git commit -m "docs: add complete project README with Groq API setup and architecture details"

# 3. Push to remote repository
git push origin upstream