#!/usr/bin/env python
# coding: utf-8

import os
import json
import argparse

from llm_api import model_is_chat, query_llm
from llm_query import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dataset', default='d4j', help='dataset to use: d4j or ghrb')
    parser.add_argument('-p', '--projects', nargs='*') 
    parser.add_argument('-b', '--bug_report_path', default='/root/libro/data/Defects4J/bug_report')
    parser.add_argument('--use_html', action='store_true')
    parser.add_argument('--use_plain_text', action='store_true')
    parser.add_argument('--save_prompt', action='store_true')
    parser.add_argument('--template', default='2example_chat')
    parser.add_argument('--model', default='OpenAI/gpt-4o')
    parser.add_argument('-n', '--num_tests', default=10)
    parser.add_argument('-o', '--output_prefix', default='/root/libro/data/Defects4J/gen_tests_')
    parser.add_argument('--prompt_out', default=None)
    args = parser.parse_args()

    if args.dataset == 'ghrb':
        BR_DIR = llm_exp_config['bug_report_dir']['ghrb'] # FIXME: will not be updated for GHRB properly

    model_short = args.model.split('/')[-1]
    output_dir = f'{args.output_prefix}{model_short}'
    os.makedirs(output_dir, exist_ok=True)

    project_list = args.projects

    for file in sorted(os.listdir(args.bug_report_path)):
        project, bug_id = tuple(file.split('.')[0].split('-'))
        if project_list and project not in project_list:
            continue
        print(f'p={project}, v={bug_id}')

        for i in range(1, args.num_tests + 1):
            test_path = f'{output_dir}/{project}_{bug_id}_n{i}.txt'
            cost_path = f'{output_dir}/{project}_{bug_id}_n{i}_cost.json'
            if os.path.exists(test_path) and os.path.exists(cost_path):
                continue

            gen_test, cost = query_llm_for_gentest(
                project, bug_id, 
                args.model,
                args.template, 
                use_plain_text=args.use_plain_text, 
                use_html=args.use_html,
                save_prompt=args.save_prompt, 
                prompt_save_path=args.prompt_out
            )
            with open(test_path, 'w') as f:
                f.write(gen_test)

            with open(cost_path, 'w') as f:
                json.dump(cost, f, indent=2)
