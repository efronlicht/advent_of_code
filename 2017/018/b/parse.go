package main

import (
	"strconv"
	"strings"
)

func toVal(s string) (val, error) {
	if len(s) == 1 {
		r := s[0]
		if 'a' < r && r < 'z' {
			return key(s), nil
		}
	}

	v, err := strconv.ParseInt(s, 10, 0)
	return num((v)), err
}

func parseLine(line string) (asx, bool) {
	split := strings.Split(line, " ")
	if len(split) == 2 {
		return asx{code: split[0], left: split[1]}, true
	} else if len(split) == 3 {
		return asx{code: split[0], left: split[1], right: split[2]}, true
	}
	return asx{}, false
}

func parseRaw(raw string) (instructions []asx, ok bool) {
	lines := strings.Split(raw, "\n")
	instructions = make([]asx, len(lines))
	for i, line := range lines {
		if instructions[i], ok = parseLine(line); !ok {
			return nil, false
		}
	}
	return instructions, true
}

var rawInput = `set i 31
set a 1
mul p 17
jgz p p
mul a 2
add i -1
jgz i -2
add a -1
set i 127
set p 952
mul p 8505
mod p a
mul p 129749
add p 12345
mod p a
set b p
mod b 10000
snd b
add i -1
jgz i -9
jgz a 3
rcv b
jgz b -1
set f 0
set i 126
rcv a
rcv b
set p a
mul p -1
add p b
jgz p 4
snd a
set a b
jgz 1 3
snd b
set f 1
add i -1
jgz i -11
snd a
jgz f -16
jgz a -19`
