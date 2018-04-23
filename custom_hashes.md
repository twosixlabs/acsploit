Using `hashes/collions/custom_hash`
====================

ACsploit's collection of hash function exploits is great for finding collisions in the functions it covers, but what about when you want to find collisions to use against a program that implements its own custom hash function?

The `custom_hash` module allows you to define custom hash functions out of a collection of primitive operations and solve for collisions against them.

### Syntax
Functions are expressed in prefix notation, with each operator preceding the value or values it works on.

Values can be constants (literal base-10 numbers like `7` or `65536` or `-22`) and variables (declared with names like `x` or `y` or `byte_0`). All values are assumed to be [two's complement integers](https://en.wikipedia.org/wiki/Two%27s_complement).

Any number of variables may be used and variables may be used any number of times in the function.

The following operations are supported:

- `+`: addition
- `-`: subtraction
- `*`: multiplication
- `/`: division
- `<<`: arithmetic left-shift
- `>>`: arithmetic right-shift
- `&`: bit-wise AND
- `|`: bit-wise OR
- `^`: bit-wise XOR

In the examples below the left expression is the hash function and the expression on the right is its expression for `custom_hash`.

	x + 2 => + 2 x
	(x + 7) * y => * y + x 7
	(x + 7) * y => * + x 7 y
	x^2 + y << z => + * x x << y z
	
### Images and Preimages
An `image` is the value produced by a hash function when given the `preimage` as input.

`custom_hash`'s `target_type` specifies whether it solves for collisions against a given `image` or the output produced by hashing a given `preimage`.
 
If `f(a, b, c)` is the hash function, selecting `target_type` `image` with an `image` value of `32` would find values of `a, b, c` such that `f(a, b, c) = 32`.

Selecting `target_type` `preimage` with a `preimage` values of `a = 27, b = 12, c = 400` would find new values of `a, b, c` such that `f(a, b, c) = f(27, 12, 400)`.



### Bit-width

- Values are internally represented as signed integers `variable_width` bits wide and so cannot express values outside of that range.
- Computations are performed at 32-bits wide if `variable_width` is <= 32 (the default) and at 64-bits wide if `variable_width` is not.
    - The `image` and `preimage` values must fit within the computation width but can be wider than the `variable_width`.
    - eg, 500 cannot be expressed as an 8-bit signed integer, but `image` can 500 when `variable_width` is 8, because the computation will be performed at 32-bit precision, which is more than wide enough for 500.
    - eg, `preimage` could be `x = 2, y = 256, z = 400000000000`, where `z` is not expressible in 32 bits, when `variable_width` is greater than 32, becuase the computation will be performed at 64-bit precision.  
