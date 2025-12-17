package main

import (
	"embed"
	"fmt"
	"html/template"
	"log"
	"net/http"
	"os"

	"github.com/gorilla/mux"
)

//go:embed templates static
var content embed.FS

type PageData struct {
	Version     string
	Environment string
}

func getEnv(key, defaultValue string) string {
	value := os.Getenv(key)
	if value == "" {
		return defaultValue
	}
	return value
}

func main() {
	version := getEnv("APP_VERSION", "1.0.0")
	environment := getEnv("ENVIRONMENT", "development")

	// Parse templates
	tmpl, err := template.ParseFS(content, "templates/*.html")
	if err != nil {
		log.Fatal("Error parsing templates:", err)
	}

	// Create router
	r := mux.NewRouter()

	// Main page handler
	r.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		data := PageData{
			Version:     version,
			Environment: environment,
		}
		if err := tmpl.ExecuteTemplate(w, "index.html", data); err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
		}
	})

	// Health check endpoint
	r.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		fmt.Fprintf(w, `{"status":"healthy","version":"%s"}`, version)
	})

	// Static files
	r.PathPrefix("/static/").Handler(http.FileServer(http.FS(content)))

	port := ":8080"
	log.Printf("🚀 Server starting on http://localhost%s", port)
	log.Printf("📦 Version: %s | Environment: %s", version, environment)

	if err := http.ListenAndServe(port, r); err != nil {
		log.Fatal("Server failed to start:", err)
	}
}
