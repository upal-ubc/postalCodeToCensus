#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 21:35:23 2019

@author: rohannuttall
"""

import pandas as pd 
import numpy as np

# Postal Code Conversion File (PCCF)
filename = 'pccf59_MAY11_fccp59.txt'

# Open PCCF with proper encoding 
f = open(filename, 'r', encoding = "ISO-8859-1") 

# Define lists to fill. Comments indicate line positions as indicated on pg 13
# table "Record layouts and data descriptions"

postalCode = [] # 1 - 6
SAC = [] # 103 - 110 
CTname = [] # 103 - 110 
fullCT = [] 
DAuid = [] # 126 - 134
DisseminationBlockCode = [] # 134 - 136 
LAT = [] # 137 - 148 
LONG = [] # 148 - 161
Comm_Name = [] # 163 - 193 

# Loop over all lines in text file, and extract useful information 
for line in f.readlines():
    # "933" is the Statistical Area Classification for Vancouver
    if line[98:101] == '933': 
        postalCode.append(line[0:6])
        SAC.append(line[98:101])
        CTname.append(line[102:109])
        fullCT.append(line[98:101]+line[102:109])
        DAuid.append(line[125:133])
        DisseminationBlockCode.append(line[133:135])
        LAT.append(line[136:147])
        LONG.append(line[147:160])
        Comm_Name.append(line[162:192])
        # Print every 1000 lines
        if len(Comm_Name) % 1000 == 0:
            print("Lines processed: %s" % (len(Comm_Name)))
print("Done!")    
f.close()

# Write to dataframe. This is now the dictionary that can be used to map 
# postal code to a dissemination area, census tract, etc.
print("Writing to DataFrame......")
dictionary = pd.DataFrame({'postalCode':postalCode, 'SAC':SAC, 'CTname':CTname, 
                   'fullCT':fullCT, 'DAuid':DAuid,'DisseminationBlockCode':DisseminationBlockCode,
                   'LAT':LAT, 'LONG':LONG, 'Comm_Name':Comm_Name})
 
def postalCodeToSAC(postalCode, dictionary):
    sac = dictionary[dictionary['postalCode']==postalCode]['SAC']
    if not sac.empty:
        return sac
    else:
        return pd.Series([])

def postalCodeToCT(postalCode, dictionary):
    CT = dictionary[dictionary['postalCode']==postalCode]['fullCT']
    if not CT.empty:
        return CT
    else:
        return pd.Series([])

def postalCodeToDAuid(postalCode, dictionary):
    DAuid = dictionary[dictionary['postalCode']==postalCode]['DAuid']
    if not DAuid.empty:
        return DAuid
    else:
        return pd.Series([])

def partialPostalCodeToDAuid(postalCode, dictionary):
    #In case only part of a postal code is available.
    DAuid = dictionary[dictionary['postalCode'].str.contains(postalCode)]['DAuid']
    if not DAuid.empty:
        return DAuid
    else:
        return pd.Series([])    
    
def postalCodeToDisseminationBlockCode(postalCode, dictionary):
    DissBlockCode =  dictionary[dictionary['postalCode']==postalCode]['DisseminationBlockCode']
    if not DissBlockCode.empty:
        return DissBlockCode
    else:
        return pd.Series([])
    
        
def partialPostalCodeToDisseminationBlockCode(postalCode, dictionary):
    DissBlockCode =  dictionary[dictionary['postalCode'].str.contains(postalCode)]['DisseminationBlockCode']
    if not DissBlockCode.empty:
        return DissBlockCode
    else:
        return pd.Series([])
    
def postalCodeToLATLON(postalCode, dictionary):
    lat = dictionary[dictionary['postalCode']==postalCode]['LAT']
    long = dictionary[dictionary['postalCode']==postalCode]['LONG']
    
    if not lat.empty:
        return lat, long
    else:
        return pd.Series([])

#Match postal codes to census tracts
def matchPostalToCT(postalCode_df):
    print("Matching postal codes to census tracts...")
    listOfPostalCodes = []
    listOfCTs = []
    for postalCode in postalCode_df['postalCode'].values:
        # change this function call to get other things i.e. SAC, DAuids,
        CTmatches = postalCodeToCT(postalCode, dictionary).values
        for val in CTmatches:
            listOfPostalCodes.append(postalCode)
            listOfCTs.append(val)
    return listOfPostalCodes, listOfCTs

#Match postal codes to latitude/longitude pairs
def matchPostalToLATLON(postalCode_df):
    print("Matching postal codes to lat lons...")
    listOfPostalCodes = []
    listOfLATLONs = []
    for postalCode in postalCode_df['postalCode'].values:
        # change this function call to get other things i.e. SAC, DAuids,
        LATLONmatches = postalCodeToLATLON(postalCode, dictionary).values
        for val in LATLONmatches:
            listOfPostalCodes.append(postalCode)
            listOfLATLONs.append(val)
    return listOfPostalCodes, listOfLATLONs

#Match postal codes to dissemination areas
def matchPostalToDA(postalCode_df):
    print("Matching postal codes to dissemination areas...")
    listOfPostalCodes = []
    listOfDAs = []
    for postalCode in postalCode_df['postalCode'].values:
        # change this function call to get other things i.e. SAC, DAuids,
        DAmatches = postalCodeToDAuid(postalCode, dictionary).values
        for val in DAmatches:
            listOfPostalCodes.append(postalCode)
            listOfDAs.append(val)
    return listOfPostalCodes, listOfDAs

#Match postal codes to dissemination areas
def matchPostalToDisBlockCodes(postalCode_df):
    print("Matching postal codes to dissemination areas...")
    listOfPostalCodes = []
    listOfDissBlockCodeMatches = []
    for postalCode in postalCode_df['postalCode'].values:
        # change this function call to get other things i.e. SAC, DAuids,
        DissBlockCodeMatches = postalCodeToDisseminationBlockCode(postalCode, dictionary).values
        for val in DissBlockCodeMatches:
            listOfPostalCodes.append(postalCode)
            listOfDissBlockCodeMatches.append(val)
    return listOfPostalCodes, listOfDissBlockCodeMatches

#Match postal codes to dissemination areas
def matchPartialPostalToDisBlockCodes(postalCode_df):
    print("Matching postal codes to dissemination areas...")
    listOfPostalCodes = []
    listOfDissBlockCodeMatches = []
    for postalCode in postalCode_df['postalCode'].values:
        # change this function call to get other things i.e. SAC, DAuids,
        DissBlockCodeMatches = partialPostalCodeToDisseminationBlockCode(postalCode, dictionary).values
        for val in DissBlockCodeMatches:
            listOfPostalCodes.append(postalCode)
            listOfDissBlockCodeMatches.append(val)
    return listOfPostalCodes, listOfDissBlockCodeMatches


#Match postal codes to dissemination areas
def matchPartialPostalToDA(postalCode_df):
    print("Matching postal codes to dissemination areas...")
    listOfPostalCodes = []
    listOfDAs = []
    for postalCode in postalCode_df['postalCode'].values:
        # change this function call to get other things i.e. SAC, DAuids,
        DAmatches = partialPostalCodeToDAuid(postalCode, dictionary).values
        for val in DAmatches:
            listOfPostalCodes.append(postalCode)
            listOfDAs.append(val)
            print("Postal codes processed: %s" % (len(listOfDAs)))
    return listOfPostalCodes, listOfDAs


if __name__ == "__main__":
    
    options = ['DA', 'DBC', 'LATLON']
    attempts = 3
    # Check output selection.
    while attempts <=3:
        option = input("Enter 'DA' to convert to dissemination area, 'DBC' to convert to dissemination block code, or LATLON to latitude/longitude pairs: ")
        if option not in options:
            print("Please try again...")
            attempts -= 1
            print('{} more tries'.format(attempts))
            continue
        else:
            break
        
    # Check input file.
    while True:
        try:
            fileToProcess = input('Enter filepath for postal codes: ')
            postalCode_df = pd.read_csv(input_postal_code_data)
        except FileNotFoundError:
            print('Please enter the correct full filepath')
            continue
        else:
            break

    if option == 'DA':
        listOfPostalCodes, listOfDAs = matchPartialPostalToDA(postalCode_df)
        print("Writing to dataframe...")    
        postalCodes_with_DAs_df = pd.DataFrame({"postalCode": listOfPostalCodes,
                                                    "DA":listOfDAs})
        print("Writing to CSV file...")
        postalCodes_with_DAs_df.to_csv('postalCodes_with_DA.csv', index= False)
    
    elif option == 'DBC':
        listOfPostalCodes, listOfDissBlockCodeMatches = matchPartialPostalToDisBlockCodes(postalCode_df)
        print("Writing to dataframe...")    
        postalCodes_with_DBCs_df = pd.DataFrame({"postalCode": listOfPostalCodes,
                                                    "DBC":listOfDissBlockCodeMatches})
        print("Writing to CSV file...")
        postalCodes_with_DBCs_df.to_csv('postalCodes_with_DBC.csv', index= False)
        
    elif option == 'LATLON':
        print("Matching postal codes to lat lons...")
        listOfPostalCodes = []
        listOfLATLONs = []
        for postalCode in postalCode_df['postalCode'].values:
            try:
                lat, lon = postalCodeToLATLON(postalCode, dictionary)
                lat = lat.to_list()
                lon = lon.to_list()
                for index, value in enumerate(lat):
                    latLon = [float(value), float(lon[index])]
                    listOfPostalCodes.append(postalCode)
                    listOfLATLONs.append(latLon)  
            except ValueError:
                continue
                
        print("Writing to dataframe...")    
        postalCodes_with_LATLONS_df = pd.DataFrame({"postalCode": listOfPostalCodes,
                                                    "latLon":listOfLATLONs})
        print("Writing to CSV file...")
        postalCodes_with_LATLONS_df.to_csv('postalCodes_with_LATLONS.csv', index= False)