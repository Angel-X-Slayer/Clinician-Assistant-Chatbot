from prompts.agent_prompt import INTAKE_SYSTEM_PROMPT
from llm import get_llm


llm = get_llm()


def intake_agent(state):
    stage = state.stage

    stage_instruction = {
        "cc": "Ask about the chief complaint (main problem).",
        "hpi": "Ask details about the illness (duration, severity, symptoms).",
        "pmh": "Ask about past medical history.",
        "ros": "Ask review of systems (other symptoms).",
        "done": "Stop asking questions."
    }
    messages = state.messages

    system_prompt = f"""
    {INTAKE_SYSTEM_PROMPT}

    Current stage: {stage}

    Instruction:
    {stage_instruction.get(stage)}

    RULES:
    - Ask ONE question only
    - Be concise
    """

    response = llm.invoke([
        {"role": "system", "content": system_prompt},
        *messages
    ])

    state.messages.append({"role": "assistant", "content": response.content})
    return state
