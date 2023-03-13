from .jsonrenamer.json_file_renamer import JsonFileRenamer

renamer = JsonFileRenamer("./data/output/json_rules", "./data/output/json_rules3")
renamer.rename_files()
