import json
from prompts.agent_prompt import EXTRACTION_PROMPT
from llm import get_llm
from state import ClinicalSchema

llm = get_llm()


def extractor_agent(state):
    messages = state.messages

    conversation = "\n".join(
        [f"{m['role']}: {m['content']}" for m in messages]
    )

    prompt = EXTRACTION_PROMPT.format(conversation=conversation)

    response = llm.invoke([
        {"role": "user", "content": prompt}
    ])

    try:
        data = json.loads(response.content)

        state.clinical_data = ClinicalSchema(**data)

    except Exception as e:
        pass

    return state
