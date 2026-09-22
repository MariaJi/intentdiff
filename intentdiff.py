from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
import os

endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
user_request = input("Enter your request: ")
project_client = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
)


# Configure Foundry/Application Insights observability
connection_string = project_client.telemetry.get_application_insights_connection_string()
configure_azure_monitor(connection_string=connection_string)

tracer = trace.get_tracer("IntentDiff")
openai_client = project_client.get_openai_client()
# Trace the complete multi-agent orchestration
with tracer.start_as_current_span("IntentDiff Workflow"):
    intent_response = openai_client.responses.create(
        input=[
            {
                "role": "user",
                "content": user_request
            }
        ],
        extra_body={
            "agent_reference": {
                "name": "intent-agent",
                "version": "3",
                "type": "agent_reference"
            }
        },
    )

    print("=== INTENT CONTRACT ===")
    print(intent_response.output_text)
    planner_input = f"""
    ORIGINAL USER REQUEST:
    {user_request}

    ORIGINAL INTENT CONTRACT:
    {intent_response.output_text}

    Create a proposed plan for accomplishing the user's request.
    """
    # 2. Generate a practical plan for accomplishing the request
    planner_response = openai_client.responses.create(
        input=[
            {
                "role": "user",
                "content": planner_input
            }
        ],
        extra_body={
            "agent_reference": {
                "name": "planner-agent",
                "version": "3",
                "type": "agent_reference"
            }
        },
    )

    print("\n=== PROPOSED PLAN ===")
    print(planner_response.output_text)
    diff_input = f"""
    ORIGINAL USER REQUEST:
    {user_request}

    ORIGINAL INTENT CONTRACT:
    {intent_response.output_text}

    PROPOSED PLAN:
    {planner_response.output_text}

    Compare the proposed plan against the original intent contract.
    """
    # 3. Compare proposed actions against the original intent
    diff_response = openai_client.responses.create(
        input=[
            {
                "role": "user",
                "content": diff_input
            }
        ],
        extra_body={
            "agent_reference": {
                "name": "intent-diff-agent",
                "version": "3",
                "type": "agent_reference"
            }
        },
    )

    print("\n=== INTENT DIFF ===")
    print(diff_response.output_text)