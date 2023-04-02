from jsonrenamer.json_file_renamer import JsonFileRenamer

json_folder = "/Volumes/HiMacData/GitHub/data/core-rule-builder/data/output/json_rules"
xlsx_folder = "/Volumes/HiMacData/GitHub/data/core-rule-builder/data/target"
xlsx_file   = "current_rules.xlsx"

renamer = JsonFileRenamer(json_folder, xlsx_folder)
# renamer.extract_rules(xlsx_file)
renamer.write_rules2xlsx(xlsx_file)
