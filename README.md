# Electron configuration descriptor calculation
Codes for calculating electron configuration descriptor for inorganic compounds

Hyun Kil Shin, Electron configuration-based neural network model to predict physicochemical properties of inorganic compounds, RSC Advances, 2020, 10, 33268-33278.
DOI of manuscript: https://doi.org/10.1039/D0RA05873D
ORCID: https://orcid.org/0000-0003-3665-0841

[1]'generate_element_table_from_molecular_formulars.py' produces element table based on molecular formular
(input example file is 'molecular_formular_input_example.xlsx)

[2]'calculate_electron_configuration.py' calcualtes electron configuration descriptor based on two input files: 1) element table prepared by code[1] and 2) ground-state electron configuration for elements ('electron_cohnfiguration_final_no7d7f.xlsx')

[3]'molecular_formular_input_example_atom_table_check.xlsx' is an example of element table.

[4] 'molecular_formular_input_example_atom_table_check_ec.xlsx' is an example of electron configuration descriptors.
