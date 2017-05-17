# https://docs.google.com/document/d/10qtrZeCFeGPZt5r6Z_TKWl0ihXBzNysp8nhOpbgrl1o/edit

ALL_EXPERIMENTS_WITH_IMAGE = """
PREFIX lm: <http://ontology.lungmap.net/ontologies/expression_ontology#>
SELECT DISTINCT ?experiment, ?experiment_type_label
FROM  <http://data.lungmap.net/lungmap_data>
WHERE {
    ?image lm:part_of_experiment ?experiment .
    ?experiment lm:is_experiment_type/rdfs:label ?experiment_type_label .
    ?experiment lm:is_experiment_type/rdfs:label "Immunofluorescence-Confocal" .
    ?image lm:display_url ?img_file .
    ?image lm:magnification ?magnification .
    ?image lm:x_scaling ?x_scaling .
    ?image lm:y_scaling ?y_scaling .
    ?experiment lm:file_name ?path .
} ORDER BY ASC(?experiment)
"""

GET_IMAGES_BY_EXPERIMENT = """
PREFIX lm: <http://ontology.lungmap.net/ontologies/expression_ontology#>
PREFIX mont: <http://ontology.lungmap.net/ontologies/mouse_anatomy#>
PREFIX owl: <http://www.w3.org/2002/07/>
PREFIX owl2: <http://www.w3.org/2002/07/owl#>
SELECT DISTINCT ?experiment ?image ?path ?img_file ?magnification ?x_scaling ?y_scaling
FROM  <http://data.lungmap.net/lungmap_data>
FROM  <http://data.lungmap.net/sequence_mappings>
FROM  <http://data.lungmap.net/lungmap_ontology>
WHERE {
    VALUES ?experiment { owl2:EXPERIMENT_PLACEHOLDER } .
    ?image lm:part_of_experiment ?experiment .
    ?image lm:display_url ?img_file .
    ?image lm:magnification ?magnification .
    ?image lm:x_scaling ?x_scaling .
    ?image lm:y_scaling ?y_scaling .
    ?experiment lm:file_name ?path .
} ORDER BY ASC(xsd:integer(REPLACE(str(?magnification), 'X', '')))
"""

GET_ANATOMY_BY_EXPERIMENT = """
PREFIX lm: <http://ontology.lungmap.net/ontologies/expression_ontology#>
PREFIX mont: <http://ontology.lungmap.net/ontologies/mouse_anatomy#>
PREFIX owl: <http://www.w3.org/2002/07/>
PREFIX owl2: <http://www.w3.org/2002/07/owl#>
SELECT DISTINCT ?experiment ?term ?term_label
FROM  <http://data.lungmap.net/lungmap_data>
FROM  <http://data.lungmap.net/sequence_mappings>
FROM  <http://data.lungmap.net/lungmap_ontology>
WHERE {
    VALUES ?experiment { owl2:EXPERIMENT_PLACEHOLDER } .
    ?experiment lm:has_condition ?term .
    ?term rdfs:label ?term_label
}"""

GET_SAMPLE_BY_EXPERIMENT = """
PREFIX lm: <http://ontology.lungmap.net/ontologies/expression_ontology#>
PREFIX owl: <http://www.w3.org/2002/07/>
PREFIX owl2: <http://www.w3.org/2002/07/owl#>
PREFIX mont: <http://ontology.lungmap.net/ontologies/mouse_anatomy#>
PREFIX hont: <http://ontology.lungmap.net/ontologies/human_anatomy#>
SELECT ?sample_id ?tax_id ?organism_label ?local_id ?age ?age_label ?age_group ?age_group_label ?weight ?sex ?race ?cause_of_death ?health_status ?strain ?genotype ?crown_rump_length ?harvest_date
WHERE {
    VALUES ?experiment_id { owl2:EXPERIMENT_PLACEHOLDER }
    ?sample_id lm:part_of_experiment ?experiment_id .
    ?sample_id lm:in_organism ?tax_id .
    ?tax_id rdfs:label ?organism_label .
    ?sample_id lm:local_id ?local_id .
    ?sample_id lm:in_stage ?age .
    ?sample_id lm:in_stage ?age .
    OPTIONAL { ?age rdfs:label ?age_label }
    FILTER NOT EXISTS { ?age rdfs:subClassOf hont:LMHA0000000648 }
    OPTIONAL {
       ?sample_id lm:in_stage ?age_group .
       ?age_group rdfs:label ?age_group_label .
       ?age_group rdfs:subClassOf hont:LMHA0000000648
    }
    ?sample_id lm:weight ?weight .
    ?sample_id lm:gender ?sex .
    OPTIONAL {?sample_id lm:race ?race }
    OPTIONAL {?sample_id lm:cause_of_death ?cause_of_death }
    OPTIONAL {?sample_id lm:health_status ?health_status }
    OPTIONAL {?sample_id lm:in_strain ?strain }
    OPTIONAL {?sample_id lm:genotype ?genotype }
    OPTIONAL {?sample_id lm:crown_rump_length ?crown_rump_length }
    OPTIONAL {?sample_id lm:harvest_date ?harvest_date }
}"""

GET_PROBE_BY_EXPERIMENT = """
PREFIX lm: <http://ontology.lungmap.net/ontologies/expression_ontology#>
PREFIX mont: <http://ontology.lungmap.net/ontologies/mouse_anatomy#>
PREFIX owl: <http://www.w3.org/2002/07/>
PREFIX owl2: <http://www.w3.org/2002/07/owl#>
SELECT DISTINCT ?experiment_id ?probe_id ?probe_label ?color (GROUP_CONCAT(DISTINCT CONCAT(?gene_id, ';', ?symbol),'|') as ?target_molecules) (GROUP_CONCAT(DISTINCT CONCAT(?anatomy,';',?anatomy_label),'|') AS ?target_conditions)
WHERE {
    VALUES ?experiment_id { owl2:EXPERIMENT_PLACEHOLDER } .
    ?experiment_id lm:in_organism ?tax_id .
    ?image lm:part_of_experiment ?experiment_id .
    ?image lm:has_probe ?probe_id .
    ?probe_color lm:maps_to ?probe_id .
    ?probe_color lm:maps_to ?image .
    ?probe_color lm:color ?color .
    OPTIONAL { 
        ?probe_id lm:maps_to ?resource .
        ?resource lm:maps_to{0,1} ?gene_id .
        ?gene_id lm:id_type owl:Gene_ID .
        ?gene_id rdfs:label ?symbol .
        ?gene_id lm:in_organism ?tax_id .
    }
    OPTIONAL { ?probe_id rdfs:label ?probe_label }
    OPTIONAL { 
        ?probe_id lm:probe_target_condition ?anatomy .
        ?anatomy rdfs:label ?anatomy_label
    }
}
"""

GET_EXPERIMENT_TYPE_BY_EXPERIMENT = """
PREFIX lm: <http://ontology.lungmap.net/ontologies/expression_ontology#>
PREFIX mont: <http://ontology.lungmap.net/ontologies/mouse_anatomy#>
PREFIX owl: <http://www.w3.org/2002/07/>
PREFIX owl2: <http://www.w3.org/2002/07/owl#>
SELECT DISTINCT ?experiment ?experiment_type_label ?release_date ?description ?platform
FROM  <http://data.lungmap.net/lungmap_data>
FROM  <http://data.lungmap.net/lungmap_ontology>
WHERE {
    VALUES ?experiment { owl2:EXPERIMENT_PLACEHOLDER } .
    ?experiment lm:is_experiment_type/rdfs:label ?experiment_type_label .
    OPTIONAL { ?experiment lm:creation_date|(^lm:part_of_experiment/lm:creation_date) ?release_date }
    OPTIONAL { ?experiment rdfs:comment ?description }
    OPTIONAL { ?experiment lm:platform|(^lm:part_of_experiment/lm:platform) ?platform }
}"""

GET_RESEARCHER_BY_EXPERIMENT = """
PREFIX lm: <http://ontology.lungmap.net/ontologies/expression_ontology#>
PREFIX mont: <http://ontology.lungmap.net/ontologies/mouse_anatomy#>
PREFIX owl: <http://www.w3.org/2002/07/>
PREFIX owl2: <http://www.w3.org/2002/07/owl#>
SELECT DISTINCT ?experiment ?researcher_label ?site_label
FROM  <http://data.lungmap.net/lungmap_data>
FROM  <http://data.lungmap.net/lungmap_ontology>
WHERE {
    VALUES ?experiment { owl2:EXPERIMENT_PLACEHOLDER } .
    ?researcher a lm:researcher .
    ?experiment lm:part_of ?researcher .
    ?site a lm:site .
    ?researcher lm:part_of ?site .
    ?researcher rdfs:label ?researcher_label .
    ?site rdfs:label ?site_label .
}"""
