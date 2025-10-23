"""
Configuration for LLM test generator w/ different datasets.
"""

llm_exp_config = {
    'bug_report_dir': {
        'ghrb': '/root/libro/data/GHRB/bug_report/',
        'd4j': '/root/libro/data/Defects4J/bug_report/'
    },
    'template_dir': '/root/libro/data/prompt_templates/',
    'gen_tests_dir': {
        'ghrb': '/root/libro/data/GHRB/gen_tests/',
        'd4j': '/root/libro/data/Defects4J/gen_tests/'
    }
}
