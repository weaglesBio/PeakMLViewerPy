from cobra import Model, Reaction, Metabolite

# It is highly recommended that the ids for reactions, metabolites and genes are valid 
# SBML identifiers (SId). SId is a data type derived from the basic XML typestring, but 
# with restrictions about the characters permitted and the sequences in which those 
# characters may appear.

# letter   ::=   ’a’..’z’,’A’..’Z’
# digit    ::=   ’0’..’9’
# idChar   ::=   letter | digit | ’_’
# SId      ::=   ( letter | ’_’ ) idChar*

# The main limitation is that ids cannot start with numbers. Using SIds allows serialization 
# to SBML. In addition features such as code completion and object access via the dot syntax 
# will work in cobrapy.

#Create model
model = Model('example_model')

#Create reaction
reaction = Reaction('R_3OAS140')
reaction.name = '3 oxoacyl acyl carrier protein synthase n C140'
reaction.subsystem = 'Cell Envelope Biosynthesis'
reaction.lower_bound = 0 #default
reaction.upper_bound = 1000 #default

#Create metabolites
#Can be extracted from existing model using Model.get_by_id
ACP_c = Metabolite(
    'ACP_c',
    formula = 'C11H21N2O7PRS',
    name = 'acyl-carrier-protein',
    compartment = 'c')

omrsACP_c = Metabolite(
    'M3omrsACP_c',
    formula = 'C25H45N2O9PRS',
    name = '3-Oxotetradecanoyl-acyl-carrier-protein',
    compartment = 'c')

co2_c = Metabolite(
    'co2_c',
    formula = 'CO2',
    name = 'CO2',
    compartment = 'c')

malACP_c = Metabolite(
    'malACP_c',
    formula = 'C14H22N2O10PRS',
    name = 'Malonyl-acyl-carrier-protein',
    compartment = 'c')

h_c = Metabolite(
    'h_c',
    formula = 'H',
    name = 'H',
    compartment = 'c')

ddcaACP_c = Metabolite(
    'ddcaACP_c',
    formula = 'C23H43N2O8PRS',
    name = 'Dodecanoyl-ACP-n-C120ACP',
    compartment = 'c')

#Adding metabolites to a reaction uses a dictionary of the metabolites and their stoichiometric coefficients (all at once or one at a time)

reaction.add_metabolites({
    malACP_c: -1.0,
    h_c: -1.0,
    ddcaACP_c: -1.0,
    co2_c: 1.0,
    ACP_c: 1.0,
    omrsACP_c: 1.0
})

#Gives a string representation of the reaction
reaction.reaction

#Gene reaction rule is a boolean representation of the gene requirements for this reaction to be active. 
#Assigning the gene reaction rule string, automatically creates the corresponding gene objects.

reaction.gene_reaction_rule = '( STM2378 or STM1197 )'
reaction.genes

#Model is currently empty
print(f'{len(model.reactions)} reactions initially')
print(f'{len(model.metabolites)} metabolites initially')
print(f'{len(model.genes)} genes initially')

#Adding the reaction to the model, adds all associated metabolites and genes.
model.add_reactions([reaction])

print(f'{len(model.reactions)} reactions')
print(f'{len(model.metabolites)} metabolites')
print(f'{len(model.genes)} genes')

#Iterating through the model to observe the contents
print("Reactions")
print("---------")
for x in model.reactions:
    print("%s : %s" % (x.id, x.reaction))

print("")
print("Metabolites")
print("-----------")
for x in model.metabolites:
    print("%9s : %s" % (x.id, x.formula))

print("")
print("Genes")
print("-----")
for x in model.genes:
    associated_ids = (i.id for i in x.reactions)
    print("%s is associated with reactions: %s" %
            (x.id, "{" + ", ".join(associated_ids) + "}"))


#Setting the objective at the model
#For this it is the maximization of the flux in the single reaction
#Achieved by assigning the reaction's identifier to the objective property of the model.

model.objective = 'R_3OAS140'

#Created objective is a symbolic algebraic expression and we can examine it by printing it.
print(model.objective.expression)
print(model.objective.direction)

#Shows solver will maximize the flux in the forward direction.

#Model can be validated and exported to SBML
import tempfile
from pprint import pprint
from cobra.io import write_sbml_model, validate_sbml_model
with tempfile.NamedTemporaryFile(suffix='.xml') as f_sbml:
    print(f_sbml.name)
    print(model)
    #test filepath
    fp = "C:\\Users\\willi\\OneDrive\\University\\RP2\\example_mod.xml"
    write_sbml_model(model, filename=fp)
    #write_sbml_model(model, filename=f_sbml.name)
    report = validate_sbml_model(filename=fp)

pprint(report)

#Boundary reactions
#They are unbalanced pseudoreactions - fufill function for adding or removing metabolites - not based on real biology.
#Exchange - reversible that adds/removes an extracellular metabolite from the extracellular compartment
#Demand - irreversible - consumes intracellular metabolite 
#Sink - reversible that adds/removes an intracellular metabolite

print("exchanges", model.exchanges)
print("demands", model.demands)
print("sinks", model.sinks)

# Boundary reactions are defined on metabolites.(first add metabolites, then boundary reactions)

model.add_metabolites([
    Metabolite(
    'glycogen_c',
    name='glycogen',
    compartment='c' #cytosolic
    ),
    Metabolite(
    'co2_e',
    name='CO2',
    compartment='e' #external
    ),
])

model.add_boundary(model.metabolites.get_by_id("co2_e"), type="exchange")

model.add_boundary(model.metabolites.get_by_id("glycogen_c"), type="sink")

print("exchanges", model.exchanges)
print("demands", model.demands)
print("sinks", model.sinks)

#Information on all boundary reactions.
model.boundary

#Get all metabolic reactions.
set(model.reactions) - set(model.boundary)