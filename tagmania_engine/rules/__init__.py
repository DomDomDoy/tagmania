from utils import load
directory = 'libs/tagmania_engine/rules'
rule_files = ['rule_set1']
rule_dict = {rule: load(directory, rule) for rule in rule_files}
