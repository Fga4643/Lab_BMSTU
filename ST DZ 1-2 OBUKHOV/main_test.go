package main


import (
	"reflect"
	"strconv"
	"testing"
)

func ConvertInt(val string, base, toBase int) (string, error) {
	i, err := strconv.ParseInt(val, base, 64)
	if err != nil {
		return "", err
	}
	return strconv.FormatInt(i, toBase), nil
}

func TestOperationO(t *testing.T) {
	type args struct {
		a uint64
		b uint64
	}
	tests := []struct {
		name  string
		args  args
		want  uint64
		want1 uint64
	}{
		{"17-1", args{17, 1}, 17, 0},
		{"10-100", args{10, 100}, 0, 10},
		{"101.0011.0000-1.0011", args{1328, 19}, 93, 7},
		{"110.1000-1011", args{104, 11}, 15, 1},
		{"111.1001-1011", args{121, 11}, 13, 6},
		{"1001 1101 0000-11001", args{2512, 25}, 226, 2},
		{"1001 1101 0010-11001", args{2514, 25}, 226, 0},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, got1 := OperationO(tt.args.a, tt.args.b)
			if got != tt.want {
				t.Errorf("OperationO() got = %v, want %v", got, tt.want)
			}
			if got1 != tt.want1 {
				t.Errorf("OperationO() got1 = %v, want %v", got1, tt.want1)
			}
		})
	}
}

func TestIntToBytes(t *testing.T) {
	type args struct {
		digit uint64
	}
	tests := []struct {
		name string
		args args
		want []byte
	}{
		// TODO: Add test cases.
		{"1", args{1}, []byte{1}},
		{"2", args{2}, []byte{1, 0}},
		{"4", args{4}, []byte{1, 0, 0}},
		{"5", args{5}, []byte{1, 0, 1}},
		{"6", args{6}, []byte{1, 1, 0}},
		{"7", args{7}, []byte{1, 1, 1}},
		{"17", args{17}, []byte{1, 0, 0, 0, 1}},
		{"127", args{127}, []byte{1, 1, 1, 1, 1, 1, 1}},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := IntToBytes(tt.args.digit); !reflect.DeepEqual(got, tt.want) {
				t.Errorf("IntToBytes() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestImposeError(t *testing.T) {
	type args struct {
		a uint64
		e uint64
	}
	tests := []struct {
		name string
		args args
		want uint64
	}{
		{"100_&_1", args{4, 1}, 5},
		{"100_&_2", args{4, 2}, 6},
		{"100_&_3", args{4, 3}, 7},
		{"100_&_4", args{4, 4}, 0},
		{"100_&_5", args{4, 5}, 1},
		{"100_&_6", args{4, 6}, 2},
		{"100_&_7", args{4, 7}, 3},
		{"1001_&_1", args{17, 1}, 16},
		{"1_&_1001", args{1, 17}, 16},
		{"0_&_1001", args{0, 17}, 17},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := ImposeError(tt.args.a, tt.args.e); got != tt.want {
				t.Errorf("ImposeError() = %v, want %v", got, tt.want)
			}
		})
	}
}