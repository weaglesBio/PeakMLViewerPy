import cobra.test
model = cobra.test.create_test_model("textbook")

#Returns a Solution object
solution = model.optimize()
print(solution)

# objective_value
# status - linear programming solver status
# fluxes - a pandas series with flux indexed by reaction identifier. 
#           The flux for a reaction variable is the difference of the primal valeus for the forward and reverse reaction variables.
# shadow_prices - a pandas series with shadow price indexed by the metabolite identifier

solution.objective_value

# Performance bottleneck is collection of all values (solver fast)
# For only the flux value of a single reaction of the objective, faster to use.

model.slim_optimize()

#Quick representation of model behaviour
model.summary()

#Input-output behaviour of individual metabolites
model.metabolites.nadh_c.summary()

#Details of main energy production and consumption reactions
model.metabolites.atp_c.summary()

#Objective function determined from the objective_coefficient attribute of the objective reaction(s).
#Generally "biomass" function which describes the composition of metabolites which make up a cell is used.
biomass_rxn = model.reactions.get_by_id("Biomass_Ecoli_core")

#Get all
from cobra.util.solver import linear_reaction_coefficients
linear_reaction_coefficients(model)

#OF can be changed by assigning Model.objective - can be reaction object, its name, or a dict of {Reaction: objective_coefficient}
model.objective = "ATPM"

#Set upper bound to 1000 to get actual optimal value
model.reactions.get_by_id("ATPM").upper_bound = 1000
linear_reaction_coefficients(model)

model.optimize().objective_value
# More complicated objectives involving quadratic terms are possible.

#FBA not always unique solution as multiple flux states can achieve the same optimum.
#Flux variability analysis (FVA) finds the range of each metabolic flux at the optimum.

from cobra.flux_analysis import flux_variability_analysis
flux_variability_analysis(model, model.reactions[:10])

#Get flux ranges for reactions at 90% optimality
cobra.flux_analysis.flux_variability_analysis(model, model.reactions[:10], fraction_of_optimum=0.9)

#FVA may contain loops, high absolute flux values that can only be high if they are allowed to participate in loops. (mathematical - cannot happen in vivo)
loop_reactions = [model.reactions.FRD7, model.reactions.SUCDi]
flux_variability_analysis(model, reaction_list = loop_reactions, loopless = True)

#Can be embedded in summary method calls
model.optimize()
model.summary(fva=0.95)
model.metabolites.pyr_c.summary(fva=0.95)
#values are reported as a center point +/- the reange of the FVA solution from min max.

# Parsimonious FBA (pFBA) - finds flux distribution which gives the optimal growth but minimizes the total sum of flux. 
model.objective = 'Biomass_Ecoli_core'
fba_solution = model.optimize()
pfba_solution = cobra.flux_analysis.pfba(model)

abs(fba_solution.fluxes["Biomass_Ecoli_core"] - pfba_solution.fluxes["Biomass_Ecoli_core"])

#Geometric FBA - finds unique optimal flux distribution which is central to the range of possible fluxes
geometric_fba_sol = cobra.flux_analysis.geometric_fba(model)
geometric_fba_sol