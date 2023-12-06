package main

import (
	"fmt"
	"html/template"
	"math/bits"
	"net/http"
)

const n = 15
const k = 11
const informationVector = 83         // 000.0101.0011b
const codedInformationVector = 1335  // 000.0101.0011.0111b
const genPolynomial = 19             // 10011b
var result = make(map[int]string, n + 1)
var errorClasses = getErrorsByClasses(n)
var symptomTablesByClasses = getSymptomTablesByClasses(errorClasses, genPolynomial)

func powBinary(n uint64) uint64 {
	res := uint64(1)
	for i := uint64(1); i <= n; i++ {
		res <<= 1
	}
	return res
}

func getBinaryLength(digit uint64) uint64 {
	bitsNum := uint64(0)
	for ; digit / 2 != 0; digit /= 2 {
		bitsNum++
	}
	bitsNum++
	return bitsNum
}

func IntToBytes(digit uint64) []byte {
	var res []byte
	for i := powBinary(getBinaryLength(digit) - 1); i > 0; i /= 2 {
		res = append(res, byte(digit / i))
		digit %= i
	}
	return res
}

func factorial(n uint64)(result uint64) {
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
		eBytes = append(make([]byte, len(aBytes) - len(eBytes)), eBytes...)
	} else {
		aBytes = append(make([]byte, len(eBytes) - len(aBytes)), aBytes...)
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
		firstBitInCur := cur / powBinary(bLen - 1)
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
	errorClasses := make([][]uint64, n + 1)
	for i := uint64(1); i <= n; i++ {
		size := factorial(n) / factorial(n-i) / factorial(i)
		errorClasses[i] = make([]uint64, 0, size)
	}

	for i := uint64(1); i < powBinary(n); i++ {
		class := bits.OnesCount64(i)
		errorClasses[class] = append(errorClasses[class], i)
	}
	return  errorClasses
}

func getErrorsByClassesString(errorClasses [][]uint64) [][]string {
	errorsView := make([][]string, len(errorClasses))
	for class, errorClass := range errorClasses {
		errorsView[class] = make([]string, len(errorClass))
		for i, err := range errorClass{
			errorsView[class][i] = fmt.Sprintf("%b",err)
		}
	}
	return errorsView
}

func ErrorPage(w http.ResponseWriter, r *http.Request) {
	errorsView := getErrorsByClassesString(errorClasses)

	tmpl, _ := template.ParseFiles("./templates/errors.html")
	tmpl.Execute(w, errorsView)
}

func getSymptomTableForErrorList(errorVectors []uint64, genPolynomial uint64) map[uint64] uint64 {
	errorMap := make(map[uint64] uint64, len(errorVectors))
	for _, err := range errorVectors{
		_, symptom := OperationO(err, genPolynomial)
		errorMap[symptom] = err
	}
	return errorMap
}

func getSymptomTablesByClasses(errorsByClasses [][]uint64, genPolynomial uint64) []map[uint64]uint64 {
	symptomTables := make([]map[uint64]uint64, len(errorsByClasses))
	for i, errorsClass := range errorsByClasses {
		symptomTables[i] = getSymptomTableForErrorList(errorsClass, genPolynomial)
	}
	return symptomTables
}

func getSymptomTablesByClassesString(symptomTablesByClasses []map[uint64]uint64) []map[string]string {
	res := make([]map[string]string, len(symptomTablesByClasses))
	for class, symptomTable := range symptomTablesByClasses {
		res[class] = make(map[string]string, len(symptomTable))
		for symptom, err := range symptomTable {
			res[class][fmt.Sprintf("%b", symptom)] = fmt.Sprintf("%b", err)
		}
	}
	return res
}

func SymptomPage(w http.ResponseWriter, r *http.Request) {
	symptomView := getSymptomTablesByClassesString(symptomTablesByClasses)

	tmpl, _ := template.ParseFiles("./templates/symptoms.html")
	tmpl.Execute(w, symptomView)
}

func getSymptomArrayStr(n, genPolynomial uint64) map[string] string {
	errorMap := make(map[string] string, powBinary(n))
	for i := uint64(1); i < powBinary(n); i++ {
		_, symptom := OperationO(i, genPolynomial)
		errorMap[fmt.Sprintf("%b", i)] = fmt.Sprintf("%b", symptom)
	}
	return errorMap
}

func SymptomArrayPage(w http.ResponseWriter, r *http.Request) {
	errorMap := getSymptomArrayStr(n, genPolynomial)

	tmpl, _ := template.ParseFiles("./templates/symptomsArray.html")
	tmpl.Execute(w, errorMap)
}

func ResultsPage(w http.ResponseWriter, r *http.Request) {
	tmpl, _ := template.ParseFiles("./templates/results.html")
	tmpl.Execute(w, result)
}


func main() {
	for class, errorClass := range errorClasses {
		symptomTable := symptomTablesByClasses[class]
		var correctedCounter uint64
		for _, errorVector := range errorClass {
			transferredVector := ImposeError(codedInformationVector, errorVector)
			_, symptom := OperationO(transferredVector, genPolynomial)
			if symptom == 0 {
				continue
			}
			correctedVector := ImposeError(transferredVector, symptomTable[symptom])
			decodedMessage := correctedVector >> (n - k)
			if decodedMessage == informationVector {
				correctedCounter++
			}
		}
		result[class] = fmt.Sprintf("%.2f", float64(correctedCounter) * 100 /  float64(len(errorClass)))
	}

	http.HandleFunc("/", ErrorPage)
	http.HandleFunc("/symptoms/", SymptomPage)
	http.HandleFunc("/symptoms/array", SymptomArrayPage)
	http.HandleFunc("/results/", ResultsPage)
	http.ListenAndServe(":8080", nil)

}