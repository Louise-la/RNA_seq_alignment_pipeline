import os
import subprocess
from process_fastq_files import process_fastq_files
from align_with_hisat2 import align_with_hisat2
from trim_and_map_transcripts import trim_and_map_transcripts

def main(gtf_file, genome_index):
    """Process FASTQ files, align with Hisat2, map transcripts using Stringtie, and convert SAM to BAM.

    This script automates the processing of FASTQ files, alignment with Hisat2, mapping of transcripts using Stringtie,
    and conversion of resulting SAM files to BAM format.

    Args:
        gtf_file (str): Path to the GTF file containing genomic annotations.
        genome_index (str): Path to the Hisat2 genome index.

    Raises:
        FileNotFoundError: If any of the input directories or files are not found.
        OSError: If an error occurs during execution.

    Note:
        - This script requires the following modules to be accessible: process_fastq, align_with_hisat2, 
          trim_and_map_transcripts.
        - Ensure that all required modules are either in the same directory as this script or are accessible 
          via Python's module search path.
        - Paths to FASTQ files directory, genome index, GTF file, and the location for BAM output are currently hardcoded.
          Ensure that these paths are updated to reflect the actual locations of the files on your system or provide them
          as arguments to this function for greater flexibility.
    """
    try:
        # Define the directory where the fastq files are stored
        fastq_files_dir = "/path/to/fastq/files"
    
        # Step 1: Process FASTQ files and store the output directory
        trimmed_reads_dir = process_fastq_files(fastq_files_dir)
    
        # Step 2: Align trimmed reads with Hisat2 and store the output directory
        aligned_reads_dir = align_with_hisat2(trimmed_reads_dir, genome_index)
    
        bam_output_dir = os.path.join(os.path.dirname(aligned_reads_dir), "bam")
        os.makedirs(bam_output_dir, exist_ok=True)
        
        for sam_file in os.listdir(aligned_reads_dir):
            if sam_file.endswith(".sam"):
                input_sam = os.path.join(aligned_reads_dir, sam_file)
                output_bam = os.path.join(bam_output_dir, os.path.splitext(sam_file)[0] + ".bam")
                subprocess.run(['samtools', 'view', '-bS', input_sam, '-o', output_bam], check=True)
                
        # Step 3: Trim genome to region of interest and map transcripts using Stringtie
        trim_and_map_transcripts(bam_output_dir, gtf_file)
    except (FileNotFoundError, OSError) as e:
        raise OSError(f"Error during execution: {e}")
