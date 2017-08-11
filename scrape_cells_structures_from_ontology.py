import ontospy

SPARQL_CELL_PROBE = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX : <http://www.semanticweb.org/am175/ontologies/2017/1/untitled-ontology-79#>
SELECT ?c ?p ?p_label WHERE {
    ?c rdfs:subClassOf* :cell . 
    ?p rdfs:subClassOf :macromolecule .
    ?p :has_synonym ?p_label . 
    ?c rdfs:subClassOf ?restriction .
    ?restriction owl:onProperty :has_part ; owl:someValuesFrom ?p .
}
"""

SPARQL_MACROMOLECULES = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX : <http://www.semanticweb.org/am175/ontologies/2017/1/untitled-ontology-79#>
SELECT ?c WHERE {
    ?c rdfs:subClassOf :macromolecule .
}
"""

SPARQL_CELL_TISSUE_STRUCTURE = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX : <http://www.semanticweb.org/am175/ontologies/2017/1/untitled-ontology-79#>
    SELECT ?t ?s WHERE {
        ?c rdfs:subClassOf ?restriction .
        ?restriction owl:onProperty :part_of ; owl:someValuesFrom ?t .
        ?t rdfs:subClassOf* :tissue .
        ?t rdfs:subClassOf ?restriction2 .
        ?restriction2 owl:onProperty :part_of ; owl:someValuesFrom ?s .
        VALUES ?c { <%s> }
    }
"""


model = ontospy.Ontospy("playground/histology of lung E16.5AMM1_v2.owl")

cell_probe_combos = model.query(SPARQL_CELL_PROBE)

probe_struct_list = []

for cp in cell_probe_combos:
    cell_uri = cp[0]
    probe_uri = cp[1]

    sparql_cell_tissue_structure = SPARQL_CELL_TISSUE_STRUCTURE % cell_uri

    result = model.query(sparql_cell_tissue_structure)

    if len(result) > 0:
        probe_struct_list.append(
            {
                'probe': probe_uri,
                'cell': cell_uri,
                'tissue': result[0][0],
                'structure': result[0][1]
            }
        )