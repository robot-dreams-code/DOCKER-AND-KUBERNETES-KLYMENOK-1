package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"strconv"
)

const counterFile = "/app/data/counter.txt"

func loadCounter() int {
	data, err := ioutil.ReadFile(counterFile)
	if err != nil {
		return 0
	}
	n, err := strconv.Atoi(string(data))
	if err != nil {
		return 0
	}
	return n
}

func saveCounter(n int) {
	ioutil.WriteFile(counterFile, []byte(strconv.Itoa(n)), 0644)
}

func mainHandler(w http.ResponseWriter, r *http.Request) {
	// реагуємо тільки на /
	if r.URL.Path != "/" {
		http.NotFound(w, r)
		return
	}

	counter := loadCounter()
	counter++
	saveCounter(counter)

	html := fmt.Sprintf(`<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="UTF-8">
<title>Домашнє завдання 05</title>
<style>
body { display:flex; justify-content:center; align-items:center; height:100vh; margin:0; font-family:Arial,sans-serif; background-color:#f5f5f5; }
h1 { color:#333; font-size:32px; }
</style>
</head>
<body>
<h1>Лічильник відвідувань: %d</h1>
</body>
</html>`, counter)

	fmt.Fprint(w, html)
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprint(w, "OK")
}

func main() {
	// гарантуємо наявність каталогу
	os.MkdirAll("/app/data", 0755)

	http.HandleFunc("/", mainHandler)
	http.HandleFunc("/healthz", healthHandler)

	fmt.Println("Server running on port 8080")
	http.ListenAndServe(":8080", nil)
}
