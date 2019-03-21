# Exploiting PHP Hash Collisions with ACsploit 

## Using ACsploit to create a PoC for PHP 5

A major design goal of ACsploit was to bridge as much of the gap between vulnerability discovery and exploitation as 
possible. In this example we build a working exploit for a real-world attack using ACsploit, based only on a high level 
description of the vulnerability.

In late 2011 Alexander Klink and Julian Wälde noted algorithmic complexity vulnerabilities in the hash functions of 
several popular web-based platforms. In short, these platforms utilized hash functions vulnerable to practical pre-image
attacks. Among these functions was the default PHP hash function. Thus, while their findings led to several CVEs and
security patches, for our demonstration we have chosen their attack on the PHP scripting language. PHP stores variables 
from `POST` requests in a hash table and so a `POST` request with a large number of variables that have colliding hashes 
will cause poor runtime behavior and will spike CPU utilization to 100% (efficiently producing a DOS with a relatively 
small payload).

For this example, we select PHP version 5.3.8 running behind Apache 2.2, but any version of PHP 5 below 5.3.8 is 
vulnerable. (The vulnerability was [patched](http://svn.php.net/viewvc?view=revision&revision=321040) in PHP 5.3.9.) 
We've included a `Dockerfile` in this directory that will start a vulnerable PHP 5.3.8 instance. To start the server and
view its CPU usage in `htop` run the following commands:

```
docker build -t php538 .
docker run -it -p 80:80 php538
```

From the description given in the CVE we know that our payload will be a malicious `HTTP POST` request. We also know 
that we want it to contain a list of variables that share the same PHP hash value. Let's begin by building a list of 
colliding PHP hash pre-images using ACsploit.

We start ACsploit and examine the available exploits. 

<img src="images/ACsploitOptions.png" class="center" width="300">

After selecting `hashes/collisions/php5_fast` as our module, we set our `options`.

We first examine the exploit options and set some necessary parameters. We found that 40,000 collisions is a good number 
to achieve an observable effect so we set `exploit.n_collisions` to `40000`. This should hang the CPU for 15-30 seconds,
which more than suffices for a proof of concept. (We can go back and increase the number of collisions for a larger 
effect.) We note that the `hash\_table\_size` is already set to `2^32`, which covers all integer values in PHP. 

Note that we leave the `input` generator set to `char`. This may seem unintuitive because the output will be a set of
strings, but the exploit generates its collisions by manipulating and combining individual characters, and so must be 
given individual characters to work with. By default, the `char` input generator will use only lowercase letters.

We want to send our input to a web server so we set `output` to `http`. We set `output.url` to our target: 
`http://127.0.0.1/post.php`, which leads to a simple PHP file we added to the running Docker container. The file accepts
`POST` requests, so we set `output.http_method` to `POST`. We want to submit our collisions as parameters in the body of
the request. To do this, we set `output.use_body` to `True` and run `set output.separator custom =&` to chain together
the collisions. Finally, we set `output.content_type` to `application/x-www-form-urlencoded; charset=utf-8`.

<img src="images/ACsploitSetOptions.png" class="center" width="400">

We re-examine our options. Everything looks fine, so we are ready to run our exploit with `run`. Generating 40,000 
collisions takes about 60 seconds, after which you should see one CPU in the Docker container spike to near 100% for 
15-30 seconds.

<img src="images/PHPCPU.png" class="center" width="800" >

Repeating this exercise with the `java_fast` exploit will not produce the same effect, demonstrating that the PHP 
collisions cause the CPU spike, not simply the size of the generated payload.
