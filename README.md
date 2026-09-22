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