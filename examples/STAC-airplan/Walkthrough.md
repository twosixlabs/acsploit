# Bombing TextCrunchr1

## Using ACsploit to identify and exploit vulnerabilities

`AirPlan` is a set of programs from Engagement 2 of the DARPA STAC program. (The STAC program, which birthed ACsploit, presents its performers with a series of Java programs containing algorithmic complexity vulnerabilities and challenge questions that specify the conditions under which the vulnerabilities must be exploited.) In this example we use ACsploit to identify and exploit a vulnerability.

The `airplan_1.tar` and `airplan_5.tar` archives in this directory contains a description of the challenge program (`description.txt`), the challenge program itself(`challenge_program/bin/airplan_1`) as well as some example scripts to help a user interact with the vulnerable program (`examples/`). You can use these to follow along with this walkthrough at home.

The challenge question (the same question for `Question_051.txt`, `Question_052.txt`) that we are trying to answer is reproduced below:

```
Challenge Program:

        airplan_[1,5].jar

Challenge Question:

        Is there an algorithmic complexity vulnerability in space
        that would cause the challenge program's memory usage to
        exceed the resource usage limit given the input budget?

Additional background for question:

        The AirPlan application can support multiple users. For
        the purpose of this question assume there is only one user
        connected to the server at any one time.

Input Budget:

        Maximum sum of the PDU sizes of the application requests sent from
        the user to the server: 25,000 bytes

Resource Usage Limit:

        Available Memory: 1024 MB (total memory usage of the JVM shown 
        under the RSS column in pmap -x <PID>)
```

From this that we are looking for a runtime algorithmic complexity vulnerability in space in the challenge program. 

We note from `examples/Route_Map_Formats.txt` that a user can upload files in plaintext, XML, and JSON formats.

Since the challenge program accepts XML files, it's possible a conventional XML bomb will trigger the AC vulnerability.

Let's start by firing up ACsploit and examining the potential exploits with `show`.

We will try the `bombs/xml/billion_laughs` exploit to generate an XML bomb.

From the exploit option descriptions we see that ACsploit can generate XML bombs with varying memory impact. We are targeting 1024 MB of total memory usage.

<img src="images/STAC-airplan/acsploitdescribeoptions.png" class="center"  width="700">

Let's round up the memory_impact to 1100, name the file `bomb.xml`, and run the exploit.

<img src="images/STAC-airplan/acsploitrun.png" class="center" width="500">

Checking the generated zip bomb, we see that `bomb.xml` is only 779 bytes, well within our input budget of 25,000 bytes. Now that we've generated our bomb, let's try it out! We move `bomb.xml` into the `examples/` directory and edit `example_xmlmap.sh` as shown below to throw the bomb at `AirPlan_1`.

```
$ cat example_xmlmap.sh
#!/bin/sh


./login.sh usr pwd

# upload a route map
curl -s -b cookies.txt -F file=@bomb.xml -F "route_map_name=test" --insecure https://localhost:8443/add_route_map

# view it
curl -s -L -b cookies.txt --insecure https://localhost:8443/passenger_capacity_matrix/1553932502
```

We start the AirPlan server by running `start_server.sh` in the `challenge_program` directory, then we launch our XML bomb by running our modified `example_xmlmap.sh`.
When we run this modified example script, we see an error because we have not uploaded a valid route map to the AirPlan server. But did our attack impact the server's memory usage? Checking `htop`, we see that the Java process for `AirPlan_1` is below 100 MB of memory usage, so it seems AirPlan_1 may not be vulnerable to XML bombs.

Similar programs might still be vulnerable to XML bombs. Let's try the same attack against AirPlan_5. Copy `example_xmlmap.sh` and `bomb.xml` into the airplan_5 `examples/` directory. Kill the airplan_1 server, run the airplan_5 `start_server.sh` script, and laaunch our attack with `example_xmlmap.sh`. 
This time, we get the same invalid route map error, but `htop`shows the JVM memory usage far exceeding our target value of 1024 MB.

Note that the memory_impact refers to the approximate size of the expanded XML file, not the actual memory usage of a vulnerable XML parser. We can expect the memory usage to be at least as large as memory impact, but, as is the case here, it may be much larger.
 
<img src="images/STAC-airplan/htop.png" class="center"  width="600">
