# https://docs.google.com/document/d/10qtrZeCFeGPZt5r6Z_TKWl0ihXBzNysp8nhOpbgrl1o/edit

GET_BASIC_EXPERIMENTS = """
PREFIX lm: <http://www.lungmap.net/ontologies/data#>
PREFIX lmdb:<http://www.lungmap.net/ontologies/database#>
SELECT ?experiment_id ?species ?stage_label
WHERE {
    VALUES ?exp_type_id { lm:LMXT0000000003 } .
    ?experiment_id lmdb:is_experiment_type ?exp_type_id .
    ?experiment_id lmdb:in_organism ?tax_id .
    ?tax_id rdfs:label ?species . 
    ?experiment_id lmdb:uses_sample ?sample_id . 
    ?sample_id lmdb:in_stage ?stage .
    ?stage rdfs:label ?stage_label .
}
"""

ALL_EXPERIMENTS_WITH_IMAGE = """
PREFIX lm: <http://www.lungmap.net/ontologies/data#>
PREFIX lmdb:<http://www.lungmap.net/ontologies/database#>
SELECT DISTINCT ?experiment
WHERE {
    VALUES (?exp_type ?image_type) { (lm:LMXT0000000003 lmdb:expression_image) } .
    ?experiment lmdb:is_experiment_type ?exp_type .
    ?image lmdb:part_of_experiment ?experiment .
    ?image rdf:type ?image_type
} ORDER BY ASC(?experiment)
"""

GET_IMAGES_BY_EXPERIMENT = """
PREFIX lm: <http://www.lungmap.net/ontologies/data#>
PREFIX lmdb: <http://www.lungmap.net/ontologies/database#>
SELECT DISTINCT ?experiment ?image ?path ?dir ?magnification ?x_scaling ?y_scaling
WHERE {
    VALUES ?experiment { lm:EXPERIMENT_PLACEHOLDER } .
    ?image lmdb:part_of_experiment ?experiment .
    ?image lmdb:directory ?dir .
    ?image lmdb:magnification ?magnification .
    ?image lmdb:x_scaling ?x_scaling .
    ?image lmdb:y_scaling ?y_scaling .
    ?experiment lmdb:s3_path ?path .
} ORDER BY ASC(xsd:integer(REPLACE(str(?magnification), 'X', '')))
"""

GET_SAMPLE_BY_EXPERIMENT = """
PREFIX lm: <http://www.lungmap.net/ontologies/data#>
PREFIX lmdb: <http://www.lungmap.net/ontologies/database#>
SELECT ?sample_id ?organism_label ?local_id ?age_label
WHERE {
    VALUES ?experiment_id { lm:EXPERIMENT_PLACEHOLDER }
    ?experiment_id lmdb:uses_sample ?sample_id .
    ?sample_id lmdb:in_organism ?tax_id .
    ?tax_id rdfs:label ?organism_label .
    ?sample_id lmdb:local_id ?local_id .
    ?sample_id lmdb:in_stage ?age .
    ?age rdfs:label ?age_label
}
"""

GET_PROBE_BY_EXPERIMENT = """
PREFIX lm: <http://www.lungmap.net/ontologies/data#>
PREFIX lmdb: <http://www.lungmap.net/ontologies/database#>
SELECT DISTINCT ?experiment_id ?probe_id ?probe_label ?color
WHERE {
    VALUES ?experiment_id { lm:EXPERIMENT_PLACEHOLDER } .
    ?experiment_id lmdb:in_organism ?tax_id .
    ?image lmdb:part_of_experiment ?experiment_id .
    ?image lmdb:has_probe ?probe_id .
    ?probe_color lmdb:maps_to ?probe_id .
    ?probe_color lmdb:maps_to ?image .
    ?probe_color lmdb:color ?color .
    ?probe_id rdfs:label ?probe_label
}
"""

GET_EXPERIMENT_TYPE_BY_EXPERIMENT = """
PREFIX lm: <http://www.lungmap.net/ontologies/data#>
PREFIX lmdb: <http://www.lungmap.net/ontologies/database#>
SELECT DISTINCT ?experiment ?experiment_type_label
WHERE {
    VALUES ?experiment { lm:EXPERIMENT_PLACEHOLDER } .
    ?experiment lmdb:is_experiment_type/rdfs:label ?experiment_type_label .
}
"""
