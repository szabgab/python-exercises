from __future__ import print_function
import os, sys, importlib
import contextlib

# based on http://stackoverflow.com/questions/5136611/capture-stdout-from-a-script-in-python
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

class Exe(object):
    def check(self):
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
        self.exercise = exercise

        self.main_file = ex_name + '.py'

        if os.environ.get('CM'):
            path = os.path.join(ex_name, 'solution')
            self.main_file = os.path.join(ex_name, 'solution', self.main_file)
            sys.path.insert(0, path)

        if not os.path.exists(self.main_file):
            print("File {} does not exist".format(self.main_file))
            return

        # TODO check other required files
        # TODO convert this to me a class so these methods can inherit??
        # or shall I just use a global exercise object?
        if exercise.is_script:
            res = self.check_script()
        else:
            res = self.check_module()

        if res:
            print('Congratulations. You passed all the checks!')

    def check_script(self):
        import subprocess

        proc = subprocess.Popen([sys.executable, self.main_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        out,err = proc.communicate()
        if out != self.exercise.expected_out:
            print("Expected output:")
            print(self.exercise.expected_out)
            print("Actual output:")
            print(out)
            return False

        if err != self.exercise.expected_err:
            print("Expected error:")
            print(self.exercise.expected_err)
            print("Actual error:")
            print(err)
            return False
        return True


    def check_module():
        try:
            with capture() as out:
                mud = importlib.import_module(ex_name)
        except Exception as e:
            print("Could not load " + ex_name)
            print("It seems the file '{}' cannot be compiled".format(path))
            print('-------------------------')
            print(e)


Exe().check()
