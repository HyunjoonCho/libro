import json
import os

from llm_query import make_messages_from_file, BR_DIR, TEMPLATE_DIR

# Assuming all models are using chat 
if __name__ == "__main__":
    template = '2example_chat'
    prompts = dict()

    for file in sorted(os.listdir(BR_DIR)):
        project, bug_id = tuple(file.split('.')[0].split('-'))
        with open(BR_DIR + project + '-' + str(bug_id) + '.json') as f:
            br = json.load(f)

        prompt, stop = make_messages_from_file(
            br['title'], br['description'],
            template_file=TEMPLATE_DIR+f'{template}.json')
        key = f"{project}_{bug_id}"
        prompts[key] = prompt
    
    with open('../data/Defects4J/prompts.json', 'w') as f:
        json.dump(prompts, f, indent=2)
