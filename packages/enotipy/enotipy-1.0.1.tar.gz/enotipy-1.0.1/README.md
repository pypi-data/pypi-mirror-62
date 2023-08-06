#ENotiPy

###Description
ENotipy is a simple script that emails the users upon code completion or failure.

###Environment Setup
ENotipy requires 4 environment variables to be setup prior to use. These variables
can be set 3 different ways. The first is manually. For a bash shell this would
look something like:

```
export ENOTIPY_EMAIL="dev.notipy@gmail.com"
export ENOTIPY_KEY="SuperSecretPassword"
export ENOTIPY_SMTP="smtp.gmail.com"
export ENOTIPY_PORT="587"
```

The next way is the info file. These commands can also be placed in a file like
the SAMPLE_INFO file provided and passed to the `infoFileEnvSetup(./SAMPLE_INFO)`
function in a script or using `-i=SAMPLE_INFO` as a command line argument.

The final way is to request environment setup prompts. This can be done with
`requestEnvSetup()` in a script or `-r=True` on the command line.

For examples of these options, checkout `scriptExample` and `codeExample.py`

**Note that to use strictly "enotipy" on the commandline that the package must be installed via pip. Otherwise, replace "enotipy" with "python /path/to/enotipy.py".**


###Script Examples
####commands:
To access the help menu you can invoke

```bash
enotipy -h #Brings up help menu
```

Environment set up can be done with prompts by as

```bash
enotipy "python scriptCodeExample.py" -r=True #Execute with env setup request
```

or using an info file as

```bash
enotipy "python scriptCodeExample.py" -i=SAMPLE_INFO #Execute with env setup info file
```

If you want to use a sample info file `SAMPLE_INFO` use

```bash
enotipy -g #Generates SAMPLE_INFO
```

The command can also be given a timeout time in minutes

```bash
enotipy "python scriptCodeExample.py" -t=60 #timeout after 60 minutes
```

####scriptExampleCode.py:
```python
def test_fcn(*args):
    x, = args;
    for i in range(x):
        print(i)

if __name__ == "__main__":
    test_fcn(100)
```

###Code Example
If you want to use ENotipy in a code it can be used as

```python
import enotipy.enotipy as enotipy
if __name__ == "__main__":
    #The function to be executed
    def test_fcn(*args):
        x, = args;
        for i in range(x):
            print(i)

    # notipy.requestEnvSetup() #This option requests user input to set environment
    args = (10,)
    enotipy.infoFileEnvSetup("./INFO") #This option sets the environment with an info file
    # enotipy.infoFileEnvSetup("./SAMPLE_INFO") #This option sets the environment with an info file
    notifier = enotipy.ENotiPy() #Creating notipy object
    notifier.run(test_fcn,*args) #Calling run to execute the function and send email when completed.
```
