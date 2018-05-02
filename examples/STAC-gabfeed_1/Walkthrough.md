# GabFeed Line Break Exploit

## The problem

```
Challenge Program:

    gabfeed_1.jar

Challenge Question:

    Is there an algorithmic complexity vulnerability in time that would cause the challenge
    program's real runtime (on the reference platform) to exceed the resource usage limit
    given the input budget?

Additional background for question:

    GabFeed is a web based application that supports multiple users, however, this question 
    assumes there is only one user interacting with the system in any vulnerability demonstration. 

Input Budget:

    Maximum sum of the PDU sizes of the HTTP requests sent from the user to the server: 
    400000 bytes
    
Resource Usage Limit:

    Runtime: 300 seconds measured as the time interval between sending the last byte of the 
    attack and the server sending the last byte of the response.
```

## The vulnerability

GabFeed contains a naive line breaking algorithm that, when given a string containing many 'words' (ie tokens separated by whitespace), takes an exploitably long time.

### Generating the string

We load up ACsploit and use the `strings/line_breaking` algorithm to generate a string that fits comfortably within the input budget (280000 < 400000) but will occupy GabFeed for more than the time limit and save that string to a file (`gabfeed.dat`).

<img src='images/1.png'>

We then start the GabFeed server…

<img src='images/2.png'>

…and launch our exploit against it with a script that sends the data in the `gabfeed.dat` file we generated at the server.

<img src='images/3.png'>

Timing our attack, we see that we've kept the server busy for over 7 minutes, well over the target of 5 minutes (300 seconds).

<img src='images/4.png'>
