# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 16:32:19 2020

@author: Hyun Kil Shin
ORCID: https://orcid.org/0000-0003-3665-0841

manuscript DOI: https://doi.org/10.1039/D0RA05873D

This code intends to generate element table from molecular formula (MF) of inorganic compound.
Example of expected input: Fe2O3, Al(OH3)2.
"""

import pandas as pd
import numpy as np
import os
from rdkit import Chem

def extract_atom_from_fragment (mf_frag, mf_dict, multi=1):
    '''
    !Molecular formula is fragmented for each atom.
    !Each atom is identified, and the number of them is counted.
    
    @variables
    >> mf_frag: string of molecular formular (entire or fraction of it)
    >> mf_dict: dictrionary whose key is atom and value is the number of atom.
    >> multi: integer extracted from molecualr formular.
    '''
    
    atom = ''
    num = ''
    for m in mf_frag:
        if m.isdigit():
            num = num + m
        else:
            atom = atom + m
    
    if num != '':
        mf_dict[atom] = mf_dict[atom]+int(num)*multi
    else:
        mf_dict[atom] = mf_dict[atom]+1*multi
    
    return mf_dict


def extract_atom_with_number (mf, mf_dict, multi=1):    
    '''
    !Extract atom and their number from molecular formula
    
    @variable
    >> mf: string of molecular formular
    >> mf_dict: dictionary whose key is atom and value is the number of atom.
    >> multi: integer extracted from molecular formular.
    '''
    capital_index = []
    for i in range(len(mf)):
        if mf[i].isupper():
            capital_index.append(i)
    
    #Count number of atoms from simple molecular formula
    if len(capital_index) > 1:  
        for i in range(1,len(capital_index)):
            mf_frag = mf[capital_index[i-1]:capital_index[i]]
            extract_atom_from_fragment(mf_frag, mf_dict, multi)
            #mf_dict = extract_atom_from_fragment(mf_frag, mf_dict, multi)
            
        #Collect last part of the molecular formula            
        mf_frag = mf[capital_index[i]:]
        extract_atom_from_fragment(mf_frag, mf_dict, multi)
        #mf_dict = extract_atom_from_fragment(mf_frag, mf_dict, multi)
        
    #If molecular formula is composed of single atom.
    else:
        mf_frag = mf[capital_index[0]:]
        extract_atom_from_fragment(mf_frag, mf_dict, multi)
        #mf_dict = extract_atom_from_fragment(mf_frag, mf_dict, multi)
        
    
    return mf_dict
    

def prepare_atom_dict (molecular_formulars):
    '''
    !Produce dictionary. Key is atom, value is the number of atom in molecular formular.
    
    @ variable
    >> molecular_formulars: string of molecular formular(e.g., Fe2O3)#
    '''
    
    periodic_table = Chem.GetPeriodicTable()    #Available electron composition is upto Rf(atomic number: 104)
    atom = [periodic_table.GetElementSymbol(i) for i in range(1,105)]
    
    atom_dict = {k:0 for k in atom}
    
    start = 0
    end = 0
    parenthesis_index = [] #Check location of start and end of parenthesis mark and number attached after parenthesis.
    for i in range(len(molecular_formulars)):
        if molecular_formulars[i] == '(':
            start = i
        elif molecular_formulars[i] == ')':
            end = i
        elif molecular_formulars[i-1] == ')' and molecular_formulars[i].isdigit():
            parenthesis_index.append(start+1)   #start index for parenthesis
            parenthesis_index.append(end)       #final index for parenthesis
            parenthesis_index.append(int(molecular_formulars[i:])) #The number after parenthesis
    
    #Count number of atoms within parentheses
    remove_list = []
    start_end_mfnum = np.array([0,1,2])
    for i in range(int(len(parenthesis_index)/3)):
        parenthesis_mf = molecular_formulars[parenthesis_index[start_end_mfnum[0]]:parenthesis_index[start_end_mfnum[1]]]
        extract_atom_with_number(parenthesis_mf, atom_dict, parenthesis_index[start_end_mfnum[2]])
        #atom_dict = extract_atom_with_number(parenthesis_mf, atom_dict, parenthesis_index[start_end_mfnum[2]])
        
        remove_from_mf = molecular_formulars[parenthesis_index[start_end_mfnum[0]]-1:parenthesis_index[start_end_mfnum[1]]+1+len(str(parenthesis_index[-1]))]
        remove_list.append(remove_from_mf)
        start_end_mfnum = start_end_mfnum+3
    
    #Remove molecular formula within parentheses
    for r in remove_list:
        molecular_formulars = molecular_formulars.replace(r, "")
    molecular_formulars = molecular_formulars.replace('(',"")
    molecular_formulars = molecular_formulars.replace(')',"")
        
    #Count remained part of molecular formula
    #Skip empty string
    if molecular_formulars!='':
        extract_atom_with_number(molecular_formulars, atom_dict)
    #atom_dict = extract_atom_with_number(molecular_formulars, atom_dict)
    
    return atom_dict

def generate_atom_dataframe (id_list):
    '''
    !Produce Pandas dataframe whose dolumns of dataframe are mf and list of elements.
    
    @ variable
    >> id_list: Pandas Series of molecular formular
    '''
    
    atom_dict_list = []
    for i in id_list:
        try:
            atom_dict_list.append(prepare_atom_dict(i))
        except:
            print (i)
    df = pd.DataFrame(atom_dict_list)
    return df

wdir = r'target_directory_for_molecular_formular_file'
excel = 'molecular_formaular_file_name.xlsx'

df = pd.read_excel(os.path.join(wdir, excel))

col_key = 'id' #Column name for molecular formular column
atom_table = generate_atom_dataframe(df[col_key])

df_final = pd.concat([df, atom_table],axis=1)
df_final.to_excel(os.path.join(wdir, excel.replace('.xlsx','_element_table.xlsx')), index=False)
