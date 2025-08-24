import argparse, json, os, time, itertools, statistics, pathlib
from openai import OpenAI
from rich.console import Console
from rich.table import Table

console = Console()

def call(model, effort, verbosity, payload):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    t0 = time.time()
    r = client.responses.create(
        model=model,
        reasoning={"effort": effort},
        verbosity=verbosity,
        input=payload
    )
    dt = time.time() - t0
    # Token usage keys can vary; guard just in case
    usage = getattr(r, "usage", None)
    tokens = getattr(usage, "total_tokens", None) if usage else None
    return dt, tokens

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--model", default=os.getenv("MODEL_NAME","gpt-5"))
    ap.add_argument("--tries", type=int, default=1)
    args = ap.parse_args()

    code = pathlib.Path(args.file).read_text(encoding="utf-8")
    payload = [{"role":"user","content":"Explain the following function and improve it." + code}]

    efforts = ["minimal","low","medium","high"]
    verbosities = ["low","medium","high"]

    rows = []
    for eff, ver in itertools.product(efforts, verbosities):
        durs, toks = [], []
        for _ in range(args.tries):
            dt, tokens = call(args.model, eff, ver, payload)
            durs.append(dt)
            if tokens is not None: toks.append(tokens)
        rows.append({
            "effort": eff,
            "verbosity": ver,
            "latency_avg_s": round(statistics.mean(durs), 2),
            "tokens_avg": round(statistics.mean(toks), 1) if toks else None
        })

    out = {"results": rows, "model": args.model, "file": args.file}
    os.makedirs("runs", exist_ok=True)
    with open("runs/last_run.json","w",encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    table = Table(title="GPT-5 benchmark (toy)")
    table.add_column("effort"); table.add_column("verbosity")
    table.add_column("latency_avg_s"); table.add_column("tokens_avg")
    for r in rows:
        table.add_row(r["effort"], r["verbosity"], str(r["latency_avg_s"]), str(r["tokens_avg"]))
    console.print(table)

if __name__ == "__main__":
    main()
