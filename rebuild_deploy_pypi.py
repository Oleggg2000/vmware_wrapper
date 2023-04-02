from os import system, environ
from pathlib import Path
from shutil import rmtree

ROOT_DIR = Path(__file__).parent

def del_folders():
    rmtree(ROOT_DIR / 'build', ignore_errors=True)
    rmtree(ROOT_DIR / 'dist', ignore_errors=True)
    rmtree(ROOT_DIR / 'vmware_wrapper.egg-info', ignore_errors=True)

if __name__ == '__main__':
    del_folders()
    system('py setup.py sdist build')
    system(f'twine upload -u Oleggg2000 -p {environ["PYPI_PASS"]} --verbose dist/*')
    del_folders()
