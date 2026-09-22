# IntentDiff – Multi-Agent Intent Drift Detection

IntentDiff is a multi-agent AI prototype built with Microsoft Azure AI Foundry that detects when an AI agent's proposed actions drift beyond a user's original intent.

> Git diff shows how code changed. IntentDiff shows how an agent's mission changed.

## Why IntentDiff?

As AI systems become more agentic, a user's simple request can evolve into a plan containing actions the user never explicitly authorized.

IntentDiff introduces an intent-checking layer between planning and execution. It compares proposed actions with the user's original intent and identifies potential scope expansion before downstream actions are taken.

## Architecture

IntentDiff uses three specialized Microsoft Azure AI Foundry agents:

1. **Intent Agent** – Converts the user's request into a structured intent contract describing the goal, allowed actions, constraints, unclear authority, and unsupported actions.
2. **Planner Agent** – Creates a practical plan for accomplishing the requested task.
3. **IntentDiff Agent** – Compares the proposed plan with the original intent contract and classifies proposed actions.

### Classification Model

- **WITHIN** – Clearly supported by the user's original intent.
- **AMBIGUOUS** – Potentially reasonable, but the user's authority is unclear; human clarification or approval is needed.
- **EXPANDED** – Introduces a material action, side effect, or objective beyond the original authorization; human review is required.

## Workflow

```text
User Request
     |
     v
Intent Agent
     |
     v
Original Intent Contract
     |
     v
Planner Agent
     |
     v
Proposed Plan
     |
     v
IntentDiff Agent
     |
     +---- WITHIN
     |
     +---- AMBIGUOUS ----> Human Review
     |
     +---- EXPANDED -----> Human Review

     ## Evaluation

IntentDiff includes a custom classification evaluation for the IntentDiff Agent.

A controlled three-case dataset tests the three core classifications:

- **WITHIN** — an action clearly authorized by the original intent.
- **AMBIGUOUS** — an action where authority is unclear and human review is appropriate.
- **EXPANDED** — an action that goes beyond the user's authorized scope.

The current controlled evaluation achieved **3/3 correct classifications (100%)** in Microsoft Azure AI Foundry.

This result validates the prototype against the initial test cases; it should not be interpreted as production-level accuracy. A production evaluation suite would require a substantially larger and more diverse dataset, including edge cases and regression tests.

## Observability

IntentDiff uses OpenTelemetry with Microsoft Azure AI Foundry / Application Insights to trace the complete multi-agent workflow.

The orchestration creates a parent workflow span containing calls to the three specialized agents, making it possible to inspect:

- End-to-end and per-agent execution flow
- Agent and model calls
- Latency
- Token usage
- Failures and errors

For a production deployment, observability could be extended with classification distributions, human-review frequency and outcomes, cost monitoring, and regression tracking across prompt, model, and agent changes.

## Running the Project
### Prerequisites

- Python 3.11+
- An Azure AI Foundry project
- Azure CLI authentication
- Access to the three configured Foundry agents:
  - `intent-agent`
  - `planner-agent`
  - `intent-diff-agent`

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure the Foundry endpoint

Set the project endpoint as an environment variable instead of storing it in source code.

PowerShell:

```powershell
$env:AZURE_AI_PROJECT_ENDPOINT="https://<your-resource>.services.ai.azure.com/api/projects/<your-project>"
```

### Run IntentDiff

```bash
python intentdiff.py
```

The application uses `DefaultAzureCredential` for authentication. No API keys or credentials should be committed to the repository.