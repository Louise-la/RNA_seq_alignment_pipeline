# RNA-Seq Pipeline

RNA-Seq Pipeline is a tool for automating the processing of RNA-Seq data, including trimming of FASTQ files, alignment with Hisat2, mapping of transcripts using Stringtie, and conversion of resulting SAM files to BAM format.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Introduction

RNA-Seq Pipeline is designed to streamline the analysis of RNA sequencing data, providing a comprehensive workflow for processing raw sequencing files and obtaining aligned reads and mapped transcripts. By automating these tasks, the pipeline reduces manual effort and ensures consistency in data processing.

**Note**: This pipeline was developed specifically for analyzing RNA-Seq data related to the mouse Dcx gene. It may require modifications for use with other genes or organisms.


## Installation

To install and set up the RNA-Seq Pipeline, follow these steps:

1. Clone the repository:
   git clone https://github.com/Louise-la/RNA-seq-alignment-pipeline.git

2. Navigate to the project directory:
    cd rna-seq-pipeline

3. Install dependencies:
    pip install -r requirements.txt

To use the RNA-Seq Pipeline, you need to provide the paths to the GTF file containing genomic annotations and the Hisat2 genome index. You can then execute the main script to run the pipeline.

# Example usage of the main function
from main import main

gtf_file = "/path/to/genomic_annotations.gtf"
genome_index = "/path/to/hisat2_genome_index"

try:
    main(gtf_file, genome_index)
except OSError as e:
    print(f"Error: {e}")
Dependencies

The RNA-Seq Pipeline requires the following dependencies:

Python (>=3.6)
cutadapt (3.5)
Hisat2 (2.2.1)
Stringtie (2.1.4)
Contributing

Contributions to the RNA-Seq Pipeline are welcome! If you encounter any bugs, have suggestions for improvements, or would like to contribute code, please open an issue or submit a pull request on GitHub.

License

This project is licensed under the MIT License - see the LICENSE file for details.

Make sure to update the paths to the GTF file and Hisat2 genome index accordingly. You can also add more detailed information or sections as needed for your project.

