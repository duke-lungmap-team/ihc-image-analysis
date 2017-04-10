#https://docs.google.com/document/d/10qtrZeCFeGPZt5r6Z_TKWl0ihXBzNysp8nhOpbgrl1o/edit

ALL_PROBES = """
PREFIX lm: <http://ontology.lungmap.net/ontologies/expression_ontology#>
PREFIX mont: <http://ontology.lungmap.net/ontologies/mouse_anatomy#>
PREFIX owl: <http://www.w3.org/2002/07/>
PREFIX owl2: <http://www.w3.org/2002/07/owl#>
SELECT DISTINCT ?experiment_id ?probe_id ?probe_label ?color (GROUP_CONCAT(DISTINCT CONCAT(?gene_id, ';', ?symbol),'|') as ?target_molecules) (GROUP_CONCAT(DISTINCT CONCAT(?anatomy,';',?anatomy_label),'|') AS ?target_conditions)
WHERE {
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

ALL_EXPERIMENTS = """PREFIX lm: <http://ontology.lungmap.net/ontologies/expression_ontology#>
PREFIX mont: <http://ontology.lungmap.net/ontologies/mouse_anatomy#>
PREFIX owl: <http://www.w3.org/2002/07/>
PREFIX owl2: <http://www.w3.org/2002/07/owl#>
SELECT DISTINCT ?experiment_id ?experiment_type_id ?image_id ?path ?raw_file ?label ?description ?age ?age_label ?organism ?organism_label ?magnification ?platform ?strain ?date ?gender
FROM  <http://data.lungmap.net/lungmap_data>
FROM  <http://data.lungmap.net/lungmap_ontology>
WHERE {
   ?image_id lm:part_of_experiment ?experiment_id .
   ?experiment_id lm:file_name ?path .
   ?image_id lm:display_url ?raw_file .
   ?image_id lm:part_of_experiment ?experiment_id .
   OPTIONAL { ?experiment_id rdfs:comment ?description } .
   OPTIONAL { ?image_id lm:magnification ?magnification } .
   OPTIONAL { ?image_id lm:platform ?platform } .
   OPTIONAL { ?image_id lm:creation_date ?date } .
   OPTIONAL { ?experiment_id lm:gender ?gender } .
   OPTIONAL {
      ?experiment_id lm:in_strain ?strain_id .
      BIND(REPLACE(str(?strain_id), '^.+#', '') AS ?strain) .
   } .
   ?experiment_id rdfs:label ?label .
    ?experiment_id lm:is_experiment_type ?experiment_type_id .
   ?image_id lm:in_stage ?age .
   ?age rdfs:subClassOf ?organism .
   ?organism rdfs:subClassOf lm:organism .
   ?organism rdfs:label ?organism_label .
   ?age rdfs:label ?age_label .
}
"""

RESEARCHERS_AND_SITES = """PREFIX lm: <http://ontology.lungmap.net/ontologies/expression_ontology#>
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
}
"""

DESCRIPTION_AND_PLATFORM = """PREFIX lm: <http://ontology.lungmap.net/ontologies/expression_ontology#>
PREFIX mont: <http://ontology.lungmap.net/ontologies/mouse_anatomy#>
PREFIX owl: <http://www.w3.org/2002/07/>
PREFIX owl2: <http://www.w3.org/2002/07/owl#>
SELECT DISTINCT ?experiment_type_label ?release_date ?description ?platform
FROM  <http://data.lungmap.net/lungmap_data>
FROM  <http://data.lungmap.net/lungmap_ontology>
WHERE {
    VALUES ?experiment { owl2:EXPERIMENT_PLACEHOLDER } .
    ?experiment lm:is_experiment_type/rdfs:label ?experiment_type_label .
    OPTIONAL { ?experiment lm:creation_date|(^lm:part_of_experiment/lm:creation_date) ?release_date }
    OPTIONAL { ?experiment rdfs:comment ?description }
    OPTIONAL { ?experiment lm:platform|(^lm:part_of_experiment/lm:platform) ?platform }
}"""

PROBE_STAIN = """PREFIX lm: <http://ontology.lungmap.net/ontologies/expression_ontology#>
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

SAMPLE_DETAILS = """PREFIX lm: <http://ontology.lungmap.net/ontologies/expression_ontology#>
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
}
"""

EXPERIMENT_ANATOMY = """PREFIX lm: <http://ontology.lungmap.net/ontologies/expression_ontology#>
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
}
"""

EXPERIMENT_IMAGES = """PREFIX lm: <http://ontology.lungmap.net/ontologies/expression_ontology#>
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