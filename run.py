import os
import shutil

root_folder = os.getcwd()
app_path = os.path.join(root_folder, 'app.py')

if not os.path.exists(app_path):
    os.system('git init')
    os.system('git remote add origin https://github.com/fulviocoelho/arch-model-repo-gui.git')
    os.system('git pull origin main')

if os.path.exists(app_path):
    os.system('git pull origin main')
    os.system('yarn setup')
    shutil.copyfile(os.path.join(root_folder, 'dist', 'update.exe'), os.path.join(root_folder, 'update.exe'))
    os.system("python ./app.py")

# os.remove(os.path.join(root_folder, 'run.exe'))