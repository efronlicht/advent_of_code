import typing as T
"""
--- Day 1: Inverse Captcha ---

The night before Christmas, one of Santa's Elves calls you in a panic. "The printer's broken! We can't print the Naughty or Nice List!" By the time you make it to sub-basement 17, there are only a few minutes until midnight. "We have a big problem," she says; "there must be almost fifty bugs in this system, but nothing else can print The List. Stand in this square, quick! There's no time to explain; if you can convince them to pay you in stars, you'll be able to--" She pulls a lever and the world goes blurry.

When your eyes can focus again, everything seems a lot more pixelated than before. She must have sent you inside the computer! You check the system clock: 25 milliseconds until midnight. With that much time, you should be able to collect all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day millisecond in the advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

You're standing in a room with "digitization quarantine" written in LEDs along one wall. The only door is locked, but it includes a small interface. "Restricted Area - Strictly No Digitized Users Allowed."

It goes on to explain that you may only leave by solving a captcha to prove you're not a human. Apparently, you only get one millisecond to solve the captcha: too fast for a normal human, but it feels like hours to you.

The captcha requires you to review a sequence of digits (your puzzle input) and find the sum of all digits that match the next digit in the list. The list is circular, so the digit after the last digit is the first digit in the list.

For example:

1122 produces a sum of 3 (1 + 2) because the first digit (1) matches the second digit and the third digit (2) matches the fourth digit.
1111 produces 4 because each digit (all 1) matches the next.
1234 produces 0 because no digit matches the next.
91212129 produces 9 because the only digit that matches the next one is the last digit, 9.
What is the solution to your captcha?


--- Part Two ---
You notice a progress bar that jumps to 50% completion. Apparently, the door isn't yet satisfied, but it did emit a star as encouragement. The instructions change:

Now, instead of considering the next digit, it wants you to consider the digit halfway around the circular list. That is, if your list contains 10 items, only include a digit in your sum if the digit 10/2 = 5 steps forward matches it. Fortunately, your list has an even number of elements.

For example:

1212 produces 6: the list contains 4 items, and all four digits match the digit 2 items ahead.
1221 produces 0, because every comparison is between a 1 and a 2.
123425 produces 4, because both 2s match each other, but no other digit has a match.
123123 produces 12.
12131415 produces 4.
What is the solution to your new captcha?
"""




def parse(raw: str) -> T.Iterable[int]:
    return (int(x) for x in raw if x in frozenset("0123456789")) 



def get_sum(ints: T.Iterable[int]) -> int:
    a = list(ints)
    print(a)
    offset = len(a)//2
    print(offset)
    def digit_halfway_across(i: int) -> int:
        j = (i + offset) % len(a)
        return a[j]
    
    total = 0
    for i, n in enumerate(a):
        if n == digit_halfway_across(i):
            total += n
    return total


input_raw = """52554437147555553177771524418267843219182859995942215316
3624294499836371611929484583857994356254324723996955579177239268156788344983798211923
953632534126352441539712382435846789196376294872332777454571585154242983211917913991447
1523515332247317441719184556891362179267368325486642376685657759623876854958721636574219871
24964577373859775142995943746687616627375552487335145295141162847935252236771426971851483893
3283861425982562854845471512652555633922878128558926123935941858532446378815929573452775348599
6939828346997577347141878313375464745156785771587217519215621455911666342796992994182691585575579
9658388164246827461819633526734289749848686992526289612514686712459658798953149589164668152825962467
4792728146526849711139146268799436334618974547539561587581268886449291817335232859391493839167111246
3764931919851458485318293441985365689879968942265858373483729589595359696515735165425811444625365749
53764413723147957237298324458181291167587791714172674717898567269547766636143732438694473231473258452
166457194797819423528139157452148236943283374193561963393846385622218535952591588353565319432285579711
88155934354451546196284687968587943176796397565434756938535448222634126176854732874994716386464516842895
344539636139887353643493182363552246775478242255799826285829756386249265246452636617121827617625858244492
34971817761294363963973339762159767315421828789793893622971558194616853616764147255973357599762855977133326
882752412716646582868686971675153298118312343246983451599491354744636247496246265182478314481438761831338142
39776115643398654663212443991774648226496119698963448743819789864535669797629111559313623941926639435268341485
9634226832156388525576561441814182893497192799899473976914178918516546197642515185584673995933864949937965722319
688553938615493558679454836586175935486545321172155177699757628981159565417167225912933524353151822828239332639
52412421857958282613192151642622379577432325589712891456398521481971842657662918852598472366466159359637596311453
3815925753811435978185468569542934842888424897217727836135381476665399667599478419582721429546238953242282569645
6457332417366426619555"""

print(get_sum(parse(input_raw)))