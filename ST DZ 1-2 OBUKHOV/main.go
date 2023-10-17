package main


import (
	"fmt"
	"html/template"
	"math/bits"
	"net/http"
)

type ResultRow struct {
	CorrectiveAbility string
	Count             uint64
	ClassSize         int
}

var DEBUG bool = false

const n = 15
const k = 11
const informationVector = 83        // 000.0101.0011b
const codedInformationVector = 1335 // 000.0101.0011.0111b
const genPolynomial = 19            // 10011b
var result = make([]ResultRow, n+1)
var errorClasses = getErrorsByClasses(n)
var syndromeTable = getSyndromeTable(errorClasses[1], genPolynomial)

func powBinary(n uint64) uint64 {
	res := uint64(1)
	for i := uint64(1); i <= n; i++ {
		res <<= 1
	}
	return res
}

func getBinaryLength(digit uint64) uint64 {
	bitsNum := uint64(0)
	for ; digit/2 != 0; digit /= 2 {
		bitsNum++
	}
	bitsNum++
	return bitsNum
}

func IntToBytes(digit uint64) []byte {
	var res []byte
	for i := powBinary(getBinaryLength(digit) - 1); i > 0; i /= 2 {
		res = append(res, byte(digit/i))
		digit %= i
	}
	return res
}

func factorial(n uint64) (result uint64) {
	if n > 0 {
		result = n * factorial(n-1)
		return result
	}
	return 1
}

func ImposeError(a, e uint64) uint64 {
	aBytes := IntToBytes(a)
	eBytes := IntToBytes(e)

	if len(aBytes) > len(eBytes) {
		eBytes = append(make([]byte, len(aBytes)-len(eBytes)), eBytes...)
	} else {
		aBytes = append(make([]byte, len(eBytes)-len(aBytes)), aBytes...)
	}

	for pos, eByte := range eBytes {
		if eByte == 1 {
			if aBytes[pos] == 1 {
				aBytes[pos] = 0
				continue
			}
			aBytes[pos] = 1
		}
	}
	a = 0
	for _, val := range aBytes {
		a <<= 1
		a += uint64(val)
	}
	return a
}

func OperationO(a, b uint64) (uint64, uint64) {
	if a < b {
		return 0, a
	}

	var integer uint64
	aBytes := IntToBytes(a)
	bLen := getBinaryLength(b)
	var cur uint64

	aBytesPos := uint64(0)
	for ; aBytesPos < bLen; aBytesPos++ {
		cur <<= 1
		cur += uint64(aBytes[aBytesPos])
	}

	for ; aBytesPos <= uint64(len(aBytes)); aBytesPos++ {
		firstBitInCur := cur / powBinary(bLen-1)
		integer <<= 1
		integer += firstBitInCur

		if firstBitInCur == 1 {
			cur ^= b
		}
		if aBytesPos == uint64(len(aBytes)) {
			break
		}

		cur <<= 1
		cur += uint64(aBytes[aBytesPos])
	}

	return integer, cur
}

func getErrorsByClasses(n uint64) [][]uint64 {
	errorClasses := make([][]uint64, n+1)
	for i := uint64(1); i <= n; i++ {
		size := factorial(n) / factorial(n-i) / factorial(i)
		errorClasses[i] = make([]uint64, 0, size)
	}

	for i := uint64(1); i < powBinary(n); i++ {
		class := bits.OnesCount64(i)
		errorClasses[class] = append(errorClasses[class], i)
	}
	return errorClasses
}

func getErrorsByClassesString(errorClasses [][]uint64) [][]string {
	errorsView := make([][]string, len(errorClasses))
	for class, errorClass := range errorClasses {
		errorsView[class] = make([]string, len(errorClass))
		for i, err := range errorClass {
			errorsView[class][i] = fmt.Sprintf("%b", err)
		}
	}
	return errorsView
}

func ErrorPage(w http.ResponseWriter, r *http.Request) {
	errorsView := getErrorsByClassesString(errorClasses)

	tmpl, _ := template.ParseFiles("./templates/errors.html")
	tmpl.Execute(w, errorsView)
}

func getSyndromeTable(errorVectors []uint64, genPolynomial uint64) map[uint64]uint64 {
	errorMap := make(map[uint64]uint64, len(errorVectors))
	for _, err := range errorVectors {
		_, syndrome := OperationO(err, genPolynomial)
		errorMap[syndrome] = err
	}
	return errorMap
}

func syndromeTableToString(syndromeTable map[uint64]uint64) map[string]string {
	syndromeTableStr := make(map[string]string, len(syndromeTable))
	for syndrome, err := range syndromeTable {
		syndromeTableStr[fmt.Sprintf("%b", syndrome)] = fmt.Sprintf("%b", err)
	}
	return syndromeTableStr
}

func SyndromePage(w http.ResponseWriter, r *http.Request) {
	syndromeView := syndromeTableToString(syndromeTable)

	tmpl, _ := template.ParseFiles("./templates/syndromes.html")
	tmpl.Execute(w, syndromeView)
}

func getSyndromeArrayStr(n, genPolynomial uint64) map[string]string {
	errorMap := make(map[string]string, powBinary(n))
	for i := uint64(1); i < powBinary(n); i++ {
		_, syndrome := OperationO(i, genPolynomial)
		errorMap[fmt.Sprintf("%b", i)] = fmt.Sprintf("%b", syndrome)
	}
	return errorMap
}

func SyndromeArrayPage(w http.ResponseWriter, r *http.Request) {
	errorMap := getSyndromeArrayStr(n, genPolynomial)

	tmpl, _ := template.ParseFiles("./templates/syndromesArray.html")
	tmpl.Execute(w, errorMap)
}

func ResultsPage(w http.ResponseWriter, r *http.Request) {
	tmpl, _ := template.ParseFiles("./templates/results.html")
	tmpl.Execute(w, result)
}

func main() {
	if DEBUG {
		fmt.Printf("syndromeTable: %v\n", syndromeTable)
	}
	for class, errorClass := range errorClasses {
		var correctedCounter uint64
		for _, errorVector := range errorClass {
			transferredVector := ImposeError(codedInformationVector, errorVector)
			if DEBUG && class == 1 {
				fmt.Printf("\ntransferredVector: %b\n", transferredVector)
			}
			_, syndrome := OperationO(transferredVector, genPolynomial)
			if DEBUG && class == 1 {
				fmt.Printf("syndrome: %b\n", syndrome)
			}
			if syndrome == 0 {
				continue
			}
			correctedVector := ImposeError(transferredVector, syndromeTable[syndrome])
			if DEBUG && class == 1 {
				fmt.Printf("correctedVector: %b\n", correctedVector)
			}
			if correctedVector == codedInformationVector {
				correctedCounter++
				if DEBUG && class == 1 {
					fmt.Printf("eror corrected successfully | counter: %d\n", correctedCounter)
				}
			}
		}
		result[class] = ResultRow{
			fmt.Sprintf("%.2f", float64(correctedCounter)*100/float64(len(errorClass))),
			correctedCounter,
			len(errorClass),
		}
	}

	http.HandleFunc("/", ErrorPage)
	http.HandleFunc("/syndromes/", SyndromePage)
	http.HandleFunc("/syndromes/array", SyndromeArrayPage)
	http.HandleFunc("/results/", ResultsPage)
	http.ListenAndServe(":8080", nil)

}
