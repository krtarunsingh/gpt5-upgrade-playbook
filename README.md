# GPT‑5 Upgrade Playbook — Demo & Evals

A tiny, reproducible repo you can clone to try **GPT‑5** quickly and compare settings like `reasoning.effort` and `verbosity`.  
Everything here is **original** and licensed under **MIT** for the code.

> **Requirements**: Python 3.9+, an OpenAI API key (set `OPENAI_API_KEY` in your environment).

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

export OPENAI_API_KEY=YOUR_KEY_HERE   # Windows PowerShell: $Env:OPENAI_API_KEY="..."
python src/gpt5_upgrade_demo.py --file examples/foo.py --effort low --verbosity low
```

You should see a **JSON** summary describing the refactor and tests added.

## Compare settings

```bash
python src/bench/benchmark.py --file examples/foo.py --tries 2
```

This logs latency, tokens, and simple quality proxies for different combos:
- `effort`: minimal | low | medium | high
- `verbosity`: low | medium | high

Results are written to `runs/last_run.json` and a CSV for quick charts.

## Files

- `src/gpt5_upgrade_demo.py` — one-shot refactor + tests with **Structured Outputs** (safe JSON).
- `src/bench/benchmark.py` — quick harness to compare model settings.
- `examples/foo.py` — small sample function to refactor.
- `tests/test_examples.py` — tiny pytest to show how you'd confirm changes.
- `requirements.txt` — conservative deps.
- `LICENSE` — MIT (code).

## Notes

- This repo **does not** include any third‑party copyrighted content.  
- Model names and parameters are configurable via CLI flags and env vars.

---

**Author**: Tarun.  
**Disclaimer**: Not affiliated with OpenAI. See OpenAI docs for latest capabilities and pricing.
