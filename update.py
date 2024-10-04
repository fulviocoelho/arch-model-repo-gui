import os
import shutil

root_folder = os.getcwd()

if os.path.exists(os.path.join(root_folder, 'run.exe')):
    os.remove('./run.exe')

os.system('git pull origin main')
os.system('yarn build-run')
shutil.copyfile(os.path.join(root_folder, 'dist', 'run.exe'), os.path.join(root_folder, 'run.exe'))