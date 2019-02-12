import unittest
import tempfile
import os
import re

sample_file = """Assay,TruSeq Nano DNA,,,,,,,,,
Index Adapters,TruSeq DNA CD Indexes (96 Indexes),,,,,,,,,
Chemistry,Amplicon,,,,,,,,,
,,,,,,,,,,
[Reads],,,,,,,,,,
76,,,,,,,,,,
76,,,,,,,,,,
,,,,,,,,,,
[Settings],,,,,,,,,,
Adapter,AGATCGGAAGAGCACACGTCTGAACTCCAGTCA,,,,,,,,,
AdapterRead2,AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT,,,,,,,,,
,,,,,,,,,,
[Data],,,,,,,,,,
Sample_ID,Sample_Name,Sample_Plate,Sample_Well,Index_Plate_Well,I7_Index_ID,index,I5_Index_ID,index2,Sample_Project,Description
P3G12-S1PC_4,,,,G12,D712,AGCGATAG,D507,ACGTCCTG,,
P3H12-S1CA_2,,,,H12,D712,AGCGATAG,D508,GTCAGTAC,,
P4E01-S1VA_2,,,,E01,D701,ATTACTCG,D505,CTTCGCCT,,
P4F01-S1PA_2,,,,F01,D701,ATTACTCG,D506,TAAGATTA,,
P4G01-C1LA_3,,,,G01,D701,ATTACTCG,D507,ACGTCCTG,,
P4H01-C2LC_2,,,,H01,D701,ATTACTCG,D508,GTCAGTAC,,
P4E02-C2LB_1,,,,E02,D702,TCCGGAGA,D505,CTTCGCCT,,
P4F02-S2LB_3,,,,F02,D702,TCCGGAGA,D506,TAAGATTA,,
P4G02-R2NA_4,,,,G02,D702,TCCGGAGA,D507,ACGTCCTG,,
P4H02-S1NA_1,,,,H02,D702,TCCGGAGA,D508,GTCAGTAC,,
P4E03-C1NB_1,,,,E03,D703,CGCTCATT,D505,CTTCGCCT,,
P4F03-C1LB_3,,,,F03,D703,CGCTCATT,D506,TAAGATTA,,
P4G03-R1VA_3,,,,G03,D703,CGCTCATT,D507,ACGTCCTG,,
P4H03-S2CB_2,,,,H03,D703,CGCTCATT,D508,GTCAGTAC,,
P4E04-S2VB_2,,,,E04,D704,GAGATTCC,D505,CTTCGCCT,,
P4F04-C2LC_4,,,,F04,D704,GAGATTCC,D506,TAAGATTA,,
P4G04-C2LB_2,,,,G04,D704,GAGATTCC,D507,ACGTCCTG,,
"""


def read_samplesheet():
    new_file, filename = tempfile.mkstemp()
    fh = open(filename, 'w')
    fh.write(sample_file)
    fh.close()
    fh = open(filename, 'r')
    lines = fh.readlines()
    lines = list(map(lambda line: line.rstrip(), lines))
    pass


class MyTest(unittest.TestCase):
    def test(self):
        self.assertEqual(3, 3)
