import cobra.test
import os
from os.path import join

data_dir = cobra.test.data_dir

#Many provided test models

print("mini test files: ")
print(", ".join(i for i in os.listdir(data_dir) if i.startswith("mini")))

textbook_model = cobra.test.create_test_model("textbook")
ecoli_model = cobra.test.create_test_model("ecoli")
salmonella_model = cobra.test.create_test_model("salmonella")

## SBML
# The Systems Biology Markup Language is an XML-based standard format for 
# distributing models which has support for COBRA models through the 
# FBC extension version 2.

#Cobrapy has native support for reading and writing SBML with FBCv2. 
# Please note that all id’s in the model must conform to the 
# SBML SID requirements in order to generate a valid SBML file.

cobra.io.read_sbml_model(join(data_dir, "mini_fbc2.xml"))
cobra.io.write_sbml_model(join(textbook_model, "test_fbc2.xml"))