import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lap.settings")
django.setup()

from analytics import models

onto_protein_to_probe_dict = {
    'ADP-ribosylation factor-like protein 13B': {'Anti-Arl13B'},
    'ATP-binding_cassette_sub-family_A_member_3': {'Anti-Abca3'},
    'advanced_glycosylation_end_product-specific_receptor': {'Anti-Ager'},
    'alpha-actin-2': {'Anti-Acta2'},
    'calcitonin': {'Anti-Calca'},
    'chondroitin_sulfate_proteoglycan_4': {'Anti-Cspg4'},
    'endomucin': {'Anti-Emcn'},
    'histone_H3.3C': {'Anti-p-Histone H3'},
    'homeobox_protein_Nkx-2.1': {'Anti-Nkx2-1'},
    'homeodomain-only_protein': {'Anti-Hopx'},
    'lymphatic_vessel_endothelial_hyaluronic_acid_receptor_1': {'Anti-Lyve1'},
    'platelet_endothelial_cell_adhesion_molecule': {'Anti-Pecam1'},
    'pulmonary_surfactant-associated_protein_C': {'Anti-Sftpc'},
    'transcription_factor_SOX-2': {'Anti-Sox2'},
    'transcription_factor_SOX-9': {'Anti-Sox9'},
    'tubulin_alpha-1A_chain': {'Anti-Tuba1a'},
    'uteroglobin': {'Anti-SCGB1A1', 'Anti-Scgb1a1'},
    'vimentin': {'Anti-Vimentin'}
}

for k, v in onto_protein_to_probe_dict.items():
    e = models.OntoEntity.objects.get(name=k.replace('_', ' '))
    for p_label in v:
        print(p_label)
        try:
            p = models.Probe.objects.get(label=p_label, species='mus musculus')
        except models.Probe.DoesNotExist:
            continue

        models.ProbeOntoProteinMap.objects.get_or_create(probe=p, protein=e)
