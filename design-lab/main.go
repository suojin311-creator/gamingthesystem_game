package main

import (
	"context"
	"embed"
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"io/fs"
	"net"
	"net/http"
	"os"
	"os/exec"
	"os/signal"
	"runtime"
	"strconv"
	"strings"
	"time"
)

//go:embed web
var embeddedWeb embed.FS

type application struct {
	session *Session
	urls    []string
	server  *http.Server
	files   http.Handler
}
type actionBody struct {
	ParticipantID string `json:"participantId"`
	Text          string `json:"text"`
	ReflectionID  string `json:"reflectionId"`
	Choice        string `json:"choice"`
	Audience      bool   `json:"audience"`
}

func local(r *http.Request) bool {
	host, _, err := net.SplitHostPort(r.RemoteAddr)
	if err != nil {
		return false
	}
	ip := net.ParseIP(host)
	return ip != nil && ip.IsLoopback()
}
func writeJSON(w http.ResponseWriter, status int, v any) {
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.Header().Set("Cache-Control", "no-store")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(v)
}
func (a *application) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("X-Content-Type-Options", "nosniff")
	w.Header().Set("Referrer-Policy", "same-origin")
	w.Header().Set("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; font-src 'self'; frame-ancestors 'none'")
	if r.URL.Path == "/host" && !local(r) {
		http.Error(w, "Open the host page on the teacher's computer using localhost.", http.StatusForbidden)
		return
	}
	if strings.HasPrefix(r.URL.Path, "/api/") {
		a.api(w, r)
		return
	}
	if r.Method != "GET" && r.Method != "HEAD" {
		http.Error(w, "Method not allowed", 405)
		return
	}
	if r.URL.Path == "/" || r.URL.Path == "/host" || r.URL.Path == "/display" {
		data, err := embeddedWeb.ReadFile("web/index.html")
		if err != nil {
			http.Error(w, "Build the Design Lab interface first.", 500)
			return
		}
		w.Header().Set("Content-Type", "text/html; charset=utf-8")
		w.Header().Set("Cache-Control", "no-cache")
		_, _ = w.Write(data)
		return
	}
	a.files.ServeHTTP(w, r)
}
func (a *application) api(w http.ResponseWriter, r *http.Request) {
	isHost := strings.HasPrefix(r.URL.Path, "/api/host/")
	if isHost && !local(r) {
		writeJSON(w, 403, map[string]string{"error": "Use the host page on the teacher's computer."})
		return
	}
	if r.Method != "GET" && r.Method != "POST" {
		writeJSON(w, 405, map[string]string{"error": "Method not allowed."})
		return
	}
	var body actionBody
	if r.Method == "POST" {
		if err := json.NewDecoder(http.MaxBytesReader(w, r.Body, 8192)).Decode(&body); err != nil {
			writeJSON(w, 400, map[string]string{"error": "The request could not be read."})
			return
		}
	}
	s := a.session
	s.mu.Lock()
	defer s.mu.Unlock()
	s.tick()
	id := r.Header.Get("X-Participant")
	if body.ParticipantID != "" {
		id = body.ParticipantID
	}
	var err error
	switch r.URL.Path {
	case "/api/join":
		if r.Method != "POST" {
			writeJSON(w, 405, map[string]string{"error": "Use POST."})
			return
		}
		id, err = s.join(id)
	case "/api/state":
		if r.Method != "GET" {
			writeJSON(w, 405, map[string]string{"error": "Use GET."})
			return
		}
		if _, exists := s.Participants[id]; !exists {
			writeJSON(w, 401, map[string]string{"error": "Please join the lab first."})
			return
		}
	case "/api/display":
		if r.Method != "GET" {
			writeJSON(w, 405, map[string]string{"error": "Use GET."})
			return
		}
	case "/api/submit":
		if r.Method != "POST" {
			writeJSON(w, 405, map[string]string{"error": "Use POST."})
			return
		}
		err = s.submit(id, body.Text, body.Audience)
	case "/api/vote":
		if r.Method != "POST" {
			writeJSON(w, 405, map[string]string{"error": "Use POST."})
			return
		}
		err = s.vote(id, body.ReflectionID, body.Choice)
	case "/api/next":
		if r.Method != "POST" {
			writeJSON(w, 405, map[string]string{"error": "Use POST."})
			return
		}
		err = s.advance(id, body.ReflectionID)
	case "/api/host/state":
		if r.Method != "GET" {
			writeJSON(w, 405, map[string]string{"error": "Use GET."})
			return
		}
	case "/api/host/start":
		if r.Method != "POST" {
			writeJSON(w, 405, map[string]string{"error": "Use POST."})
			return
		}
		err = s.start()
	case "/api/host/ending":
		if r.Method != "POST" {
			writeJSON(w, 405, map[string]string{"error": "Use POST."})
			return
		}
		err = s.closeQuestions()
	case "/api/host/close":
		if r.Method != "POST" {
			writeJSON(w, 405, map[string]string{"error": "Use POST."})
			return
		}
		s.phase("closed", s.now(), 0)
		go func() {
			time.Sleep(900 * time.Millisecond)
			ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
			defer cancel()
			_ = a.server.Shutdown(ctx)
		}()
	default:
		writeJSON(w, 404, map[string]string{"error": "Not found."})
		return
	}
	v := s.snapshot(id)
	if isHost {
		v.JoinURLs = a.urls
	}
	if err != nil {
		writeJSON(w, 409, map[string]any{"error": err.Error(), "state": v})
		return
	}
	writeJSON(w, 200, v)
}
func networkURLs(port int) []string {
	addresses, _ := net.InterfaceAddrs()
	urls := []string{}
	for _, addr := range addresses {
		ip, _, err := net.ParseCIDR(addr.String())
		if err == nil && ip.To4() != nil && !ip.IsLoopback() {
			urls = append(urls, fmt.Sprintf("http://%s:%d", ip.String(), port))
		}
	}
	return urls
}
func openBrowser(url string) {
	var c *exec.Cmd
	switch runtime.GOOS {
	case "windows":
		c = exec.Command("rundll32", "url.dll,FileProtocolHandler", url)
	case "darwin":
		c = exec.Command("open", url)
	default:
		c = exec.Command("xdg-open", url)
	}
	_ = c.Start()
}
func run() error {
	port := flag.Int("port", 3000, "Classroom port (0 chooses an available port)")
	noBrowser := flag.Bool("no-browser", false, "Do not open the host page automatically")
	writing := flag.Float64("writing-seconds", 90, "Writing duration; classroom default: 90 seconds")
	ranking := flag.Float64("ranking-seconds", 12, "Static ranking duration")
	question := flag.Float64("question-seconds", 4, "Duration of each closing question")
	flag.Parse()
	if *writing <= 0 || *ranking <= 0 || *question <= 0 {
		return errors.New("All durations must be positive.")
	}
	var listener net.Listener
	var err error
	for attempt := 0; attempt < 10; attempt++ {
		p := *port
		if p != 0 {
			p += attempt
		}
		listener, err = net.Listen("tcp4", ":"+strconv.Itoa(p))
		if err == nil {
			break
		}
		if *port == 0 {
			break
		}
	}
	if err != nil {
		return fmt.Errorf("cannot start the classroom: %w", err)
	}
	actualPort := listener.Addr().(*net.TCPAddr).Port
	config := Config{int64(*writing * 1000), int64(*ranking * 1000), int64(*question * 1000)}
	for _, ms := range []int64{config.WritingMS, config.RankingMS, config.QuestionMS} {
		if ms < 1 {
			return errors.New("Durations must be at least one millisecond.")
		}
	}
	s := newSession(config, func() int64 { return time.Now().UnixMilli() })
	files, err := fs.Sub(embeddedWeb, "web")
	if err != nil {
		return err
	}
	a := &application{session: s, urls: networkURLs(actualPort), files: http.FileServer(http.FS(files))}
	a.server = &http.Server{Handler: a, ReadHeaderTimeout: 5 * time.Second, ReadTimeout: 10 * time.Second, WriteTimeout: 10 * time.Second, IdleTimeout: 30 * time.Second}
	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt)
	defer stop()
	go func() {
		ticker := time.NewTicker(50 * time.Millisecond)
		defer ticker.Stop()
		for {
			select {
			case <-ticker.C:
				s.mu.Lock()
				s.tick()
				s.mu.Unlock()
			case <-ctx.Done():
				shutdown, cancel := context.WithTimeout(context.Background(), 3*time.Second)
				_ = a.server.Shutdown(shutdown)
				cancel()
				return
			}
		}
	}()
	hostURL := fmt.Sprintf("http://localhost:%d/host", actualPort)
	fmt.Println("DESIGN LAB - LOCAL CLASSROOM")
	fmt.Println("Host:", hostURL)
	fmt.Println("Participant on this computer:", fmt.Sprintf("http://localhost:%d", actualPort))
	for _, url := range a.urls {
		fmt.Println("Share with the class:", url)
	}
	fmt.Println("Keep this window open. Close the classroom from the host page when finished.")
	if !*noBrowser {
		go func() { time.Sleep(250 * time.Millisecond); openBrowser(hostURL) }()
	}
	err = a.server.Serve(listener)
	if errors.Is(err, http.ErrServerClosed) {
		return nil
	}
	return err
}
func main() {
	if err := run(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		if runtime.GOOS == "windows" {
			fmt.Println("Press Enter to close.")
			_, _ = fmt.Scanln()
		}
		os.Exit(1)
	}
}
