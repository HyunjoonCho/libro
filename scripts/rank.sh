#!/bin/bash

python selection_and_ranking.py -d Defects4J -f ../results/gpt-4o_n10.json -g ../data/Defects4J/gen_tests_gpt-4o -p _gpt-4o --projects Chart Lang Time Math
python selection_and_ranking.py -d Defects4J -f ../results/llama3-8b_n10.json -g ../data/Defects4J/gen_tests_Meta-Llama-3-8B-Instruct -p _llama3-8b --projects Chart Lang Time Math
python selection_and_ranking.py -d Defects4J -f ../results/llama3.1-8b_n10.json -g ../data/Defects4J/gen_tests_Meta-Llama-3.1-8B-Instruct -p _llama3.1-8b --projects Chart Lang Time Math
python selection_and_ranking.py -d Defects4J -f ../results/mistral-nemo-12b_n10.json -g ../data/Defects4J/gen_tests_Mistral-Nemo-Instruct-2407 -p _mistral-nemo-12b --projects Chart Lang Time Math
python selection_and_ranking.py -d Defects4J -f ../results/qwen2.5-coder-7b_n10.json -g ../data/Defects4J/gen_tests_Qwen2.5-Coder-7B-Instruct -p _qwen2.5-coder-7b --projects Chart Lang Time Math
python selection_and_ranking.py -d Defects4J -f ../results/phi4-14b_n10.json -g ../data/Defects4J/gen_tests_phi-4 -p _phi4-14b --projects Chart Lang Time Math
