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

GET_IMAGES_BY_EXPERIMENT = """
PREFIX lm: <http://www.lungmap.net/ontologies/data#>
PREFIX lmdb: <http://www.lungmap.net/ontologies/database#>
SELECT DISTINCT strafter(str(?experiment),'#') as ?experiment strafter(str(?experiment_type),'#') as ?experiment_type ?image ?path ?dir ?magnification ?x_scaling ?y_scaling ?image_file_path
WHERE {
    VALUES ?experiment { lm:EXPERIMENT_PLACEHOLDER } .
    ?image lmdb:part_of_experiment ?experiment .
    ?image lmdb:directory ?dir .
    ?image lmdb:magnification ?magnification .
    ?image lmdb:x_scaling ?x_scaling .
    ?image lmdb:y_scaling ?y_scaling .
    ?image lmdb:has_supporting_file ?image_file_id .
    ?image_file_id lmdb:display_url ?image_file_path .
    ?experiment lmdb:s3_path ?path .
    ?experiment lmdb:is_experiment_type ?experiment_type
} ORDER BY ASC(xsd:integer(REPLACE(str(?magnification), 'X', '')))
"""


GET_PROBE_BY_EXPERIMENT = """
PREFIX lm: <http://www.lungmap.net/ontologies/data#>
PREFIX lmdb: <http://www.lungmap.net/ontologies/database#>
SELECT DISTINCT ?experiment_id ?probe_id ?probe_label ?color
WHERE {
    VALUES ?experiment_id { lm:EXPERIMENT_PLACEHOLDER } .
    ?image lmdb:part_of_experiment ?experiment_id .
    ?image lmdb:has_probe_color ?probe_color .
    ?probe_color lmdb:maps_to ?probe_id .
    ?probe_color lmdb:color ?color .
    ?probe_id rdfs:label ?probe_label
}
"""
