def h5_converter(Filein, return_folder):
    """
    IMPORT PACKAGES
    """
    import h5py
    import numpy as np
    import csv
    from os import path
    from collections import OrderedDict
    """
    GET FILE INFO FROM FILENAME
    """
    # Break Path
    A1 = path.split(Filein)
    # Split Str File Name
    A = A1[-1]
    A = A.split("_")
    # Identify File Type (Peaks or TimeSeries)
    FileType = A[- 1].split(".")[0]
    # Identify Post Processing Type
    PostType = A[-4]

    """
    GET h5 INFORMATION
    """
    with h5py.File(Filein, 'r') as hdf:
        # ____________________ PARENT FILE HANDLING _____________________
        # Get File Attributes
        FileAttributesAll = list(hdf.attrs.keys())
        # Initialize File Attribute List
        FileAttributesAll_values = []
        # Get File Attributes Values
        for k in FileAttributesAll:
            try:
                # How to get group attributes values (decoding needed for bytes-> str)
                FileAttributesAll_values.append(hdf.attrs.__getitem__(k).decode("utf-8"))
            except:
                FileAttributesAll_values.append(hdf.attrs.__getitem__(k))
        # Determine How Many Groups Are In Data
        n = len(list(hdf.keys()))
        # ________________________________________________________________

        if n > 1:
            if 'NLR' in FileType or 'SRR' in FileType:
                if 'NLR' in FileType:
                    # Key List
                    fkeys = list(hdf.keys())[0:len(hdf.keys()) - 3]
                    # Dummy Variable
                    dummy = ['m', 'm', 'm', 'm', 'm', 'm', 'Save Point ID', 'Save Point Latitude', 'Save Point Longitude']
                    # Indexing Variable For Sorting Datasets
                    dIndx = []
                    # Define Units Header
                    units_header = ['', 'deg', 'deg', 'm', 'm', 'm', 'm', 'm', 'm']
                    # Initialize First Header
                    header1 = []
                    # Get Datasets Attributes
                    for k in hdf.keys():
                        if k in fkeys:
                            header1 = np.hstack(
                                (header1, hdf.get(k).attrs.__getitem__(list(hdf.get(k).attrs)[0]).decode("utf-8")))
                        else:
                            dIndx = np.hstack((dIndx, dummy.index(k)))
                    # Fill missing Attributes
                    header1 = np.hstack((['', '', ''], header1))
                    # Reorder Keys
                    fkeys2 = []
                    for k in dIndx:
                        fkeys2 = np.hstack((fkeys2, dummy[int(k)]))
                    fkeys = np.hstack((fkeys2, fkeys))
                elif 'SRR' in FileType:
                    # Get Keys List
                    fkeys = list(hdf.keys())
                    # Get Save Point ID, Lat, Lon
                    data1 = np.array(hdf.get(fkeys[0]))
                    # Initialize First Header
                    header1 = ['Save Point ID', 'Save Point Latitude', 'Save Point Longitude']
                    # Initialize Units Vector
                    header_units = ['', 'deg', 'deg', 'storm/yr/km', 'storm/yr/km']
                    # Redefine Keys
                    fkeys = fkeys[1:]
            else:
                # __________________ GROUP NAMES HANDLING ________________________
                # Get Group Listing
                group_obj = hdf.keys()
                GroupNames = list(hdf.keys())
                # ________________________________________________________________

                # _________________ GROUP 1 ATTRIBUTES HANDLING __________________
                # Access Group 1
                g1 = hdf.get(GroupNames[0])
                # Get Group 1 Items
                g1_items = list(g1.items())
                # Get Group 1 Attributes
                GroupAttributesAll = list(g1.attrs)
                # Initialize Group 1 Attribute List
                GroupAttributesAll_values = []
                # For All Attributes In Group 1 Extract The Corresponding Values
                for k in list(g1.attrs):
                    # How to get group attributes values (decoding needed for bytes-> str)
                    GroupAttributesAll_values.append(g1.attrs.__getitem__(k).decode("utf-8"))
                # ________________________________________________________________

                # _________________ GROUP 1 DATA SET HANDLING ____________________
                # Group 1 Datasets List
                Datasets = list(g1.keys())
                nn = len(Datasets)
                # Initialize Group 1 Dataset Attribute List
                DatasetAttributes = []
                # For All Attributes In Group 1 Dataset Extract The Corresponding Values (units)
                for k in Datasets:
                    try:
                        # Get Group 1 Dataset Attributes
                        DatasetAttributes.append(list(g1.get(k).attrs.values())[-1].decode("utf-8"))
                    except:
                        DatasetAttributes.append('')

                # ________________________________________________________________
        else:
            # ___________ GROUP 1 DATA SET HANDLING (No Groups) ______________
            g1 = hdf.get(list(hdf.keys())[0])
            # Get Group 1 Attributes
            GroupAttributesAll = list(g1.attrs)
            # Initialize Group 1 Attribute List
            GroupAttributesAll_values = []
            # For All Attributes In Group 1 Extract The Corresponding Values
            for k in list(g1.attrs):
                # How to get group attributes values (decoding needed for bytes-> str)
                GroupAttributesAll_values.append(g1.attrs.__getitem__(k).decode("utf-8"))
            # Group 1 Datasets List
            Datasets = list(g1)
            nn = len(Datasets)
            if 'AEP' in FileType:
                # Initialize Group 1 Dataset 1 Attribute List
                DatasetAttributes = []
                # For All Attributes In Group 1 Dataset 1 Extract The Corresponding Values (units)
                for k in Datasets:
                    # Get Group 1 Dataset Attributes
                    DatasetAttributes.append(list(g1.get(k).attrs.values())[-1].decode("utf-8"))
                # Get AEP Values
                AEP = np.array(list(g1.get(Datasets[0]).attrs.values())[0].decode("utf-8").split(','))
                # Convert From Str To Float
                AEP = [float(i) for i in AEP]
                # Define Number Of Entries
                ctr = len(AEP)
                # Reshape AEP Vector
                AEP = np.reshape(AEP, (ctr, 1))
            else:
                # Initialize Group 1 Dataset 1 Attribute List
                DatasetAttributes = []
                # For All Attributes In Group 1 Dataset 1 Extract The Corresponding Values (units)
                for k in Datasets:
                    # Get Group 1 Dataset Attributes
                    DatasetAttributes.append(list(g1.get(k).attrs.values())[-1].decode("utf-8"))
            # ________________________________________________________________
        """
        WRITE CSV FILE 
        """
        # ___________________ CASE 1: TS OR PEAKS NO POST PROCESSING __________________
        if ('TimeSeries' in FileType or 'Peaks' in FileType) and 'Post0' in PostType:
            # Get File Attributes Sorting Index
            header1_order = ['Save Point ID', 'Save Point Latitude', 'Save Point Longitude']
            # Initialize Units Vector (spID, spLat,spLon,spDepth,stName,stID,stType)
            unit_header = ['', 'deg', 'deg', 'm', '', '', '']

            # Initialize Index List
            indx = []
            for k in header1_order:
                # Append Matching Strings To indx Var
                indx.append(FileAttributesAll.index(k))

            # Initialize Data Entries Counter
            ctr = 0
            # Initialize Storm ID, Name, Type Variables
            stmID = []
            stmName = []
            stmType = []
            # Loop Through Groups And Gather Details
            for g in GroupNames:
                # Count Data Entries
                ctr = ctr + len(hdf.get(g).get(Datasets[0]))
                # Store Storm ID Per Group
                stmID = np.hstack((stmID, np.repeat(str(hdf.get(g).attrs.__getitem__('Storm ID').decode("utf-8")),
                                                    len(hdf.get(g).get(Datasets[0])))))
                # Store Storm Name Per Group
                stmName = np.hstack((stmName, np.repeat(str(hdf.get(g).attrs.__getitem__('Storm Name').decode("utf-8")),
                                                        len(hdf.get(g).get(Datasets[0])))))
                # Store Storm Type Per Group
                stmType = np.hstack((stmType, np.repeat(str(hdf.get(g).attrs.__getitem__('Storm Type').decode("utf-8")),
                                                        len(hdf.get(g).get(Datasets[0])))))
            # Reshape To Col Vector
            stmID = np.reshape(stmID, (len(stmID), 1))
            stmName = np.reshape(stmName, (len(stmName), 1))
            stmType = np.reshape(stmType, (len(stmType), 1))

            # Initialize Dictionaries
            Data_Dic = OrderedDict()
            for ds in Datasets:
                # Initialize Dummy Var For Cat Dataset Of All Groups
                dummy = []
                for g in GroupNames:
                    # Cat Group Dataset
                    dummy = np.hstack((dummy, np.array(hdf.get(g).get(ds))))
                # Update Dictionary
                Data_Dic.update({ds: np.reshape(dummy, (len(dummy), 1))})
            # Change Dictionary Key Order For Convenience
            Data_Dic.move_to_end(Datasets[-1], last=False)
            # Save Point ID
            spID = np.zeros((ctr, 1), dtype=int)
            spID[spID == 0] = int(FileAttributesAll_values[indx[0]])
            # Save Point Lat
            spLat = np.zeros((ctr, 1), dtype=float)
            spLat[spLat == 0] = float(FileAttributesAll_values[indx[1]])
            # Save Point Lon
            spLon = np.zeros((ctr, 1), dtype=float)
            spLon[spLon == 0] = float(FileAttributesAll_values[indx[2]])
            # Get Group Attributes Sorting Index
            indx = GroupAttributesAll.index('Save Point Depth')
            # Save Point Depth
            spDepth = np.zeros((ctr, 1), dtype=float)
            spDepth[spDepth == 0] = float(GroupAttributesAll_values[indx])
            # Build Writing Table
            csvTable = np.hstack((spID, spLat, spLon, spDepth, stmName, stmID, stmType))
            # Write Datasets
            for ds in Data_Dic.keys():
                csvTable = np.hstack((csvTable, Data_Dic.get(ds)))
            # ________________________ CSV WRITING ___________________________
            # Open File
            csvfile = open(path.join(return_folder, path.basename(Filein).split('.')[0] + '.csv'), 'w', newline='')
            # Cat Date Header To Existing Header Var
            header1_order = ['Save Point ID', 'Save Point Latitude', 'Save Point Longitude', 'Save Point Depth',
                             'Storm Name', 'Storm ID', 'Storm Type', Datasets[-1]]
            # Cat Date Header To Existing Units Header Var
            unit_header.append(Datasets[-1])
            # Cat Datasets Names To Header
            for ds in Datasets[0:len(Datasets) - 1]:
                header1_order.append(ds)
            # Cat Datasets Units To Header
            for dsA in DatasetAttributes[0:len(Datasets) - 1]:
                unit_header.append(dsA)
            # Create Dummy Row To Keep Consistency With Old Format
            drow = ['', '', '', '', '', '', '', Datasets[-1], '', '', '', '', '', '']
            # Define CSV Writer Handle
            writer = csv.writer(csvfile)
            # Write Header Row
            writer.writerow(header1_order)
            # Write Dummy Row
            writer.writerow(drow)
            # Write Units Row
            writer.writerow(unit_header)
            # Write Datasets
            writer.writerows(csvTable)
            # Close CSV
            csvfile.close()
            # ________________________________________________________________
        # ________________________________________________________________
        # ___________________ CASE 2: PEAKS  POST96RT ____________________
        if 'Peaks' in FileType and 'Post96RT' in PostType:
            # Get File Attributes Sorting Index
            header1_order = ['Save Point ID', 'Save Point Latitude', 'Save Point Longitude']

            # Initialize Index List
            indx = []
            for k in header1_order:
                # Append Matching Strings To indx Var
                indx.append(FileAttributesAll.index(k))

            # Determine Groups Count
            ctr = len(GroupNames)
            # Initialize Storm ID, Name, Type Variables
            stmID = []
            stmName = []
            stmType = []
            # Loop Through Groups And Gather Details
            for g in GroupNames:
                # Store Storm ID Per Group
                stmID = np.hstack((stmID, str(hdf.get(g).attrs.__getitem__('Storm ID').decode("utf-8"))))
                # Store Storm Name Per Group
                stmName = np.hstack((stmName, str(hdf.get(g).attrs.__getitem__('Storm Name').decode("utf-8"))))
                # Store Storm Type Per Group
                stmType = np.hstack((stmType, str(hdf.get(g).attrs.__getitem__('Storm Type').decode("utf-8"))))
            # Reshape To Col Vector
            stmID = np.reshape(stmID, (len(stmID), 1))
            stmName = np.reshape(stmName, (len(stmName), 1))
            stmType = np.reshape(stmType, (len(stmType), 1))
            # Save Point ID
            spID = np.zeros((ctr, 1), dtype=int)
            spID[spID == 0] = int(FileAttributesAll_values[indx[0]])
            # Save Point Lat
            spLat = np.zeros((ctr, 1), dtype=float)
            spLat[spLat == 0] = float(FileAttributesAll_values[indx[1]])
            # Save Point Lon
            spLon = np.zeros((ctr, 1), dtype=float)
            spLon[spLon == 0] = float(FileAttributesAll_values[indx[2]])
            # Get Group Attributes Sorting Index
            indx = GroupAttributesAll.index('Save Point Depth')
            # Save Point Depth
            spDepth = np.zeros((ctr, 1), dtype=float)
            spDepth[spDepth == 0] = float(GroupAttributesAll_values[indx])
            # Build Writing Table
            csvTable = np.hstack((spID, spLat, spLon, spDepth, stmName, stmID, stmType))
            # Initialize Data Matrix
            dateTable = np.zeros((len(GroupNames), 96), dtype=float)
            dataTable = np.zeros((len(GroupNames), 96), dtype=float)
            # Extract Data-sets
            ctr = 0
            for g in GroupNames:
                dataTable[ctr, 0:] = np.array(hdf.get(g).get(Datasets[0]))
                dateTable[ctr, 0:] = np.array(hdf.get(g).get(Datasets[1]))
                ctr = ctr + 1
            # Initialize Combination Matrix
            cTable = np.zeros((len(GroupNames), 1))
            # Cat Elevation Data And Dates In Proper Format
            for ff in range(0, 96):
                cTable = np.hstack([cTable, np.reshape(dateTable[0:, ff], (len(GroupNames), 1)),
                                    np.reshape(dataTable[0:, ff], (len(GroupNames), 1))])
            # Remove Dummy First Col
            cTable = np.delete(cTable, 0, 1)
            # Cat Tables To Write To CSV
            csvTable = np.hstack((csvTable, cTable))
            # ________________________ CSV WRITING ___________________________
            # Open File
            csvfile = open(path.join(return_folder, path.basename(Filein).split('.')[0] + '.csv'), 'w', newline='')
            # Cat Date Header To Existing Header Var
            header1_order = ['Save Point ID', 'Save Point Latitude', 'Save Point Longitude', 'Save Point Depth',
                             'Storm Name', 'Storm ID', 'Storm Type']
            # Initialize Dummy Vars
            ctr = 1
            dummy = []
            # Create Maxele num Header
            for kk in range(0, 96):
                dummy = np.hstack((dummy, ('Maxele' + ' ' + np.str(ctr))))
                ctr = ctr + 1
            # Create Empty List
            dummy2 = list(' ' * 192)
            # Fill Maxele Rows
            dummy2[0:192:2] = dummy
            # Fill Date Rows
            dummy2[1:191:2] = [Datasets[-1]] * 95
            # Finish Creating Header
            header1_order = header1_order + [Datasets[-1]] + dummy2
            # Cat Datasets Units To Header
            unit_header = list(('', 'deg', 'deg', 'm', '', '', '')) + ['', 'm'] * 96
            # Create Dummy Row To Keep Consistency With Old Format
            drow = list(('', '', '', '', '', '', '')) + ['', 'ETAMAX'] * 96
            # Define CSV Writer Handle
            writer = csv.writer(csvfile)
            # Write Header Row
            writer.writerow(header1_order)
            # Write Dummy Row
            writer.writerow(drow)
            # Write Units Row
            writer.writerow(unit_header)
            # Write Datasets
            writer.writerows(csvTable)
            # Close CSV
            csvfile.close()
            # ________________________________________________________________
        # ________________________________________________________________
        # ________________________ CASE 3: AEP  __________________________
        if 'AEP' in FileType:
            # Get File Attributes Sorting Index
            header1_order = ['Save Point ID', 'Save Point Latitude', 'Save Point Longitude']
            # Initialize Index List
            indx = []
            for k in header1_order:
                # Append Matching Strings To indx Var
                indx.append(FileAttributesAll.index(k))
            # Save Point ID
            spID = np.zeros((ctr, 1), dtype=int)
            spID[spID == 0] = int(FileAttributesAll_values[indx[0]])
            # Save Point Lat
            spLat = np.zeros((ctr, 1), dtype=float)
            spLat[spLat == 0] = float(FileAttributesAll_values[indx[1]])
            # Save Point Lon
            spLon = np.zeros((ctr, 1), dtype=float)
            spLon[spLon == 0] = float(FileAttributesAll_values[indx[2]])
            # Create First Header
            header1_order = ['Save Point ID', 'Save Point Latitude', 'Save Point Longitude', 'AEP values',
                             'Parameters'] + Datasets
            # Create Units Header
            unit_header = ['', 'deg', 'deg', '', ''] + DatasetAttributes
            # Read Parameter
            try:
                indx = GroupAttributesAll.index('WL')
            except:
                indx = GroupAttributesAll.index('Hs')
            # Store Parameter Name
            param = np.reshape([GroupAttributesAll[indx]] * ctr, (ctr, 1)).tolist()
            # Read Datasets
            dataTable = np.zeros((ctr, len(Datasets)), dtype=float)
            # Extract Data-sets
            ctr2 = 0
            for g in Datasets:
                dataTable[0:, ctr2] = np.array(g1.get(g))
                ctr2 = ctr2 + 1
            # Cat Tables To Write To CSV
            csvTable = np.hstack((spID, spLat, spLon, AEP, param, dataTable))
            # ________________________ CSV WRITING ___________________________
            # Open CSV
            csvfile = open(path.join(return_folder, path.basename(Filein).split('.')[0] + '.csv'), 'w', newline='')
            # Define CSV Writer Handle
            writer = csv.writer(csvfile)
            # Write Header Row
            writer.writerow(header1_order)
            # Write Units Row
            writer.writerow(unit_header)
            # Write Datasets
            writer.writerows(csvTable)
            # Close CSV
            csvfile.close()
            # ________________________________________________________________
        # ________________________________________________________________
        # ________________________ CASE 4: NLR  __________________________
        if 'NLR' in FileType:
            # Read Data
            ctr = 0
            dataTable = np.zeros((len(hdf.get(fkeys[0])), len(fkeys)), dtype=float)
            for k in fkeys:
                dataTable[0:, ctr] = np.array(hdf.get(k))
                ctr = ctr + 1
            # ________________________ CSV WRITING ___________________________
            # Open CSV
            csvfile = open(path.join(return_folder, path.basename(Filein).split('.')[0] + '.csv'), 'w', newline='')
            # Define CSV Writer Handle
            writer = csv.writer(csvfile)
            # Write Header Row
            writer.writerow(fkeys)
            # Write Header Row
            writer.writerow(header1)
            # Write Units Row
            writer.writerow(units_header)
            # Write Datasets
            writer.writerows(dataTable)
            # Close CSV
            csvfile.close()
            # ________________________________________________________________
        # ________________________________________________________________
        # ________________________ CASE 5: SRR  __________________________
        if 'SRR' in FileType:
            # Get Storm Rates Keys
            g1 = list(hdf.get(fkeys[0]))
            # Initialize Data Vectors
            data2 = np.zeros((len(data1[:, 0]), 2), dtype=float)
            ctr = 0
            # Read High/Low Intensity
            for k in g1:
                data2[0:, ctr] = np.array(hdf.get(fkeys[0]).get(k))
                ctr = ctr + 1
            # Get Storm Probabilities Keys
            g1 = list(hdf.get(fkeys[1]))
            # Initialize Data Vectors
            data3 = np.zeros((len(data1[:, 0]), len(g1)), dtype=float)
            ctr = 0
            # Read Storm Probabilities
            for k in g1:
                data3[0:, ctr] = np.array(hdf.get(fkeys[1]).get(k))
                ctr = ctr + 1
            # Cat Data Matrix
            dataTable = np.hstack((data1, data2, data3))
            # Cat Top Header
            header1 = np.hstack((header1, list(hdf.get(fkeys[0])), list(hdf.get(fkeys[1]))))
            # ________________________ CSV WRITING ___________________________
            # Open CSV
            csvfile = open(path.join(return_folder, path.basename(Filein).split('.')[0] + '.csv'), 'w', newline='')
            # Define CSV Writer Handle
            writer = csv.writer(csvfile)
            # Write Header Row
            writer.writerow(header1)
            # Write Units Row
            writer.writerow(header_units)
            # Write Datasets
            writer.writerows(dataTable)
            # Close CSV
            csvfile.close()
            # ________________________________________________________________
        # ________________________________________________________________
        # __________________ CASE 6: Storm Parameters  ___________________
        if 'Param' in FileType:
            # Get Group Attributes Of Interest
            attrs = ['Storm Name', 'Storm ID', 'Storm Type']
            # Initialize Counters (Row & Col)
            stm_name = []
            stm_ID = []
            stm_type = []
            # Gather Group Attributes
            for g in GroupNames:
                stm_name = np.hstack((stm_name, hdf.get(g).attrs.__getitem__(attrs[0]).decode("utf-8")))
                stm_ID = np.hstack((stm_ID, hdf.get(g).attrs.__getitem__(attrs[1]).decode("utf-8")))
                stm_type = np.hstack((stm_type, hdf.get(g).attrs.__getitem__(attrs[2]).decode("utf-8")))
            # Reshape Vectors
            stm_name = np.reshape(stm_name, (len(stm_name), 1))
            stm_ID = np.reshape(stm_ID, (len(stm_name), 1))
            stm_type = np.reshape(stm_type, (len(stm_name), 1))
            # Finish Creating Header
            attrs = np.hstack((attrs, Datasets))
            # Initialize Attribute Matrix
            data1 = np.zeros((len(GroupNames), len(Datasets)))
            # Initialize Counters (Row & Col)
            ctr1 = 0
            ctr2 = 0
            # Gather Group Datasets
            for g in GroupNames:
                ctr2 = 0
                for k in Datasets:
                    data1[ctr1, ctr2] = np.array(hdf.get(g).get(k))
                    ctr2 = ctr2 + 1
                ctr1 = ctr1 + 1
            # Define Units Header
            header_units = ['', '', '']
            header_units = np.hstack((header_units, DatasetAttributes))
            # ________________________ CSV WRITING ___________________________
            # Open CSV
            csvfile = open(path.join(return_folder, path.basename(Filein).split('.')[0] + '.csv'), 'w', newline='')
            # Define CSV Writer Handle
            writer = csv.writer(csvfile)
            # Write Header Row
            writer.writerow(attrs)
            # Write Units Row
            writer.writerow(header_units)
            # Write Units Row
            writer.writerow(header_units)
            # Write Datasets
            writer.writerows(np.hstack((stm_name, stm_ID, stm_type, data1)))
            # Close CSV
            csvfile.close()
            # ________________________________________________________________
        # ________________________________________________________________
        # __________________ CASE 7: Storm Conditions  ___________________
        if 'STcond' in FileType:
            # Reorganize Attributes
            if len(GroupAttributesAll)>3:
                # TS
                GroupAttributesAll[1] = 'Storm Name'
                GroupAttributesAll[2] = 'Storm ID'
            else:
                # Hurricane
                GroupAttributesAll[0] = 'Storm Name'
                GroupAttributesAll[1] = 'Storm ID'
            # Initialize Attributes Var
            attrs = np.repeat('a', len(GroupAttributesAll))
            # Gather Group Attributes
            for g in GroupNames:
                dummy = []
                for a in GroupAttributesAll:
                    dummy = np.hstack((dummy, hdf.get(g).attrs.__getitem__(a).decode("utf-8")))
                attrs = np.vstack((attrs, dummy))
            # Remove Dummy Row
            attrs = attrs[1:, :]
            # Initialize Datasets Matrix
            data1 = np.zeros((1, len(Datasets)), dtype=float)
            attrs2 = np.repeat('a', len(GroupAttributesAll))
            ctr2 = 0
            # Read Datasets
            for g in GroupNames:
                dummy = np.zeros((len(hdf.get(g).get(Datasets[0])), len(Datasets)), dtype=float)
                ctr = 0
                for ds in Datasets:
                    dummy[0:, ctr] = hdf.get(g).get(ds)
                    ctr = ctr + 1
                data1 = np.vstack((data1, dummy))
                attrs2 = np.vstack((attrs2, np.tile(attrs[ctr2, :], len(hdf.get(g).get(Datasets[0]))).reshape((len(hdf.get(g).get(Datasets[0])), len(GroupAttributesAll)))))
                ctr2 = ctr2 + 1
            # Remove Additional Row
            data1 = data1[1:, 0:]
            attrs2 = attrs2[1:, 0:]
            # Define Units Header
            header_units = np.repeat('', len(GroupAttributesAll))
            header_units = np.hstack((header_units, DatasetAttributes[-1], DatasetAttributes[0:len(DatasetAttributes)-1]))
            header1 = np.hstack((GroupAttributesAll, Datasets[-1], Datasets[0:len(Datasets)-1]))
            # ________________________ CSV WRITING ___________________________
            # Open CSV
            csvfile = open(path.join(return_folder, path.basename(Filein).split('.')[0] + '.csv'), 'w', newline='')
            # Define CSV Writer Handle
            writer = csv.writer(csvfile)
            # Write Header Row
            writer.writerow(header1)
            # Write Units Row
            writer.writerow('')
            # Write Units Row
            writer.writerow(header_units)
            # Write Datasets
            writer.writerows(np.hstack((attrs2, np.reshape(data1[0:, -1], (len(data1[0:, -1]), 1)), data1[0:, 0:len(Datasets)-1])))
            # Close CSV
            csvfile.close()
            # ________________________________________________________________
        # ________________________________________________________________
