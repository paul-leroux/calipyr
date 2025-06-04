# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/




# Steps starting our the CaliPyr project

# Make sure all the usual packages are installed
# In the Pycharm Terminal [Alt+F12] run:
(.venv) C:\Python\Projects\CaliPyr git:[master]
python.exe -m pip install --upgrade pip
pip install numpy pandas



# Change from master (local) to main branches before first commit
git branch -m master main
git push -u origin main
git remote add origin https://github.com/paul-leroux/calipyr.git
git remote -v

git add .
git commit -m "Initial commit"
git push -u origin main