# Clinician Assistant Chatbot

An intelligent clinical intake assistant powered by LLMs that conducts structured patient interviews, extracts medical information, and generates clinical reports.

## Overview

The Clinician Assistant Chatbot automates the initial patient intake process by:

- Conducting a guided interview to collect chief complaint and medical history
- Extracting and structuring clinical information from conversations
- Generating comprehensive clinical reports in a professional format

This system uses a multi-agent architecture built with **LangGraph** to orchestrate different stages of patient intake, ensuring consistent and accurate data collection.

## Features

- **Guided Clinical Interview**: Structured conversation flow through multiple stages (CC → HPI → PMH → ROS)
- **Information Extraction**: Automatically extracts and structures medical data into a standardized schema
- **Report Generation**: Creates professional clinical reports from collected information
- **Dual Interface**: Both REST API and interactive CLI
- **State Management**: Maintains conversation context and extracted data throughout the session
- **LLM-Powered**: Uses Groq's fast inference for real-time responses

## Architecture

### Multi-Agent Workflow

The system uses a **LangGraph state machine** with three sequential agents:

```
START
  ↓
[Intake Agent] - Conducts guided clinical interview
  ↓
[Extractor Agent] - Parses conversation & extracts structured data
  ↓
[Report Generator] - Creates clinical report from extracted data
  ↓
END
```

### Key Components

| Component | Purpose |
|-----------|---------|
| **Intake Agent** | Asks structured questions based on clinical intake stages |
| **Extractor Agent** | Parses conversation and extracts medical information as JSON |
| **Report Generator** | Formats extracted data into a professional clinical report |
| **GraphState** | Maintains messages, clinical data, and interview stage |

## Installation

### Prerequisites

- Python 3.11+
- pip or conda
- Groq API key ([Get one free](https://console.groq.com))

### Setup

1. **Clone or extract the project**

   ```bash
   cd Clinic_Assistant_Chatbot
   ```

2. **Create a virtual environment** (optional but recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the project root:

   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

## Configuration

### Environment Variables

```env
GROQ_API_KEY          # Required: Groq API key for LLM access
```

### LLM Configuration

The chatbot uses Groq's `qwen/qwen3-32b` model by default. To change the model:

1. Edit [llm.py](llm.py):

   ```python
   def get_llm():
       return ChatGroq(model="your-model-name",
                       api_key=GROQ_API_KEY,
                       temperature=0.1)
   ```

### Interview Stages

Modify stage instructions in [agents/intake_agent.py](agents/intake_agent.py):

```python
stage_instruction = {
    "cc": "Ask about the chief complaint (main problem).",
    "hpi": "Ask details about the illness (duration, severity, symptoms).",
    "pmh": "Ask about past medical history.",
    "ros": "Ask review of systems (other symptoms).",
    "done": "Stop asking questions."
}
```

## Usage

### CLI Mode (Interactive)

Run the chatbot directly for an interactive conversation:

```bash
python main.py
```

Example interaction:

```
Chatbot is running. what brings you here today? (type 'exit' to quit)
You: I have a headache for 3 days
Assistant: When did the headache start, and how would you describe the pain (sharp, dull, throbbing)?
You: It started 3 days ago, feels like a dull pressure
Assistant: ...
```

### REST API Mode

Start the FastAPI server:

```bash
python main.py  # Runs the CLI by default
# OR
uvicorn main:app --host 0.0.0.0 --port 8000  # For API mode
```

#### API Endpoint

**POST** `/StartChat`

Send user message and get chatbot response:

```bash
curl -X POST "http://localhost:8000/StartChat?query=I%20have%20a%20headache"
```

**Response:**

```json
{
  "response": "When did the headache start? How long have you had it?"
}
```

## Project Structure

```
Clinic_Assistant_Chatbot/
├── main.py                    # FastAPI app & CLI entry point
├── graph.py                   # LangGraph workflow definition
├── state.py                   # Pydantic state models
├── config.py                  # Configuration & environment loading
├── llm.py                     # LLM initialization (Groq)
├── agents/
│   ├── intake_agent.py       # Clinical interview agent
│   ├── extractor_agent.py    # Information extraction agent
│   └── report_generator_agent.py  # Report generation agent
├── prompts/
│   └── agent_prompt.py       # System prompts for all agents
├── requirements.txt           # Python dependencies
├── .env                      # Environment variables (not in repo)
└── README.md                 # This file
```

## Data Models

### GraphState

The shared state maintained throughout the workflow:

```python
class GraphState(BaseModel):
    messages: List[Dict[str, str]]  # Conversation history
    clinical_data: ClinicalSchema   # Extracted structured data
    stage: str                       # Current interview stage
```

### ClinicalSchema

Structured clinical information extracted from conversation:

```python
class ClinicalSchema(BaseModel):
    chief_complaint: str              # Main reason for visit
    symptoms: List[str]               # Associated symptoms
    duration: str                      # How long symptoms present
    severity: str                      # Symptom severity level
    associated_symptoms: List[str]     # Related symptoms
    negatives: List[str]               # Negative findings
    past_medical_history: str          # Previous medical conditions
    surgeries: List[str]               # Previous surgeries
    hospitalizations: List[str]        # Hospital admissions
```

## Workflow Details

### 1. Intake Agent

- **Input**: User message & current conversation state
- **Process**: Constructs dynamic prompts based on interview stage
- **Output**: Clinical question appended to message history
- **Stages**: CC → HPI → PMH → ROS → Done

### 2. Extractor Agent

- **Input**: Full conversation history
- **Process**: Prompts LLM to extract structured medical information
- **Output**: Parsed JSON conforming to `ClinicalSchema`
- **Error Handling**: Silently skips extraction on JSON parse errors

### 3. Report Generator

- **Input**: Extracted clinical data
- **Process**: Formats data into professional clinical narrative
- **Output**: Structured clinical report added to messages

## Dependencies

Key packages:

- **fastapi** - REST API framework
- **pydantic** - Data validation & serialization
- **langchain** - LLM framework
- **langgraph** - Agent orchestration & state management
- **langchain-groq** - Groq LLM integration
- **uvicorn** - ASGI server for FastAPI

See [requirements.txt](requirements.txt) for complete list.

## Troubleshooting

### No Output After Running

**Check:**

1. `.env` file exists with valid `GROQ_API_KEY`
2. All agents are returning state properly
3. Network connection to Groq API is available
4. LLM responses are being appended to messages

### API Not Responding

```bash
# Check if server is running
netstat -ano | findstr :8000  # Windows
lsof -i :8000                  # macOS/Linux

# Kill process if needed and restart
python main.py
```

### LLM Rate Limiting

If you get rate limit errors, add retry logic or increase temperature for caching.

## Future Enhancements

- [ ] Database persistence for patient records
- [ ] Multi-language support
- [ ] Advanced NLP for symptom severity classification
- [ ] Integration with EHR systems
- [ ] User authentication & authorization
- [ ] Session history & patient follow-ups

## License

[Your License Here]

## Contact

For issues or questions, please open an issue in this repository.

---

**Built with LangGraph & Groq LLM**
