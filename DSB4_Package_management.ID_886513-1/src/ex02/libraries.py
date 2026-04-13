import os 
import subprocess
import sys 
import tarfile

def main():
    env_path = os.environ.get('VIRTUAL_ENV')
    if not env_path:
        raise Exception('Plese activate virtual environment')
    

    libraries = ["beautifulsoup4", "pytest", "requests"]
    with open("temp.txt", 'w', encoding='utf-8') as file:
        for library in libraries:
            file.write(library + '\n')
    

    subprocess.call([sys.executable, '-m', 'pip', 'install', '-r', 'temp.txt'])

    result = subprocess.run([sys.executable, '-m', 'pip', 'freeze'], capture_output=True, text=True)

    with open('requirenments.txt', 'w', encoding='utf-8') as f:
        f.write(result.stdout)
    print(result)
    os.remove("temp.txt")


    tar_name = 'jyanadio.tar.gz'
    with tarfile.open(tar_name, 'w:gz') as tar:
        tar.add(env_path, arcname=os.path.basename(env_path))
    print(f"Environment archived to {tar_name}")

if __name__ == "__main__":
    main()
        