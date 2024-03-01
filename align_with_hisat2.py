import os
import subprocess

def align_with_hisat2(input_dir, genome_index):
    """
    Align trimmed FASTQ files containing 'trimmed' in filenames using Hisat2.
    
    This function aligns trimmed FASTQ files present in the specified input directory
    using the Hisat2 alignment tool. Hisat2 is chosen for its speed and accuracy in aligning
    sequencing reads to reference genomes, making it suitable for various RNA-seq and DNA-seq 
    applications.
    
    Hisat2 is a popular choice for alignment due to its ability to efficiently align 
    sequencing reads, particularly for RNA-seq data, to large reference genomes. The output 
    of Hisat2 alignment is in the Sequence Alignment/Map (SAM) format, which is a standard 
    text-based format for representing alignment information. SAM format is chosen for its 
    versatility and compatibility with downstream analysis tools. 

    The '--dta-cufflinks' option is used with Hisat2 to enable direct output suitable for 
    Cufflinks, which is a downstream analysis tool for transcriptome assembly and quantification.
    This option is essential for generating alignments optimized for Cufflinks analysis.

    
    Args:
        input_dir (str): Path to the directory containing trimmed FASTQ files.
        genome_index (str): Path to the Hisat2 genome index (mm10 genome index in this case).
    
    Raises:
        FileNotFoundError: If input_dir or genome_index does not exist.
        OSError: If an error occurs during alignment.
    Returns:
        str: Path to the output directory where SAM files are saved.
    
    Note:
        - Hisat2 software is required to perform the alignment. Ensure that Hisat2 is installed
        and accessible in your system environment before using this function. To download visit 
        the Hisat2 GitHub repository page: https://github.com/DaehwanKimLab/hisat2
        
    """

    # Check if input_dir exists
    if not os.path.isdir(input_dir):
        raise FileNotFoundError(f"The directory '{input_dir}' does not exist.")

    # Create output directory
    output_dir = os.path.join(os.path.dirname(input_dir), "hisat2_output")
    os.makedirs(output_dir, exist_ok=True)

    # Check if genome_index exists
    if not os.path.isfile(genome_index):
        raise FileNotFoundError(f"The genome index file '{genome_index}' does not exist.")

    try:
        # Iterate over each file in the input directory
        for file in os.listdir(input_dir):
            # Check if the file name contains 'trimmed'
            if 'trimmed' in file:
                # Construct paths for input and output files
                input_file = os.path.join(input_dir, file)
                
                # Extract the base file name without extension
                file_name = os.path.splitext(file)[0]
                # Construct the output SAM file name
                output_sam = os.path.join(output_dir, f"aligned.{file_name}.sam")

                # Run Hisat2 alignment 
                # Use the '--dta-cufflinks' option to enable direct output suitable for Cufflinks
                subprocess.run(['hisat2', '-q', '-p', '2', '--dta-cufflinks', '-x', genome_index,
                                '-U', input_file, '-S', output_sam], check=True)
        return output_dir  # Return the path to the output directory
    
    except OSError as e:
        raise OSError(f"Error during Hisat2 alignment: {e}")
