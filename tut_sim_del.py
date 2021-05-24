import pandas
from time import time

import cobra.test
from cobra.flux_analysis import (single_gene_deletion, single_reaction_deletion, double_gene_deletion, double_reaction_deletion)

cobra_model = cobra.test.create_test_model("textbook")
ecoli_model = cobra.test.create_test_model("ecoli")

#If a reaction is not allowed to have any flux
print('complete model: ', cobra_model.optimize())
with cobra_model:
    cobra_model.reactions.PFK.knock_out()
    print('pfk knocked out', cobra_model.optimize())

#Gene knockout
print('complete model: ', cobra_model.optimize())
with cobra_model:
    cobra_model.genes.b1723.knock_out()
    print('pfkA knocked out', cobra_model.optimize())
    cobra_model.genes.b3916.knock_out()
    print('pfkB knocked out', cobra_model.optimize())

#Perform all single gene deletions on a model
deletion_results = single_gene_deletion(cobra_model)

#And for only a subset
single_gene_deletion(cobra_model, cobra_model.genes[:20])

#and reactions
single_reaction_deletion(cobra_model, cobra_model.reactions[:20])

#double deletions
double_gene_deletion(cobra_model, cobra_model.genes[-5:]).round(4)

#Default behaviour of double delete uses multiprocessing if multi cores available. Can be manually specified - disables use of multiprocessing library, helps for debugging

start = time()  # start timer()
double_gene_deletion(
    ecoli_model, ecoli_model.genes[:25], processes=2)
t1 = time() - start
print("Double gene deletions for 200 genes completed in "
      "%.2f sec with 2 cores" % t1)

start = time()  # start timer()
double_gene_deletion(
    ecoli_model, ecoli_model.genes[:25], processes=1)
t2 = time() - start
print("Double gene deletions for 200 genes completed in "
      "%.2f sec with 1 core" % t2)

print("Speedup of %.2fx" % (t2 / t1))

#double deletion reaction
double_reaction_deletion(cobra_model, cobra_model.reactions[2:7]).round(4)

#Accessing all rresults can use knockout indexer.
single = single_reaction_deletion(cobra_model)
double = double_reaction_deletion(cobra_model)

print(single.knockout["ATPM"])
print(double.knockout[{"ATPM", "TKT1"}])

atpm = cobra_model.reactions.ATPM
tkt1 = cobra_model.reactions.TKT1
pfk = cobra_model.reactions.PFK

print(single.knockout[atpm, tkt1, pfk])
print(double.knockout[{atpm, tkt1}, {atpm, pfk}, {atpm}])
