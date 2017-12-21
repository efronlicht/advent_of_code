package main

type OP struct {
	code string
	a, b val
}

type signal struct{}

var yes signal

type machine struct {
	in, out chan int
	alive   chan signal
	reg     register
	ops     []OP
}

func (m machine) Run() (sends int) {
	var i int
	for {
		op := m.ops[i]
		result := op.run(m.reg, m.in, m.out)
		if op.code == "snd" {
			sends++
		}
		i += result.offset
		if result.dead {
			return sends
		}
		m.alive <- yes
	}
}

func (op OP) run(reg register, in <-chan int, out chan<- int) result {
	return _lookup[op.code](reg, in, out, op.a, op.b)
}

func add(reg register, _ <-chan int, _ chan<- int, a, b val) result {
	k := string(a.(key))
	reg[k] += b.val(reg)
	return result{reg[k], 1, false}
}

func mul(reg register, _ <-chan int, _ chan<- int, a, b val) result {
	k := string(a.(key))
	reg[k] *= b.val(reg)
	return result{reg[k], 1, false}
}

func mod(reg register, _ <-chan int, _ chan<- int, a, b val) result {
	k := string(a.(key))
	reg[k] %= b.val(reg)
	return result{reg[k], 1, false}
}

func rcv(reg register, in <-chan int, _ chan<- int, a, _ val) result {
	v, ok := <-in
	if !ok {
		return result{0, 0, true} //dead
	}
	k := string(a.(key))
	reg[k] = v
	return result{v, 1, false}
}

func snd(reg register, _ <-chan int, out chan<- int, a, _ val) result {
	v := a.val(reg)
	out <- v
	return result{v, 1, false}
}

func set(reg register, _ <-chan int, _ chan<- int, a, b val) result {
	v := b.val(reg)
	reg[string(a.(key))] = v
	return result{v, 1, false}
}

func jgz(reg register, _ <-chan int, _ chan<- int, a, b val) result {
	v := a.val(reg)
	if v > 0 {
		return result{v, b.val(reg), false}
	}
	return result{v, 1, false}
}
