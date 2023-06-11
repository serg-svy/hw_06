import os
import shutil
import string


def normalize(name):

    valid_chars = f"-_.() {string.ascii_letters}{string.digits}"
    normalized_name = ''.join(c if c in valid_chars else '_' for c in name)
    return normalized_name


def process_file(file_path):

    extension = file_path.rsplit('.', 1)[-1].lower()
    normalized_name = normalize(file_path)
    destination = ""

    if extension in ['jpeg', 'png', 'jpg', 'svg']:
        destination = 'images'
    elif extension in ['avi', 'mp4', 'mov', 'mkv']:
        destination = 'video'
    elif extension in ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx']:
        destination = 'documents'
    elif extension in ['mp3', 'ogg', 'wav', 'amr']:
        destination = 'audio'
    elif extension in ['zip', 'gz', 'tar']:
        destination = 'archives'
        
        unpack_path = os.path.join(destination, os.path.splitext(normalized_name)[0])
        shutil.unpack_archive(file_path, unpack_path)

    if destination:
        os.makedirs(destination, exist_ok=True)
        new_file_path = os.path.join(destination, normalized_name)
        shutil.move(file_path, new_file_path)


def process_directory(directory):

    for root, dirs, files in os.walk(directory):
        
        dirs[:] = [d for d in dirs if d not in ['archives', 'video', 'audio', 'documents', 'images']]
        for file in files:
            file_path = os.path.join(root, file)
            process_file(file_path)


def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python sort.py <directory>")
        return

    directory = sys.argv[1]
    process_directory(directory)


if __name__ == "__main__":
    main()
