import os


def remove_pdf_files(directory):
    # Iterate through each group in the main directory
    for group in os.listdir(directory):
        group_path = os.path.join(directory, group)

        # Check if the path is a directory
        if os.path.isdir(group_path):
            # Iterate through each file in the group directory
            for filename in os.listdir(group_path):
                if filename.endswith('.pdf'):
                    file_path = os.path.join(group_path, filename)
                    try:
                        os.remove(file_path)
                        print(f'Removed: {file_path}')
                    except Exception as e:
                        print(f'Error removing {file_path}: {e}')


# Specify the path to the posters directory
# Change this to your actual path if necessary
posters_directory = r'C:\Users\paulm\Downloads\CSC-510-Fall2024-ProjectPosters-main\CSC-510-Fall2024-ProjectPosters-main\Posters'
remove_pdf_files(posters_directory)
