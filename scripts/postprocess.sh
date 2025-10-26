#!/bin/bash

python3.9 postprocess_d4j.py --gen_test_dir /root/libro/data/Defects4J/gen_tests_gpt-4o/  --all --exp_name gpt-4o_n10
python3.9 postprocess_d4j.py --gen_test_dir /root/libro/data/Defects4J/gen_tests_Meta-Llama-3-8B-Instruct --all --exp_name llama3-8b_n10 
python3.9 postprocess_d4j.py --gen_test_dir /root/libro/data/Defects4J/gen_tests_Meta-Llama-3.1-8B-Instruct --all --exp_name llama3.1-8b_n10 
