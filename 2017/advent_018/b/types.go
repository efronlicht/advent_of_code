package main

type register map[string]int

type val interface {
	val(reg map[string]int) int
}

type key string

type asx struct {
	code, left, right string
}

func (k key) val(reg map[string]int) int {
	v, _ := reg[string(k)]
	return v
}

type num int

func (n num) val(_ map[string]int) int {
	return int(n)
}

type chanargs struct {
	in  <-chan int
	out chan<- int
}

type args struct {
	a, b val
}

type opfunc = func(register, <-chan int, chan<- int, val, val) result

type result struct {
	val, offset int
	dead        bool
}
