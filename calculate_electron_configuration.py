# -*- coding: utf-8 -*-
"""
Created on Wed May 20 16:18:45 2020

@author: Hyun Kil Shin
ORCID: https://orcid.org/0000-0003-3665-0841

manuscript DOI: https://doi.org/10.1039/D0RA05873D

This code intends to calculate electron configuration from element table.

Two input files are required.
1) File for ground-state of electron configuration for each element.
2) Element table file.

Element table is expected to have
1) id column: molecular formular is listed.
2) target_property: mp, logS, and so forth.
3) elements: from H to Rf
"""

import pandas as pd
import numpy as np
import os

wdir = r'target_directory_for_element_table_file'
electronic_configuration = 'elecronic_configuration_final_no7d7f.xlsx'
ec_df = pd.read_excel(os.path.join(wdir, electronic_configuration))
ec_df = ec_df.set_index('atom')
ec_df = ec_df.drop(['AN'],axis=1)

element_table = 'element_file_name.xlsx'

target_df = pd.read_excel(os.path.join(wdir, element_table))

ao_composition = []
col_names = target_df.columns[2:]
for index, row in target_df.iterrows():
    empty_ao = np.zeros(ec_df.shape[-1])
    for c in col_names:
        empty_ao = empty_ao + ec_df.loc[c].to_numpy() * row[c]
    ao_composition.append(empty_ao)

ao_df = pd.DataFrame(ao_composition, columns=ec_df.columns)

target_id = target_df.iloc[:,[0,1]]
df_final = pd.concat([target_id, ao_df], axis=1)

file_name = element_table.replace('.','_ec.')
df_final.to_excel(os.path.join(wdir, file_name),index=False)
