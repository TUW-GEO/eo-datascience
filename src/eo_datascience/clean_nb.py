import os
import nbformat
from pathlib import Path

def clean_up_frontmatter(dir = './notebooks', save=False):
    # Define the path to the notebooks
    nb_paths = find_ipynb(dir)

    # Iterate over the notebooks
    for nb_path in nb_paths:
        # Load the notebook
        nb = nbformat.read(nb_path, as_version=4)
        if nb.cells[0].source.startswith('---'):
            #Load frontmatter
            fm = nb.cells[0].source.split('\n')

            # Extract the title and the subtitle
            title, subtitle = '', ''
            for line in fm:
                if line.startswith('title'):
                    title = line.split(': ')[1]
                if line.startswith('subtitle'):
                    subtitle = line.split(': ')[1]
            
            # Update the cell
            nb.cells[0].source = f'# {title}\n{subtitle}\n'
            
            # Save the notebook
            if save:
                nbformat.write(nb, nb_path)
            else:
                return nb

def convert_refs(dir="./notebooks", save=True):
    nb_paths = find_ipynb(dir)
    
    # Iterate over the notebooks
    for nb_path in nb_paths:
        # Load the notebook
        nb = nbformat.read(nb_path, as_version=4)
        for i in range(len(nb.cells)):
            if i != 0:
                nb.cells[i].source = nb.cells[i].source.replace(r"[@", r"{cite}`").replace(r"]", r"`")
        
        # Save the notebook
        if save:
            nbformat.write(nb, nb_path)
        else:
            return nb

def find_ipynb(dir):
    root = Path(dir).resolve()
    nb_paths = [root / file for file in os.listdir(root) if file.endswith('.ipynb')]
    return nb_paths

def main():
    clean_up_frontmatter()
    convert_refs()

if __name__ == '__main__':
    main()