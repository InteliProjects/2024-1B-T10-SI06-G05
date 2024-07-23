import nbformat
from nbconvert import PythonExporter

# Nome do seu notebook
notebook_filename = 'notebook_final.ipynb'

# Leia o notebook
with open(notebook_filename) as f:
    nb = nbformat.read(f, as_version=4)

# Use o PythonExporter para converter o notebook para um script Python
exporter = PythonExporter()
script, _ = exporter.from_notebook_node(nb)

# Nome do arquivo de saída
script_filename = notebook_filename.replace('.ipynb', '.py')

# Escreva o script Python
with open(script_filename, 'w') as f:
    f.write(script)

print(f'Notebook convertido para {script_filename}')
