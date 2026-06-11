import json

log_file = "/Users/jc/.gemini/antigravity-ide/brain/b461fb36-0010-4466-bf32-60608ca319ec/.system_generated/logs/transcript.jsonl"
html_file = "/Users/jc/Documents/Stock-ledger/index.html"

# Reset to base commit first to get a clean slate
import subprocess
subprocess.run(["git", "checkout", "index.html"])

with open(html_file, "r") as f:
    content = f.read()

count = 0
with open(log_file, "r") as f:
    for line in f:
        try:
            step = json.loads(line, strict=False)
            step_idx = step.get("step_index", 999999)
            if step_idx > 365:
                continue

            if "tool_calls" in step:
                for call in step["tool_calls"]:
                    name = call.get("name")
                    if name in ["replace_file_content", "multi_replace_file_content"]:
                        args = call.get("args", {})
                        target_file = json.loads(args.get("TargetFile", '""'), strict=False)
                        if target_file == html_file:
                            if name == "replace_file_content":
                                target = json.loads(args.get("TargetContent", '""'), strict=False)
                                replacement = json.loads(args.get("ReplacementContent", '""'), strict=False)
                                if target and target in content:
                                    content = content.replace(target, replacement)
                                    count += 1
                                    print(f"Applied replace_file_content at step {step_idx}")
                            elif name == "multi_replace_file_content":
                                chunks = json.loads(args.get("ReplacementChunks", "[]"), strict=False)
                                for idx, chunk in enumerate(chunks):
                                    target = chunk.get("TargetContent")
                                    replacement = chunk.get("ReplacementContent")
                                    if target and target in content:
                                        content = content.replace(target, replacement)
                                        count += 1
                                        print(f"Applied multi chunk {idx} at step {step_idx}")
        except Exception as e:
            pass

with open("index.html", "w") as f:
    f.write(content)

print(f"Recovered {count} chunks to step 365!")
