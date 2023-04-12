import os

# os.system("cp test.xml  MCSSim/generator/model_builder")
# os.system("cd ./MCSSim/generator/model_builder; ./model_builder test.xml > result.txt; cd -")
# os.system("cp ./MCSSim/generator/model_builder/result.txt  .")

os.system("cp test_nvp.xml  MCSSim/generator/model_builder") 
os.system("cd ./MCSSim/generator/model_builder; ./model_builder test_nvp.xml > result_nvp.txt; cd -")
os.system("cp ./MCSSim/generator/model_builder/result_nvp.txt .") 
