#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set expandtab tabstop=4 shiftwidth=4 :

# This is a function which throws an i ching hexagram and returns it as a
# string.  Optionally, if you run this utility from the command line, it'll
# print the output as a primitive unit test.

# by: The Doctor [412/724/301/703/415/510] <drwho at virtadpt dot net>
# License: GPLv3

# References used:
#   https://en.wikipedia.org/wiki/I_Ching (CC-BY-SA v3.0 unported)
#   https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching (CC-BY-SA v3.0 unported)

import random
import sys

broken   = "--  --"
unbroken = "------"

# A lookup table of i ching hexagrams, to identify the throw.
i_ching = {}
i_ching["111111"] = { "number": 1, "name": "qian/force",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_1" }
i_ching["000000"] = { "number": 2, "name": "kun/field",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_2" }
i_ching["010001"] = { "number": 3, "name": "zhun/sprouting",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_3" }
i_ching["100010"] = { "number": 4, "name": "meng/enveloping",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_4" }
i_ching["010111"] = { "number": 5, "name": "xu/attending",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_5" }
i_ching["111010"] = { "number": 6, "name": "song/arguing",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_6" }
i_ching["000010"] = { "number": 7, "name": "shi/leading",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_7" }
i_ching["010000"] = { "number": 8, "name": "bi/grouping",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_8" }
i_ching["110111"] = { "number": 9, "name": "xiao chu/small accumulating",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_9" }
i_ching["111011"] = { "number": 10, "name": "lu/treading",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_10" }
i_ching["000111"] = { "number": 11, "name": "tai/pervading",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_12" }
i_ching["111000"] = { "number": 12, "name": "pi/obstruction",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_12" }
i_ching["111101"] = { "number": 13, "name": "tong ren/concording people",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_13" }
i_ching["101111"] = { "number": 14, "name": "da you/great possessing",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_14" }
i_ching["000100"] = { "number": 15, "name": "qian/humbling",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_15" } 
i_ching["001000"] = { "number": 16, "name": "yu/providing for",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_16" }
i_ching["011001"] = { "number": 17, "name": "sui/following",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_17" }
i_ching["100110"] = { "number": 18, "name": "gu/correcting",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_18" }
i_ching["000011"] = { "number": 19, "name": "lin/nearing",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_19" }
i_ching["110000"] = { "number": 20, "name": "guan/viewing",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_20" }
i_ching["101001"] = { "number": 21, "name": "shi ke/gnawing bite",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_21" }
i_ching["100101"] = { "number": 22, "name": "bi/adorning",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_22" }
i_ching["100000"] = { "number": 23, "name": "bo/stripping",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_23" }
i_ching["000001"] = { "number": 24, "name": "fu/returning",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_24" }
i_ching["111001"] = { "number": 25, "name": "wu wang/without embroiling",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_25" }
i_ching["010111"] = { "number": 26, "name": "da chu/great accumulating",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_26" }
i_ching["100001"] = { "number": 27, "name": "yi/swallowing",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_27" }
i_ching["011110"] = { "number": 28, "name": "da guo/great exceeding",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_28" }
i_ching["010010"] = { "number": 29, "name": "kan/gorge",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_29" }
i_ching["101101"] = { "number": 30, "name": "li/radiance",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_30" }
i_ching["011100"] = { "number": 31, "name": "xian/conjoining",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_31" }
i_ching["001110"] = { "number": 32, "name": "heng/persevering",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_32" }
i_ching["111100"] = { "number": 33, "name": "dun/retiring",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_33" }
i_ching["001111"] = { "number": 34, "name": "da zhuang/great invigorating",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_34" }
i_ching["101000"] = { "number": 35, "name": "jin/prospering",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_35" }
i_ching["000101"] = { "number": 36, "name": "ming yi/darkening of the light",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_36" }
i_ching["110101"] = { "number": 37, "name": "jia ren/dwelling people",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_37" }
i_ching["101011"] = { "number": 38, "name": "kui/polarizing",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_38" }
i_ching["010100"] = { "number": 39, "name": "jian/limping",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_39" }
i_ching["001010"] = { "number": 40, "name": "xie/taking apart",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_40" }
i_ching["100011"] = { "number": 41, "name": "sun/diminishing",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_41" }
i_ching["110001"] = { "number": 42, "name": "yi/augmenting",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_42" }
i_ching["011111"] = { "number": 43, "name": "guai/displacement",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_43" }
i_ching["111110"] = { "number": 44, "name": "gou/coupling",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_44" }
i_ching["011000"] = { "number": 45, "name": "cui/clustering",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_45" }
i_ching["000110"] = { "number": 46, "name": "sheng/ascending",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_46" }
i_ching["011010"] = { "number": 47, "name": "kun/confining",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_47" }
i_ching["010110"] = { "number": 48, "name": "jing/welling",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_48" }
i_ching["011101"] = { "number": 49, "name": "ge/skinning",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_49" }
i_ching["101110"] = { "number": 50, "name": "ding/holding",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_50" }
i_ching["001001"] = { "number": 51, "name": "zhen/shake",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_51" }
i_ching["100100"] = { "number": 52, "name": "gen/bound",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_52" }
i_ching["110100"] = { "number": 53, "name": "jian/infiltrating",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_53" }
i_ching["001011"] = { "number": 54, "name": "gui mei/converting the maiden",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_54" }
i_ching["001101"] = { "number": 55, "name": "feng/abounding",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_55" }
i_ching["101100"] = { "number": 56, "name": "lu/sojourning",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_56" }
i_ching["110110"] = { "number": 57, "name": "xun/ground",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_57" }
i_ching["011011"] = { "number": 58, "name": "dui/open",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_58" }
i_ching["110010"] = { "number": 59, "name": "huan/dispersing",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_59" }
i_ching["010011"] = { "number": 60, "name": "jie/articulating",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_60" }
i_ching["110011"] = { "number": 61, "name": "zhong fu/center returning",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_61" }
i_ching["001100"] = { "number": 62, "name": "xiao guo/small exceeding",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_62" }
i_ching["010101"] = { "number": 63, "name": "ji ji/already fording",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_63" }
i_ching["101010"] = { "number": 64, "name": "wei ji/not yet fording",
    "meaning": "https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching#Hexagram_64" }

def handle(req):
    hexagram = ""
    coin_flip = 0
    rows = ""
    response = ""

    # Generate a hexagram by flipping a coin six times.  Each time, add a
    # line to the hexagram.
    for i in range(0, 6):
        coin_flip = random.randint(0, 1)
        # Heads.
        if coin_flip == 0:
            hexagram = hexagram + broken + "\n"
            rows = rows + "0"

        # Tails.
        if coin_flip == 1:
            hexagram = hexagram + unbroken + "\n"
            rows = rows + "1"

    response = "Your i ching hexagram is number " + str(i_ching[rows]["number"]) + " "
    response = response + "(" + i_ching[rows]["name"] + ").\n\n" + hexagram + "\n"
    response = response + i_ching[rows]["meaning"] + "\n"

    return response

if __name__ == "__main__":
    print("Unit testing mode enabled.")
    print(handle())
    sys.exit(0)
