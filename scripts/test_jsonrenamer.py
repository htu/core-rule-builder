from jsonrenamer.json_file_renamer import JsonFileRenamer
repo_dir = "/Volumes/HiMacData/GitHub/data"
src_dir = repo_dir + "/rule-transformations/data/output/json_rules"
tgt_dir = repo_dir + "/core-rule-builder/data/output/json_rules1"
renamer = JsonFileRenamer(src_dir,tgt_dir)
renamer.rename_files()
