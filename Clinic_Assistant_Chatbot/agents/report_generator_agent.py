from prompts.agent_prompt import REPORT_PROMPT
from llm import get_llm

llm = get_llm()


def report_agent(state):
    clinical_data = state.clinical_data

    schema_str = clinical_data.model_dump()

    prompt = REPORT_PROMPT.format(schema=schema_str)

    response = llm.invoke([
        {"role": "user", "content": prompt}
    ])

    return {
        "final_report": response.content.strip()
    }
