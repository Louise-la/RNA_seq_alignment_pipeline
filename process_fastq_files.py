import os
import subprocess
import cutadapt

def process_fastq_files(fastq_dir):
    """Process paired-end FASTQ files in the specified directory by trimming 
    Illumina adapter sequences.

    This function trims Illumina adapter sequences from paired-end FASTQ files
    using the 'cutadapt' tool. Paired-end reads are commonly generated by sequencing
    platforms like Illumina, where each sequencing run produces two FASTQ files 
    containing forward and reverse reads, respectively. The adapter sequences are
    removed to ensure high-quality downstream analysis, as adapter contamination can
    affect read alignment and interpretation.
    
    After trimming, the processed reads are saved with the prefix "trimmed." added to 
    the original file name. Additionally, the reverse reads are compressed using gzip 
    compression to reduce file size and storage requirements.


    Args:
        fastq_dir (str): The directory containing FASTQ files to process.

    Returns:
        str: Path to the output directory where trimmed files are saved

    Raises:
        FileNotFoundError: If the specified directory does not exist.
        OSError: If an error occurs while accessing or processing files.

    Note:
        - This function assumes that paired-end FASTQ files are named 
          consistently, with "_1.fastq" and "_2.fastq" suffixes for 
          forward and reverse reads, respectively.
        - The 'cutadapt' tool/library is used for adapter trimming. Ensure that
          'cutadapt' is installed and accessible in the system environment. You can 
          install it via pip: 'pip install cutadapt'. 
        - The adapter sequences used for trimming are common Illumina 
          adapter sequences. If your data comes from a different sequencing
          platform or uses different adapters, you may need to adjust these
          sequences accordingly.
    """
    # Confirm if the input directory exists
    if not os.path.isdir(fastq_dir):
        raise FileNotFoundError(f"The directory '{fastq_dir}' does not exist.")
    
    # Create a directory for the trimmed files to be stored
    output_dir = os.path.join(os.path.dirname(fastq_dir), "FASTQ_output")
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Iterate over each file ending with "_1.fastq" in the directory
        for file in os.listdir(fastq_dir):
            # Extract the file name without the "_1.fastq" extension
            if file.endswith('_1.fastq'):
                file_name = file[:-len('_1.fastq')]  # Remove the '_1.fastq' suffix
                input_1 = os.path.join(fastq_dir, file)
                input_2 = os.path.join(fastq_dir, f"{file_name}_2.fastq")  # Directly append '_2.fastq'
                output_1 = os.path.join(output_dir, f"trimmed.{file_name}_1.fastq")
                output_2 = os.path.join(output_dir, f"trimmed.{file_name}_2.fastq.gz")  # Append '.gz' for gzip compression
                # Generate the command to execute cutadapt
                cutadapt_command = [
                    'cutadapt',
                    '-a', 'AGATCGGAAGAGCACACGTCTGAACTCCAGTCA',
                    '-A', 'AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT',
                    '-o', output_1,
                    '-p', output_2,
                    input_1,
                    input_2
                ]
                
                # Execute cutadapt command using subprocess
                subprocess.run(cutadapt_command, check=True)
            
        return output_dir  # Return the path to the output directory

    # If an error occurs while accessing or processing files:
    except OSError as e:
        raise OSError(f"Error processing FASTQ files in '{fastq_dir}': {e}")
