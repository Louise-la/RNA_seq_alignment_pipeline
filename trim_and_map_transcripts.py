import os
import subprocess

def trim_and_map_transcripts(input_dir, gtf_file):
    """Trim genome to region of interest using gene name of Dcx and map transcripts using Stringtie.

    This function trims the genome to the region of interest specified by the Dcx gene name in the provided GTF file.
    It then maps transcripts from alignment to the Dcx region of the genome using Stringtie, capturing transcripts 
    that cover this region. Finally, it merges the transcripts obtained from the alignment into a single GTF file.

    Args:
        input_dir (str): Path to the directory containing sorted BAM files.
        gtf_file (str): Path to the GTF file containing the region of interest (Dcx gene).

    Raises:
        FileNotFoundError: If input_dir or gtf_file does not exist.
        OSError: If an error occurs during execution.

    Returns:
        str: Path to the output directory where mapped transcripts are saved.

    Note:
        - This function is specifically tailored for the DCX gene. To adapt it for other genes:
            1. Replace the gene name 'ENSMUSG00000031285' with the appropriate gene name in the 'awk' command.
            2. Modify the 'dcx_gtf' variable to specify the output GTF file name accordingly.
            3. Ensure that the gene name specified in step 1 matches the gene name in the 'G' option of Stringtie commands.
            4. Adjust any other parameters or file names as necessary for your specific gene of interest.
        - StringTie is a transcriptome assembly and quantification tool. Ensure that StringTie is installed 
          and accessible in your system environment. You can obtain StringTie from the following link: 
          https://ccb.jhu.edu/software/stringtie/
        - The GTF file containing the genomic annotations for the organism of interest can be obtained from 
          resources such as the GENCODE project (https://www.gencodegenes.org/) or Ensembl (https://www.ensembl.org/).
    """

    # Check if input_dir exists
    if not os.path.isdir(input_dir):
        raise FileNotFoundError(f"The directory '{input_dir}' does not exist.")

    # Check if the GTF file exists
    if not os.path.isfile(gtf_file):
        raise FileNotFoundError(f"The file '{gtf_file}' does not exist.")

    # Get the parent directory of input_dir
    output_dir = os.path.join(os.path.dirname(input_dir), "mapped_transcripts")
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Step 1: Trim genome to region of interest using gene name of Dcx
        dcx_gtf = os.path.join(output_dir, "Dcx.gtf")
        with open(dcx_gtf, 'w') as dcx_gtf_file:
            subprocess.run(['awk', '$8 == "ENSMUSG00000031285"', gtf_file], stdout=dcx_gtf_file, check=True)

        # Step 2: Map transcripts from alignment to Dcx region of Genome using Stringtie
        for bam_file in os.listdir(input_dir):
            if bam_file.endswith(".bam"):
                input_bam = os.path.join(input_dir, bam_file)
                output_prefix = os.path.splitext(bam_file)[0]

                covered_transcripts_gtf = os.path.join(output_dir, f"covered_transcripts_{output_prefix}.gtf")
                subprocess.run(['stringtie', input_bam, '-G', dcx_gtf, '-C', covered_transcripts_gtf, '-l', output_prefix],
                               check=True)

        # Step 3: Merge transcripts
        assembly_gtf_list = os.path.join(output_dir, "assembly_gtf_list.txt")
        with open(assembly_gtf_list, 'w') as f:
            for gtf_file in os.listdir(output_dir):
                if gtf_file.startswith("covered_transcripts_") and gtf_file.endswith(".gtf"):
                    f.write(os.path.join(output_dir, gtf_file) + '\n')

        merged_transcripts_gtf = os.path.join(output_dir, "ref_merged_transcripts.gtf")
        subprocess.run(['stringtie', '--merge', '-G', dcx_gtf, '-o', merged_transcripts_gtf, assembly_gtf_list], check=True)

        # Step 4: Map transcripts from alignment to merged transcripts
        for bam_file in os.listdir(input_dir):
            if bam_file.startswith("sorted.") and bam_file.endswith(".bam"):
                input_bam = os.path.join(input_dir, bam_file)
                output_prefix = os.path.splitext(bam_file)[0]

                covered_transcripts_gtf = os.path.join(output_dir, f"covered_transcripts_{output_prefix}.gtf")
                subprocess.run(['stringtie', input_bam, '-G', merged_transcripts_gtf, '-C', covered_transcripts_gtf, '-l', output_prefix],
                               check=True)
        return output_dir  # Return the path to the output directory

    except OSError as e:
        raise OSError(f"Error during trimming and mapping transcripts: {e}")
