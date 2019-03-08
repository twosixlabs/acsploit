Worst Case Examples
=======================================================================

Hash Collisions
------------------------
Hash collisions occur when a hash function produces an identical `hash` for two or more different inputs.

### Adler32

#### Collision example
Consider to the strings `30>1&` and `30<5$`. Using the adler32 hash function on each string, compute the hash.
```
Char   ASCII Value          A                  B
======================================================
3         51          1 + 51 = 52         0 + 52 = 52
0         48         52 + 48 = 100      52 + 100 = 152
>         62        100 + 62 = 162     152 + 162 = 314
1         49        162 + 49 = 211     314 + 211 = 525
&         38        211 + 38 = 249     525 + 249 = 774

249 to hex = 0xf9
774 to hex = 0x306

Hash value: 0x030600f9 = 0x306 << 16 + 0xf9


Char   ASCII Value          A                  B
======================================================
3         51          1 + 51 = 52         0 + 52 = 52
0         48         52 + 48 = 100      52 + 100 = 152
<         60        100 + 60 = 160     152 + 160 = 312
5         53        160 + 53 = 213     312 + 213 = 525
$         36        213 + 36 = 249     525 + 249 = 774

249 to hex = 0xf9
774 to hex = 0x306

Hash value: 0x030600f9 = 0x306 << 16 + 0xf9
```

### BSD Checksum

####  Example 16-bit checksum in python
```
def BSD_checksum(data):
    checksum = 0
    for i in data:
        checksum = (checksum >> 1) + ((checksum & 1) << 15)
        checksum += ord(i)
        checksum &= 0xffff
    return checksum

print("Checksum:", BSD_checksum("Xy+Dyu"))
```
#### Collision example
Consider to the strings `Xy+Dyu` and `Xy1Eyt`. Using the BSD checksum function on each string, compute the 16 bit hash. Both strings result in the same hash.


```
   Checksum          Circular shift        Add the checksum and character value, then perform bitmask
0000000000000000 => 0000000000000000              0 +  88 =    88 =>    88 & 0xffff = 88
0000000001011000 => 0000000000101100             44 + 121 =   165 =>   165 & 0xffff = 165
0000000010100101 => 1000000001010010          32850 +  43 = 32893 => 32893 & 0xffff = 32893
1000000001111101 => 1100000000111110          49214 +  68 = 49282 => 49282 & 0xffff = 49282
1100000010000010 => 0110000001000001          24641 + 121 = 24762 => 24762 & 0xffff = 24762
0110000010111010 => 0011000001011101          12381 + 117 = 12498 => 12498 & 0xffff = 12498
```

`Checksum:  12498 => 0x30D2`

```
0000000000000000 => 0000000000000000              0 +  88 =    88 =>    88 & 0xffff = 88
0000000001011000 => 0000000000101100             44 + 121 =   165 =>   165 & 0xffff = 165
0000000010100101 => 1000000001010010          32850 +  49 = 32899 => 32899 & 0xffff = 32899
1000000010000011 => 1100000001000001          49217 +  69 = 49286 => 49286 & 0xffff = 49286
1100000010000110 => 0110000001000011          24643 + 121 = 24764 => 24764 & 0xffff = 24764
0110000010111100 => 0011000001011110          12382 + 116 = 12498 => 12498 & 0xffff = 12498
```

`Checksum:  12498 => 0x30D2`

### Flectcher 16 Checksum


####  Example Flecture 16 checksum in python
```
def fletcher16(data):
   sum1 = 0
   sum2 = 0
   index = 0

   while ( index < len(data )):
        sum1 = (sum1 + ord(data[index])) % 255
        sum2 = (sum2 + sum1) % 255
        index += 1

   return ( sum2 << 8 ) | sum1

print(fletcher16('~# FK:s$>K'))
```
#### Collision example
Consider to the strings `~# FK:s$>K` and `~# @X6p BK`. Using the flecture16 checksum function on each string, compute the hash. Both strings result in the same hash.


```
 Sum1    Sum2
 126      126
 161       32
 193      225
   8      233
  83       61
 141      202
   1      203
  37      240
  99       84
 174        3
```

`Checksum:  942 => 0x3AE`

```
 Sum1    Sum2
 126      126
 161       32
 193      225
   2      227
  90       62
 144      206
   1      207
  33      240
  99       84
 174        3
```

`Checksum:  942 => 0x3AE`


### LRC Checksum
Longitudinal Redundancy Check hash function

####  Example LRC checksum in python
```
def LRC_checksum(data):
    checksum = 0
    
    for i in data:
        checksum += ord(i) & 0xff

    return ((checksum ^ 0xff) + 1) & 0xff

print(LRC_checksum("P2'cmw^^08"))
```
#### Collision example
Consider to the strings `P2'cmw^^08"` and `xt6lT]W 8&`. Using the LRC checksum function on each string, compute the hash. Both strings result in the same hash.


```
Checksum    Char    Char Value
     0      'P'        80
    80      '2'        50
   130      "'"        39
   169      'c'        99
   268      'm'       109
   377      'w'       119
   496      '^'        94
   590      '^'        94
   684      '0'        48
   732      '8'        56

```

`Checksum:  236 => 0xEC`

```
Checksum    Char   Char Value
     0      'x'       120
   120      't'       116
   236      '6'        54
   290      'l'       108
   398      'T'        84
   482      ']'        93
   575      'W'        87
   662      ' '        32
   694      '8'        56
   750      '&'        38

```

`Checksum:  236 => 0xEC`

### Sum Checksum
Simple byte summation hash function

####  Example sum checksum in python
```
def sum_checksum(data):
    checksum = 0
    
    for i in data:
        checksum += ord(i)
    return checksum

print(sum_checksum("((P@P00@ $"))
```
#### Collision example
Consider to the strings `((P@P00@ $"` and ` @@@@0@@ $`. Using the simple sum checksum function on each string, compute the hash. Both strings result in the same hash.


```
Checksum    Char    Char Value    New Checksum
     0      '('        40              40
    40      '('        40              80
    80      'P'        80             160
   160      '@'        64             224
   224      'P'        80             304
   304      '0'        48             352
   352      '0'        48             400
   400      '@'        64             464
   464      ' '        32             496
   496      '$'        36             532
```

`Checksum:  532 => 0x214`

```
Checksum    Char   Char Value     New Checksum
     0      ' '        32              32
    32      '@'        64              96
    96      '@'        64             160
   160      '@'        64             224
   224      '@'        64             288
   288      '0'        48             336
   336      '@'        64             400
   400      '@'        64             464
   464      ' '        32             496
   496      '$'        36             532
```

`Checksum:  532 => 0x214`

### Xor8 Checksum
Checksum that uses xor on input byte.

####  Example xor8 checksum in python
```
def xor8(data):
    checksum = 0
    
    for i in data:
        checksum ^= ord(i)

    return checksum

print(xor8('"@@@@@@@@@'))
```
#### Collision example
Consider to the strings `"@@@@@@@@@` and `<??/<|}<0@`. Using the xor8 checksum function on each string, compute the hash. Both strings result in the same hash.


```
Checksum    Char    Char Value     New Checksum
    0        "          34              34
   34        @          64              98
   98        @          64              34
   34        @          64              98
   98        @          64              34
   34        @          64              98
   98        @          64              34
   34        @          64              98
   98        @          64              34
   34        @          64              98

```

`Checksum:  98 => 0x62`

```
Checksum    Char   Char Value     New Checksum
    0        <          60              60
   60        ?          63               3
    3        ?          63              60
   60        /          47              19
   19        <          60              47
   47        |         124              83
   83        }         125              46
   46        <          60              18
   18        0          48              34
   34        @          64              98


```

`Checksum:  98 => 0x62`

Sorting
------------------------

### Bubble Sort
Bubble sort is a sorting algorithm that traverses a list of elements from the beginning, comparing two adjacent pairs and swaps the elements if they are incorrectly ordered. Once the end of the list is reached, the algorithm repeats iterations until no more swaps take place in the final pass and the list is sorted in ascending or descending order.

#### Performance
Operation          |                                          Worst Case   |
-----------          |----------------------------------------------------------------|
Comparisons|O(n^2)|
Swaps|O(n^2)|

#### Worst Case example input
Consider the list of 5 elements `[ 5 4 3 2 1] `  and sort the list in `ascending order` using bubble sort. The inner square brackets `[]` denote a pair of elements currently being compared. 

First Pass
```
[[5  4] 3  2  1 ] → [[4  5] 3  2  1 ] Swap,  5 > 4.
[ 4 [5  3] 2  1 ] → [ 4 [3  5] 2  1 ] Swap,  5 > 3.
[ 4  3 [5  2] 8 ] → [ 4  3 [2  5] 1 ] Swap,  5 > 2.
[ 4  3  2 [5  1]] → [ 4  3  2 [1  5]] Swap,  5 > 1.
```
Second Pass
```
[[4  3] 2  1  5 ] → [[3  4] 2  1  5 ] Swap,  4 > 3.
[ 3 [4  2] 1  5 ] → [ 3 [2  4] 1  5 ] Swap,  4 > 2.
[ 3  2 [4  1] 5 ] → [ 3  2 [1  4] 5 ] Swap,  4 > 1.
[ 3  2  1 [4  5]] → [ 3  2  1 [4  5]] No swap needed.
```
Third Pass
```
[[3  2] 1  4  5 ] → [[2  3] 1  4  5 ] Swap,  3 > 2.
[ 2 [3  1] 4  5 ] → [ 2 [1  3] 4  5 ] Swap,  3 > 1.
[ 2  1 [3  4] 5 ] → [ 2  1 [3  4] 5 ] No swap needed.
[ 2  1  3 [4  5]] → [ 2  1  3 [4  5]] No swap needed.
```
Fourth Pass
```
[[2  1] 3  4  5 ] → [[1  2] 3  4  5 ] Swap,  2 > 1.
[ 1 [2  3] 4  5 ] → [ 1 [2  3] 4  5 ] No swap needed.
[ 1  2 [3  4] 5 ] → [ 1  2 [3  4] 5 ] No swap needed.
[ 1  2  3 [4  5]] → [ 1  2  3 [4  5]] No swap needed.
```
Fifth and Final Pass
```
[[2  1] 3  4  5 ] → [[1  2] 3  4  5 ] No swap needed.
[ 1 [2  3] 4  5 ] → [ 1 [2  3] 4  5 ] No swap needed.
[ 1  2 [3  4] 5 ] → [ 1  2 [3  4] 5 ] No swap needed.
[ 1  2  3 [4  5]] → [ 1  2  3 [4  5]] No swap needed.
The fifth pass is required to check if no more swaps occur. When no more swaps are needed, all elements in the list are sorted.
```

### Bucket Sort
Named after how the elements of a list are distributed into `buckets`; Bucket sort first iterates through a list, putting elements into a bucket in a `scatter` phase. Each bucket is then sorted individually with the same algorithm recursively or by using a different sorting algorithm. The final `gather` phase combines the elements from each bucket in order. Also known as `radix sort`.

#### Performance
Operation          |                                          Worst Case   |
-----------          |----------------------------------------------------------------|
Comparisons|O(n^2)|
Swaps|O(n^2)|

#### Worst Case example input
The worst case input for bucket sort occurs when many elements in the list have values similar to one another that cluster together, these elements then fall in the same bucket.
Consider the list of 5 elements `[ 1 1 1 1 1] `  and sort the list in `ascending order` using bucket sort. 

```
 -------      -------      -------
|       |    |       |    |       |
|       |    |       |    |       |        Buckets are initially empty
|_______|    |_______|    |_______|
   0-9         10-19        20-29

 -------      -------      -------
| 1     |    |       |    |       |
|       |    |       |    |       |        First element is added to the first bucket
|_______|    |_______|    |_______|
   0-9         10-19        20-29

 . . .

 -------      -------      -------
| 1 1 1 |    |       |    |       |
|  1 1  |    |       |    |       |        All elements are added to the first bucket
|_______|    |_______|    |_______|
   0-9         10-19        20-29

```
### Insertion Sort
To perform an insertion sort on a list, iterate from the beginning of the list and for each element *i*, compare the element with the left value starting at i-1 until the element is at a sorted position or the beginning of the list is reached. This element is then inserted in place in sorted order. After the last element in the list is complete, the list will be sorted.

#### Performance
Operation          |                                          Worst Case   |
-----------          |----------------------------------------------------------------|
Comparisons|O(n^2)|
Swaps|O(n^2)|

#### Worst Case example input
Given a list of 10 elements `[j i h g f e d c b a]`, sort the list alphabetically with insertion sort. The worst case contains the most comparisons and is a reverse sorted list. The single element in square brackets `[]` for each line is the current element being evaluated.
```
[[j] i  h  g  f  e  d  c  b  a ] → [[j] i h g f e d c b a]    First element is not compared to any values.
[ j [i] h  g  f  e  d  c  b  a ] → [[i] j h g f e d c b a]    1 comparison. The element 'i' is compared to to 'j', and is inserted.
[ i  j [h] g  f  e  d  c  b  a ] → [[h] i j g f e d c b a]    2 comparisons.
[ h  i  j [g] f  e  d  c  b  a ] → [[g] h i j f e d c b a]    3 comparisons
[ g  h  i  j [f] e  d  c  b  a ] → [[f] g h i j e d c b a]    4 comparisons
[ f  g  h  i  j [e] d  c  b  a ] → [[e] f g h i j d c b a]    5 comparisons
[ e  f  g  h  i  j [d] c  b  a ] → [[d] e f g h i j c b a]    6 comparisons
[ d  e  f  g  h  i  j [c] b  a ] → [[c] d e f g h i j b a]    7 comparisons
[ c  d  e  f  g  h  i  j [b] a ] → [[b] c d e f g h i j a]    8 comparisons
[ b  c  d  e  f  g  h  i  j [a]] → [[a] b c d e f g h i j]    9 comparisons
[ a  b  c  d  e  f  g  h  i  j ]                              List is sorted alphabetically.
                                                              45 total comparisons.
```

### Merge Sort
Elements in an unsorted list are divided into *n* sublist and as a base case, a list of one element is an already sorted list.  Sublists are than merged together by comparing the first element of two sublists and then moving the elements into a new sublist. This process is repeated until a final sublist is created of *n* sorted elements.
#### Performance
Operation          |                                          Worst Case   |
-----------          |----------------------------------------------------------------|
Comparisons|O(n log n)|
Swaps|O(n log n)|

#### Worst Case example input
Consider the list of 10 elements `[4 6 2 9 1 5 7 3]`  and sort the list in `ascending order` using merge sort. The inner square brackets `[]` denote a pair of elements currently being compared. The worse case scenario involves more comparison operations of the elements in the list.
```
            [4 0 6 2 5 1 7 3]                 Divide the list into n sublist
                  /    \
                 /      \
          [4 0 6 2]    [5 1 7 3]
             / \          / \
            /   \        /   \
        [4 0]  [6 2]  [5 1]  [7 3]
       /  /    /\        /\    \  \
      /  /    /  \      /  \    \  \
     /  /    /    \    /    \    \  \
  [4]  [0]  [6]  [2]  [5]  [1]  [7]  [3]      Here we have n sublists, each sublist is sorted and
     \  \    \    /    \    /    /  /         comparisons are performed on pairs of sublist.
      \  \    \  /      \  /    /  /          List of comparisons: [(4,0), (6, 2), (5, 1), (7, 3)]
       \  \    \/        \/    /  /
        [0 4]  [2 6]  [1 5]  [3 7]            List of comparisons: [(0,2), (4,2), (4,6), (1,3), (5,3), (5,7)]
            \   /        \   /
             \ /          \ /
          [0 2 4 6]    [1 3 5 7]              List of comparisons: [(0,1), (2,1), (2,3), (4,3), (4,5), (6,5), (6,7)]
                 \      /
                  \    /
            [0 1 2 3 4 5 6 7]                 Sorted list with a total of 17 comparisons
```


Consider an already sorted list. 
```
            [0 1 2 3 4 5 6 7]                 Divide the list into n sublist
                  /    \
                 /      \
          [0 1 2 3]    [4 5 6 7]
             / \          / \
            /   \        /   \
        [0 1]  [2 3]  [4 5]  [6 7]
       /  /    /\        /\    \  \
      /  /    /  \      /  \    \  \
     /  /    /    \    /    \    \  \
  [0]  [1]  [2]  [3]  [4]  [5]  [6]  [7]      Here we have n sublists, each sublist is sorted and
     \  \    \    /    \    /    /  /         comparisons are performed on pairs of sublist.
      \  \    \  /      \  /    /  /          List of comparisons: [(0,1), (2, 3), (4, 5), (6, 7)]
       \  \    \/        \/    /  /
        [0 1]  [2 3]  [4 5]  [6 7]            List of comparisons: [(0,2), (1,2), (4,6), (5,6)]
            \   /        \   /
             \ /          \ /
          [0 1 2 3]    [4 5 6 7]              List of comparisons: [(0,4), (1,4), (2,4), (3,4)]
                 \      /
                  \    /
            [0 1 2 3 4 5 6 7]                 Sorted list with a total of 12 comparisons
```
The sorted list has less comparisons. When performing the merge of two sublist, once one list is exhausted, the remaining elements can be appended to the new sublist in sorted order.

### Quick Sort
Quick sort is divide and conquer algorithm that divides a list into two sublist by choosing a pivot point ( a element within the array). The pivot divides low and high values, elements with values less than the pivot's value are moved before the pivot, and likewise the elements with higher values are moved after the pivot. This process is preformed recursively for each sublists. The worst case performance depends on the implementation. For lomuto and hoare partition schemes with a high value as the pivot, having already sorted input is the worst case.  For mid partition schemes, the largest values as pivots cause the worst case. 

#### Performance
Operation          |                                          Worst Case   |
-----------          |----------------------------------------------------------------|
Comparisons|O(n^2)|
Swaps|O(n^2)|

#### Worst Case example input
Consider the list of 5 elements `[ 1 2 3 4 5]` and sort the list in `ascending order` using quick sort. Elements with the parenthesis `()` denote the pivot.

```
[1 2 3 4 (5)]     The right most element '5' is chosen as the pivot
[1 2 3 (4)] 5 ]   An n - 1 sublist is created, and element '4' is chosen as the pivot
[1 2 (3)] 4 5 ]   An n - 2 sublist is created and the element '3' is chosen as the pivot
[1 (2)] 3 4 5 ]   An n - 3 sublist is created and the element '2' is chosen as the pivot
[[1] 2 3 4 5 ]    The sublist has a list of size 1, This sublist is sorted. With n - i calls, to create partitions, the run time is O(n^2).

```

String Matching
------------------------

The naive string matching algorithm for finding a pattern `P` in a text `T` is to first start at the beginning of `T` and compare the character with the first character in the pattern. If a match is not found, the next character in `T` is examined for a match. Once a match occurs, the next character in `P` is compared to the subsequent character in `T` until the entire pattern is matched.


### Boyer-Moore
When searching for a pattern, the last character `n` of the pattern is compared to the `kth` element of the plain text, starting at `k` = `n`. When a match occurs, the `n - 1` characters are compared until the pattern is matched. If a character at `k` is compared to the pattern but does not occur anywhere in the pattern, the algorithm efficiently skips unnecessary comparisons by shifting the pattern to the right. The worst case occurs when no comparisons can be skipped.


#### Performance
Operation          |                                          Worst Case   |
-----------          |----------------------------------------------------------------|
Search|O(nm)|

#### Worst Case example input
Consider the text `aaaaaaaaaa` and the pattern `aaaa`. No skips can occur since all the values in `T` are in `P` and must be compared.

```
Index:   0123456789
Text:    aaaaaaaaaa
Pattern: aaaa                 The elements at index 3 in the text and pattern are compared 
                              => match occurs, search n-1 characters

Index:   0123456789
Text:    aaaaaaaaaa
Pattern: aaaa                 The element at index 2 in the text and pattern are compared
                              => match, search n-1 characters

Index:   0123456789
Text:    aaaaaaaaaa
Pattern: aaaa                 The element at index 1 in the text and pattern are compared
                              => match, search n-1 characters

Index:   0123456789
Text:    aaaaaaaaaa
Pattern: aaaa                 The element at index 0 in the text and pattern are compared
                              => pattern matched
```

### Knuth-Moore-Pratt
This algorithm is similar to the naive string matching algorithm as the pattern is first compared character by character with the text, progressing to the next character when matched. However, when characters do not match, the pattern can shift right and begin comparing characters either at a substring found in both the pattern and the text, or where the text comparison index left off; skipping unnecessary comparisons. The substring found in the pattern and text is known as a `partial match` and is found in the table generated by the algorithm.

#### Performance
Operation          |                                          Worst Case   |
-----------          |----------------------------------------------------------------|
Search|O(nm)|

#### Worst Case example input
Consider the text `aaaaaaaaaa` and the pattern `abaa`. 

```
Index:   0123456789
Text:    aaaaaaaaaa
Pattern: abaa                 The elements at index 0 in the text and pattern are compared 
                              => match occurs, search n-1 characters

Index:   0123456789
Text:    aaaaaaaaaa
Pattern: abaa                 The elements at text[1] and pattern[1] are compared 
                              => no match occurs

Index:   0123456789
Text:    aaaaaaaaaa
Pattern:  abaa                The elements at text[1] and pattern[0] are compared 
                              => match occurs

Index:   0123456789
Text:    aaaaaaaaaa
Pattern:  abaa                The elements at text[2] and pattern[1] are compared 
                              => no match occurs

Index:   0123456789
Text:    aaaaaaaaaa
Pattern:   abaa               The elements at text[2] and pattern[0] are compared 
                              => match occurs

Index:   0123456789
Text:    aaaaaaaaaa
Pattern:   abaa               The elements at text[3] and pattern[1] are compared 
                              => no match occurs

Index:   0123456789
Text:    aaaaaaaaaa
Pattern:    abaa              The elements at text[3] and pattern[0] are compared 
                              => match occurs

Index:   0123456789
Text:    aaaaaaaaaa
Pattern:    abaa              The elements at text[4] and pattern[1] are compared 
                              => no match occurs

Index:   0123456789
Text:    aaaaaaaaaa
Pattern:     abaa             The elements at text[4] and pattern[0] are compared 
                              => match occurs

Index:   0123456789
Text:    aaaaaaaaaa
Pattern:     abaa             The elements at text[5] and pattern[1] are compared 
                              => no match occurs

Index:   0123456789
Text:    aaaaaaaaaa
Pattern:      abaa            The elements at text[5] and pattern[0] are compared 
                              => match occurs

Index:   0123456789
Text:    aaaaaaaaaa
Pattern:      abaa            The elements at text[6] and pattern[1] are compared 
                              => no match occurs

Index:   0123456789
Text:    aaaaaaaaaa
Pattern:       abaa           The elements at text[6] and pattern[0] are compared 
                              => match occurs

Index:   0123456789
Text:    aaaaaaaaaa
Pattern:       abaa           The elements at text[7] and pattern[1] are compared 
                              => no match occurs

Index:   0123456789
Text:    aaaaaaaaaa
Pattern:        abaa          The elements at text[7] and pattern[0] are compared 
                              => match occurs

Index:   0123456789
Text:    aaaaaaaaaa
Pattern:        abaa          The elements at text[8] and pattern[1] are compared 
                              => no match occurs

Index:   0123456789
Text:    aaaaaaaaaa
Pattern:         abaa         The elements at text[8] and pattern[0] are compared 
                              => match occurs

Index:   0123456789
Text:    aaaaaaaaaa
Pattern:         abaa         The elements at text[9] and pattern[1] are compared 
                              => no match occurs

                              The worst case gives the maximum character comparisons.
```
### Rabin-Karp
Patterns are found within a text using hashing. When two strings have the same elements, their hashes will also be equivalent. Since hash collisions can occur, strings with identical hashes are compared character by character to confirm the strings are a match.

#### Performance
Operation          |                                          Worst Case   |
-----------          |----------------------------------------------------------------|
Search|O(nm)|

#### Worst Case example input
Consider the text `aaaaaaaaaa` and the pattern `aaaa`. 

```
Index:   0123456789
Text:    aaaaaaaaaa
Pattern: aaaa                 The pattern 'aaaa' is hashed and compared with the hash of the first 4 characters in the text.
                              => Hashes match.

'aaaa' compared with 'aaaa'   String match found


Index:   0123456789
Text:    aaaaaaaaaa
Pattern: aaaa                 The pattern's hash is compared with the next set of 4 characters in the text, starting at index 1.

'aaaa' compared with 'aaaa'   String match found


Index:   0123456789
Text:    aaaaaaaaaa
Pattern: aaaa                 The pattern's hash is compared with the next set of 4 characters in the text, starting at index 2.

'aaaa' compared with 'aaaa'   String match found

This is repeated until the end of the text has been reached.
```
Trees
------------------------

### AVL Tree

#### Performance
Operation          |                                          Worst Case   |
-----------          |----------------------------------------------------------------|
Access|O(log n)
Delete|O(log n)|
Insert|O(log n)|
Search|O(log n)|
Space|O(n)|

### B-Tree

#### Performance
Operation          |                                          Worst Case   |
-----------          |----------------------------------------------------------------|
Access|O(log n)
Delete|O(log n)|
Insert|O(log n)|
Search|O(log n)|
Space|O(n)|


### Binary Search Tree

#### Performance
Operation          |                                          Worst Case   |
-----------          |----------------------------------------------------------------|
Access|O(n)
Delete|O(n)|
Insert|O(n)|
Search|O(n)|
Space|O(n)|

### Heap Tree

#### Performance
Operation          |                                          Worst Case   |
-----------          |----------------------------------------------------------------|
Delete|O(log n)|
Insert|O(log n)|
Search|O(n)|
Space|O(n)|

### Huffman Tree

### Red-Black Tree

#### Performance
Operation          |                                          Worst Case   |
-----------          |----------------------------------------------------------------|
Access|O(log n)
Delete|O(log n)|
Insert|O(log n)|
Search|O(log n)|
Space|O(n)|
