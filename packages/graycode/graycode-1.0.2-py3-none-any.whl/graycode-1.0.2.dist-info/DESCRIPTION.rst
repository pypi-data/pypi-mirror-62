# Gray codes for Python

## Introduction

Library functions to convert gray code to two's complement integer and
vice versa in Python 3.

See LICENSE.md for copyright information. This library is licensed under the
MIT license.

See https://en.wikipedia.org/wiki/Gray_code for details about gray codes.

## Example

    import graycode

    graycode.tc_to_gray_code(2)
    # => 3
    graycode.gray_code_to_tc(3)
    # => 2


