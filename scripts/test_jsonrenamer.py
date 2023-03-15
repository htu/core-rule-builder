from jsonrenamer.json_file_renamer import JsonFileRenamer
repo_dir = "/Volumes/HiMacData/GitHub/repo"
src_dir = repo_dir + "/rule-transformations/data/output/json_rules"
renamer = JsonFileRenamer(src_dir,
                          "./data/output/json_rules1")
renamer.rename_files()
