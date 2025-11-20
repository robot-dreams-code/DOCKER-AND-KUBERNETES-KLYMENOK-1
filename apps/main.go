package main

import (
	"fmt"
	"net/http"
)

func handler(w http.ResponseWriter, r *http.Request) {
	html := `
	<!DOCTYPE html>
	<html lang="uk">
	<head>
		<meta charset="UTF-8">
		<title>Домашнє завдання</title>
		<style>
			body {
				display: flex;
				justify-content: center;
				align-items: center;
				height: 100vh;
				margin: 0;
				font-family: Arial, sans-serif;
				background-color: #f5f5f5;
			}
			h1 {
				color: #333;
				font-size: 32px;
			}
		</style>
	</head>
	<body>
		<h1>Виконання домашнего завдання по уроку 3</h1>
	</body>
	</html>
	`
	fmt.Fprint(w, html)
}

func main() {
	http.HandleFunc("/", handler)
	fmt.Println("Server running on port 8080")
	http.ListenAndServe(":8080", nil)
}
