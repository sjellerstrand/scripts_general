#! /usr/bin/env python

# Author: Simon Jacobsen Ellerstrand
# Github: sjellerstrand

from sys import *
import os, time, argparse, re
import gzip

parser = argparse.ArgumentParser(description='Re-genotypes half calls to a homozygote genotype in the provided VCF file')
parser.add_argument('-i', '--input', dest='i', help="input file in vcf format [required]", required=True)
parser.add_argument('-o', '--output', dest='o', help="output file [required]", required=True)
args = parser.parse_args()

# Check if the input file is gzipped
if args.i.endswith(".gz"):
    inputF=gzip.open(args.i,'rt')

else:
    inputF=open(args.i,'r')

outputF=open(args.o, 'w')


for Line in inputF:
	# Check if the header section
	if re.match('^#',Line) is None:

		# Get the columns of that line
		columns=Line.strip("\n").split("\t")

		# Add the info to the site
		result=columns[0:9]

		# Get the genotypes
		genotypecolumns=range(9,len(columns))

		# Check each individual if it is a heterozygote
		for ind in genotypecolumns:
			genotype=columns[ind]
			genotype=genotype.split(":")

			# Check genotype field
			if len(str(genotype[0]))!=1:

				if "/" in genotype[0]:
					alleles=genotype[0].split("/")

				elif "|" in genotype[0]:
					alleles=genotype[0].split("|")

				# If the genotype is heterozygous or missing data at one allele, re-genotype or check the allelic balance
				if alleles[0]!=alleles[1]:

					# Re-genotype missing data
					if alleles[0]!="." and alleles[1]==".":
						genotype[0]=alleles[0]+"/"+alleles[0]
						result.append(":".join(genotype))

					elif alleles[0]=="." and alleles[1]!=".":
						genotype[0]=alleles[1]+"/"+alleles[1]
						result.append(":".join(genotype))

					else:
						result.append(":".join(genotype))

				else:
					result.append(":".join(genotype))

			# If haploid genotype
			else:
				result.append(":".join(genotype))

		outputF.write('\t'.join(result)+"\n")

	# If it is a header line, just write it out
	else:
		outputF.write(Line)

inputF.close()
outputF.close()
