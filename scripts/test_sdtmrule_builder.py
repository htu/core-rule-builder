# Purpose: Process all the rules from a df_data 
# -----------------------------------------------------------------------------
# History: MM/DD/YYYY (developer) - description
#   03/14/2023 (htu) - ported from proc_rules_sdtm as proc_sdtm_rules module
# 

from rulebuilder.sdtmrulebuilder import SDTMRuleBuilder
repo_dir = "/Volumes/HiMacData/GitHub/repo"
src_dir = repo_dir + "/rule-transformations/data/output/json_rules"
sdtm_rb = SDTMRuleBuilder()
sdtm_rb.build()
