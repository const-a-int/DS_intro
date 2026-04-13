import os 

def get_env():
    venv_path = os.environ.get('VIRTUAL_ENV')

    print(f'Your current virtual env is: {venv_path}')
        

if __name__ == '__main__':
    get_env()