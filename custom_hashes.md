Using `hashes/collions/custom_hash`
====================

ACsploit's collection of hash function exploits is great for finding collisions in the functions it covers, but what about when you want to find collisions to use against a program that implements its own custom hash function?

The `custom_hash` module allows you to define custom hash functions out of a collection of primitive operations and solve for collisions against them.

### Syntax
Functions are expressed in prefix notation, with each operator preceding the value or values it works on.

Values can be constants (literal numbers like `7` or `65536` or `-22`) and variables (declared with names like `x` or `y` or `byte_0`). All values are assumed to be [two's complement integers](https://en.wikipedia.org/wiki/Two%27s_complement).

If the target hash works on multiple bytes of input each byte should be represented by a separate variable.

The following operations are supported:

- `+`: addition
- `-`: subtraction
- `*`: multiplication
- `/`: division
- `<<`: arithmetic left-shift
- `>>`: arithmetic right-shift
- `&`: bit-wise AND
- `|`: bit-wise OR

In the examples below the left expression is the hash function and the expression on the right is its expression for `custom_hash`.

	x + 2 => + 2 x
	(x + 7) * y => * y + x 7
	(x + 7) * y => * + x 7 y
	

### Limitations

- Variables can only be used once per function
  - eg, a function like `h(x, y) = 2x + xy` would have to be expressed as `* x + y 2`, not `+ * 2 x * x y` and a function like `h(x) = x^2` cannot not be expressed by `custom_hash`
- Values are internally represented as signed `32`-bit integers and so cannot express values outside `[-2^31, 2^31)`
