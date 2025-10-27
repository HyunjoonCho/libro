#!/bin/bash

BUG_REPORT_PATH="/root/libro/data/Defects4J/bug_report"
OUTPUT_PREFIX="/root/libro/data/Defects4J/gen_tests_"

MODELS=(
    "OpenAI/gpt-4o"
    "meta-llama/Meta-Llama-3-8B-Instruct"
    "meta-llama/Meta-Llama-3.1-8B-Instruct"
    "mistralai/Mistral-Nemo-Instruct-2407"
    "Qwen/Qwen2.5-Coder-7B-Instruct"
    "microsoft/phi-4"
)

for MODEL in "${MODELS[@]}"; do
    python3.9 llm_repeat_query.py --model "$MODEL" -b "$BUG_REPORT_PATH" -o "$OUTPUT_PREFIX" -p Chart Lang Time Math
done
