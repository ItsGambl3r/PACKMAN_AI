import os

def get_largest_checkpoint(directory):
    checkpoint_files = [filename for filename in os.listdir(directory) if filename.startswith("neat-checkpoint-")]
    if not checkpoint_files:
        return None

    # Extract the numbers from checkpoint filenames and find the largest one
    checkpoint_numbers = [int(filename.split("-")[-1]) for filename in checkpoint_files]
    largest_number = max(checkpoint_numbers)

    # Construct the filename of the largest checkpoint file
    largest_checkpoint_file = f"neat-checkpoint-{largest_number}"

    return os.path.join(directory, largest_checkpoint_file)