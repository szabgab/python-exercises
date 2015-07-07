from __future__ import print_function
import os, sys, importlib
import contextlib

@contextlib.contextmanager
def capture():
    import sys
    from cStringIO import StringIO
    oldout,olderr = sys.stdout, sys.stderr
    try:
        out=[StringIO(), StringIO()]
        sys.stdout,sys.stderr = out
        yield out
    finally:
        sys.stdout,sys.stderr = oldout, olderr
        out[0] = out[0].getvalue()
        out[1] = out[1].getvalue()

def check():
    if len(sys.argv) != 2:
        print("Usage: {}  exercise_directory".format(sys.argv[0]))
        return

    ex_name = sys.argv[1]
    ex_name = ex_name.rstrip('/')

    if not os.path.exists(ex_name):
        print("Directory '{}' does not exist".format(ex_name))
        return
    if not os.path.isdir(ex_name):
        print("'{}' is not a directory".format(ex_name))
        return

    sys.path.insert(0, ex_name)
    import exercise

    main_file = ex_name + '.py'
    #print(file)

    if os.environ.get('CM'):
        path = os.path.join(ex_name, 'solution')
        main_file = os.path.join(ex_name, 'solution', main_file)
        sys.path.insert(0, path)

    if not os.path.exists(main_file):
        print("File {} does not exist".format(main_file))
        return

    # TODO check other required files
    # TODO convert this to me a class so these methods can inherit??
    # or shall I just use a global exercise object?
    if exercise.is_script:
        check_script()
    else:
        check_module()

    try:
        with capture() as out:
            mud = importlib.import_module(ex_name)
    except Exception as e:
        print("Could not load " + ex_name)
        print("It seems the file '{}' cannot be compiled".format(path))
        print('-------------------------')
        print(e)



    print('Congratulations. You passed all the checks!')

check()
