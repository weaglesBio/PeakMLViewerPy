import xml.etree.ElementTree as ET
from Chemistry.Molecule import Molecule

def load_molecule_databases():

    molecules = {}

    try:
            # If errors while attempt to read, requires conversion.
        with open("settings.xml") as f:
            settings_tree_data = f.read()

    except Exception as err:
        print(err)

    settings_root = ET.fromstring(settings_tree_data)

    for databases in settings_root.findall("./settings/databases/database"):

        try:
            # If errors while attempt to read, requires conversion.
            with open(databases.text) as f:
                tree_data = f.read()

            compound_root = ET.fromstring(tree_data)

            for compound_node in compound_root.findall("./compound"):

                id = compound_node.find("./id")
                name = compound_node.find("./name")
                formula = compound_node.find("./formula")
                inchi = compound_node.find("./inchi")
                smiles = compound_node.find("./smiles")
                synonyms = compound_node.find("./synonyms")
                retentiontime = compound_node.find("./retentiontime")
                description = compound_node.find("./description")
                classdesc = compound_node.find("./class")
                mass = compound_node.find("./monoisotopicmass")
                polarity = compound_node.find("./polarity")

                molecule = Molecule(id.text, name.text, formula.text)
                if inchi is not None:
                    molecule.set_inchi(inchi.text)

                if smiles is not None:
                    molecule.set_smiles(smiles.text)

                if synonyms is not None:    
                    molecule.set_synonyms(synonyms.text)

                if description is not None:
                    molecule.set_description(description.text)

                if classdesc is not None:
                    molecule.set_class_description(classdesc.text)

                if retentiontime is not None:
                    molecule.set_retention_time(float(retentiontime.text) * 60.0)

                if mass is not None and mass.text is not None and len(mass.text) > 0:
                        molecule.set_mass(mass.text)
                        
                if polarity is not None:
                    molecule.set_polarity(polarity.text)

                molecules[id.text] = molecule

        except Exception as err:
            print(err)

    return molecules
            