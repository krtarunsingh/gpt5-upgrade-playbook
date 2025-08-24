import argparse, json, os, sys
from typing import Dict, Any
from pydantic import BaseModel, Field
from openai import OpenAI

class RefactorReport(BaseModel):
    refactor_summary: str = Field(..., description="Human-readable summary of changes")
    changed_files: list[str] = Field(..., description="List of files changed or created")
    tests_added: int = Field(..., description="How many new tests were added")
    next_steps: list[str] = Field(..., description="Bulleted next steps")

SCHEMA = {
  "type": "object",
  "properties": {
    "refactor_summary": {"type": "string"},
    "changed_files": {"type": "array", "items": {"type":"string"}},
    "tests_added": {"type": "integer"},
    "next_steps": {"type": "array", "items": {"type":"string"}}
  },
  "required": ["refactor_summary","changed_files","tests_added","next_steps"],
  "additionalProperties": False
}

SYSTEM_PROMPT = (
  "You are a senior Python engineer. "
  "Refactor clearly, keep behavior the same, and propose pytest tests. "
  "Return ONLY JSON matching the schema."
)

def run_gpt5(file_text: str, effort: str, verbosity: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.responses.create(
        model=os.getenv("MODEL_NAME","gpt-5"),
        reasoning={"effort": effort},     # minimal | low | medium | high
        verbosity=verbosity,              # low | medium | high
        input=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":[
                {"type":"text","text":"Refactor this code and propose pytest tests."},
                {"type":"input_text","text":file_text}
            ]}
        ],
        text={"format":"json_schema","schema":SCHEMA}
    )
    return json.loads(resp.output_text)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True, help="Path to a Python file to refactor")
    ap.add_argument("--effort", default="low", choices=["minimal","low","medium","high"])
    ap.add_argument("--verbosity", default="low", choices=["low","medium","high"])
    args = ap.parse_args()

    with open(args.file, "r", encoding="utf-8") as f:
        code = f.read()

    data = run_gpt5(code, args.effort, args.verbosity)
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
