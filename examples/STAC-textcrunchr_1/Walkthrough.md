# Bombing TextCrunchr1

## Using ACsploit as a triage tool for known vulnerabilities

This example comes from the DARPA STAC program, Engagement 2. The vulnerable java program is contained in textcrunchr1.tar contained in this directory. The textcrunchr tarball contains a description of the challenge program (`description.txt`), the challenge program itself(`challenge_program/bin/textcrunchrhost_1`) as well as some example scripts to help a user interact with the vulnerable program (`examples/`). The challenge question (`Question_021.txt`) that we are trying to answer is reproduced below:

```
Challenge Program:

    textcrunchr_1.jar

Challenge Question:

    Is there an algorithmic complexity vulnerability in time that would cause the challenge
    program's real runtime (on the reference platform) to exceed the resource usage limit
    given the input budget?

Additional background for question:

    None

Input Budget:

    Total size of input file (or files): 400000 bytes
    
Resource Usage Limit
    
    Runtime: 300 seconds
```

So we are looking for a runtime algorithmic complexity vulnerability in the challenge program. 

From `description.txt`, the following line is interesting: 

```
Given a zip, bz2, or tar file that contains text files, TextCrunchr will analyze each file.
```

Since the challenge program accepts compressed files, it's possible a conventional compression bomb will trigger the AC vulnerability.

Let's start by firing up ACSploit and examining the potential exploits.

<img src="../images/STAC-textcrunchr1/acsploitshow.png" class="center"  width="300">

We see exploits for generating zip, gz, or tar.gz bombs. Let's use the zip bomb generator.

<img src="../images/STAC-textcrunchr1/acsploitdescribeoptions.png" class="center"  width="700">

From the exploit option descriptions we see that ACsploit will generate three different types of zip bombs: recursive bombs, single layer boms and layered zip bombs. Let's try out the recursive zip bomb first, naming the file `bomb.zip`. 

<img src="../images/STAC-textcrunchr1/acsploitrun.png" class="center"  width="500">


Checking the generated zip bomb, we see that `bomb.zip` is a measly 400 bytes, well under our input budget. Now that we've generated our bomb, let's try it against textcrunchr1. I moved the newly created `bomb.zip` into the `examples/` directory, and edited the example script as below.

```
$ cat example_basic.sh
#!/bin/sh
../challenge_program/bin/textcrunchrhost_1 ./bomb.zip
```
Now running the example script, we see that the script is taking a little while to return. Will we hit 300 seconds? Checking htop, we see that the java process hits 100% CPU utilization. After 5 minutes, we confirm that the recursive zip bomb achieved the desired AC vulnerability. 

<img src="../images/STAC-textcrunchr1/htop.png" class="center"  width="600">

