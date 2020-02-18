import os, sys

CondorScript = """
universe = vanilla

notify_user = ishand@cs.utexas.edu
Notification = Error
Requirements = InMastodon

getenv = true

Initialdir = %s
Executable = %s

%s

+Group   = "GRAD"
+Project = "AI_ROBOTICS"
+ProjectDescription = "LARG Research"

Arguments = %s
Queue
"""

OutputLine = """
Error = %s.err.$(Process)
Output = %s.err.$(Process)
Log = results.$(Process).log
"""

RawExecutable = sys.argv[1]
OutputFile = '/scratch/cluster/ishand/results/' + sys.argv[-1]

arguments = ' '.join(sys.argv[2:-1])

Executable = os.popen('/bin/which %s' % RawExecutable).read()
CurrentDir = '.'

# remove path information
SafeOutputFile = OutputFile.split('/')[-1]

if OutputFile == "/dev/null":
    outputlines = ""
else:
    outputlines = OutputLine % (OutputFile, OutputFile)  # SafeOutputFile

    condor_file = '/tmp/%s.condor' % (SafeOutputFile)
    f = open(condor_file, 'w')
    f.write(CondorScript % (CurrentDir, Executable, outputlines, arguments))  # , sys.argv[4], sys.argv[5], sys.argv[6]))
    f.close()

    os.popen('/lusr/opt/condor/bin/condor_submit %s' % condor_file)

