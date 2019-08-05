import os

def create_py_list(path, destination):
    '''
    path (string): path of css file
    destination (string): path of file to save

    reads all lines from a file and makes a python file which has all of them in a list called style
    '''

    plist = os.path.splitext(os.path.basename(os.path.normpath(destination)))[0]
    print(plist)

    declaration = plist+' = """\n'
    lines = [line for line in open(path, 'r', encoding='utf-8')]

    with open(destination, 'w', encoding='utf-8') as f:
        f.write(declaration)
        for line in lines:
            f.write(line)
        f.write('"""')
    
def list_to_file(_list, destination):
    '''
    _list (list): list with strings
    destination (string): path of file to save

    takes a list and writes each item into (destination)
    '''
    with open(destination, 'w') as f:
        for line in _list:
            f.write(line)

if __name__ == "__main__":
    create_py_list('modules/index.html', 'modules/index.py')

    create_py_list('modules/bootstrap.min.js', 'modules/bootstrapjs.py')
    create_py_list('modules/jquery-1.12.4.min.js', 'modules/jquery.py')
    create_py_list('modules/script.js', 'modules/script.py')

    create_py_list('modules/bootstrap.min.css', 'modules/bootstrapcss.py')
    create_py_list('modules/custom-style.css', 'modules/custom_style.py')
