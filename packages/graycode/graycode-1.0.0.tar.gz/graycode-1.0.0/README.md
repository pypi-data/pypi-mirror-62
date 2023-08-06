# Introduction

Library functions to convert gray code to two's complement integer and
vice versa in Python 3.

See LICENSE.md for copyright information. This library is licensed under the
MIT license.

See https://en.wikipedia.org/wiki/Gray_code for details about gray codes.

# Example

```
>>> import gray_code
>>> gray_code.tc_to_gray_code(2) == 3
>>> gray_code.gray_code_to_tc(3) == 2
```
