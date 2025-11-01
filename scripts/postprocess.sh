#!/bin/bash

python3.9 postprocess_d4j.py --gen_test_dir /root/libro/data/Defects4J/gen_tests_gpt-4o/  --all --exp_name gpt-4o_n10 --projects Lang
python3.9 postprocess_d4j.py --gen_test_dir /root/libro/data/Defects4J/gen_tests_Meta-Llama-3-8B-Instruct --all --exp_name llama3-8b_n10 --projects Lang
python3.9 postprocess_d4j.py --gen_test_dir /root/libro/data/Defects4J/gen_tests_Meta-Llama-3.1-8B-Instruct --all --exp_name llama3.1-8b_n10 --projects Lang 
python3.9 postprocess_d4j.py --gen_test_dir /root/libro/data/Defects4J/gen_tests_Mistral-Nemo-Instruct-2407 --all --exp_name mistral-nemo-12b_n10 --projects Lang
python3.9 postprocess_d4j.py --gen_test_dir /root/libro/data/Defects4J/gen_tests_Qwen2.5-Coder-7B-Instruct --all --exp_name qwen2.5-coder-7b_n10 --projects Lang
python3.9 postprocess_d4j.py --gen_test_dir /root/libro/data/Defects4J/gen_tests_phi-4 --all --exp_name phi4-14b_n10 --projects Lang
