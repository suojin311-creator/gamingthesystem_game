package main

import (
	"crypto/rand"
	"encoding/hex"
	"errors"
	"fmt"
	mathrand "math/rand"
	"sort"
	"strings"
	"sync"
	"unicode/utf8"
)

type Config struct{ WritingMS, CardMS, RankingMS, QuestionMS int64 }

var standardConfig = Config{90000, 10000, 5000, 4000}

type Participant struct {
	ID                            string
	Submitted, Audience, Finished bool
	Cursor                        int
	CardStart                     int64
}
type Reflection struct{ ID, Owner, Text, Label string }
type Ranked struct {
	ID      string `json:"id"`
	Label   string `json:"label"`
	Text    string `json:"text"`
	Flowers int    `json:"flowers"`
	Rank    int    `json:"rank"`
}
type Card struct {
	ID       string `json:"id"`
	Label    string `json:"label"`
	Text     string `json:"text"`
	Own      bool   `json:"own"`
	Deadline int64  `json:"deadline"`
	Vote     string `json:"vote"`
}
type Snapshot struct {
	Revision        uint64   `json:"revision"`
	SessionID       string   `json:"sessionId"`
	Phase           string   `json:"phase"`
	Now             int64    `json:"now"`
	StartedAt       int64    `json:"startedAt"`
	Deadline        int64    `json:"deadline"`
	Joined          int      `json:"joined"`
	Submitted       int      `json:"submitted"`
	AudienceCount   int      `json:"audienceCount"`
	ReflectionCount int      `json:"reflectionCount"`
	FinishedCount   int      `json:"finishedCount"`
	WritingMS       int64    `json:"writingMs"`
	CardMS          int64    `json:"cardMs"`
	RankingMS       int64    `json:"rankingMs"`
	ParticipantID   string   `json:"participantId,omitempty"`
	HasSubmitted    bool     `json:"hasSubmitted"`
	IsAudience      bool     `json:"isAudience"`
	Cursor          int      `json:"cursor"`
	Finished        bool     `json:"finished"`
	Card            *Card    `json:"card"`
	Ranking         []Ranked `json:"ranking"`
	JoinURLs        []string `json:"joinUrls,omitempty"`
}
type Session struct {
	mu                  sync.Mutex
	serial              uint64
	ID, Phase           string
	StartedAt, Deadline int64
	Participants        map[string]*Participant
	Reflections         []*Reflection
	Votes               map[string]map[string]string
	Ranking             []Ranked
	Config              Config
	now                 func() int64
	shuffle             *mathrand.Rand
}

func randomID() string {
	var b [16]byte
	if _, err := rand.Read(b[:]); err != nil {
		panic(err)
	}
	return hex.EncodeToString(b[:])
}
func newSession(c Config, now func() int64) *Session {
	return &Session{ID: randomID(), Phase: "lobby", Participants: map[string]*Participant{}, Reflections: []*Reflection{}, Votes: map[string]map[string]string{}, Ranking: []Ranked{}, Config: c, now: now, shuffle: mathrand.New(mathrand.NewSource(now()))}
}
func (s *Session) phase(name string, at, duration int64) {
	s.Phase = name
	s.StartedAt = at
	s.Deadline = 0
	if duration > 0 {
		s.Deadline = at + duration
	}
}

// All methods below run under mu. The server owns deadlines even when a browser sleeps.
func (s *Session) tick() {
	now := s.now()
	for {
		switch s.Phase {
		case "writing":
			if now < s.Deadline {
				return
			}
			s.beginReview(s.Deadline)
		case "review":
			all := true
			for _, p := range s.Participants {
				for p.Cursor < len(s.Reflections) && now >= p.CardStart+s.Config.CardMS {
					p.Cursor++
					p.CardStart += s.Config.CardMS
				}
				if now >= s.Deadline {
					p.Cursor = len(s.Reflections)
				}
				p.Finished = p.Cursor >= len(s.Reflections)
				if !p.Finished {
					all = false
				}
			}
			if !all {
				return
			}
			s.finishReview(now)
		case "ranking":
			if now < s.Deadline {
				return
			}
			s.phase("question1", s.Deadline, s.Config.QuestionMS)
		case "question1":
			if now < s.Deadline {
				return
			}
			s.phase("question2", s.Deadline, s.Config.QuestionMS)
		case "question2":
			if now < s.Deadline {
				return
			}
			s.phase("ending", s.Deadline, 0)
		default:
			return
		}
	}
}
func (s *Session) join(previous string) (string, error) {
	s.tick()
	if _, ok := s.Participants[previous]; ok {
		return previous, nil
	}
	if s.Phase != "lobby" && s.Phase != "writing" {
		return "", errors.New("This lab has already started. Please check with your teacher.")
	}
	id := randomID()
	s.Participants[id] = &Participant{ID: id}
	return id, nil
}
func (s *Session) start() error {
	s.tick()
	if s.Phase != "lobby" {
		return errors.New("The lab has already started.")
	}
	if len(s.Participants) == 0 {
		return errors.New("Open the participant page before starting.")
	}
	s.phase("writing", s.now(), s.Config.WritingMS)
	return nil
}
func (s *Session) submit(id, text string, audience bool) error {
	s.tick()
	p := s.Participants[id]
	if p == nil {
		return errors.New("Please join the lab first.")
	}
	text = strings.TrimSpace(text)
	if p.Submitted {
		for _, r := range s.Reflections {
			if r.Owner == id && r.Text == text {
				return nil
			}
		}
		return errors.New("Your reflection has already been submitted.")
	}
	if s.Phase != "writing" {
		return errors.New("Writing has ended.")
	}
	if p.Audience {
		return errors.New("You have joined the audience.")
	}
	if audience {
		p.Audience = true
		return nil
	}
	if text == "" || utf8.RuneCountInString(text) > 240 {
		return errors.New("Please write between 1 and 240 characters.")
	}
	s.Reflections = append(s.Reflections, &Reflection{ID: randomID(), Owner: id, Text: text})
	p.Submitted = true
	return nil
}
func (s *Session) beginReview(at int64) {
	if len(s.Reflections) == 0 {
		s.phase("empty", at, 0)
		return
	}
	s.shuffle.Shuffle(len(s.Reflections), func(i, j int) { s.Reflections[i], s.Reflections[j] = s.Reflections[j], s.Reflections[i] })
	for i, r := range s.Reflections {
		r.Label = fmt.Sprintf("Reflection %02d", i+1)
	}
	for _, p := range s.Participants {
		p.Cursor = 0
		p.CardStart = at
		p.Finished = false
	}
	s.phase("review", at, int64(len(s.Reflections))*s.Config.CardMS)
}
func (s *Session) current(id, expected string) (*Participant, *Reflection, error) {
	s.tick()
	p := s.Participants[id]
	if s.Phase != "review" || p == nil || p.Finished || p.Cursor >= len(s.Reflections) {
		return nil, nil, errors.New("This review has ended.")
	}
	r := s.Reflections[p.Cursor]
	if r.ID != expected {
		return nil, nil, errors.New("That reflection has ended.")
	}
	return p, r, nil
}
func (s *Session) vote(id, expected, choice string) error {
	_, r, err := s.current(id, expected)
	if err != nil {
		return err
	}
	if r.Owner == id {
		return errors.New("This is your own reflection.")
	}
	if choice != "flower" && choice != "bomb" {
		return errors.New("Choose flowers or a bomb.")
	}
	if s.Votes[id] == nil {
		s.Votes[id] = map[string]string{}
	}
	if previous, ok := s.Votes[id][r.ID]; ok {
		if previous == choice {
			return nil
		}
		return errors.New("Your choice has already been recorded.")
	}
	s.Votes[id][r.ID] = choice
	return nil
}
func (s *Session) advance(id, expected string) error {
	p, r, err := s.current(id, expected)
	if err != nil {
		return err
	}
	if r.Owner != id && s.Votes[id][r.ID] == "" {
		return errors.New("Choose one before continuing.")
	}
	p.Cursor++
	p.CardStart = s.now()
	p.Finished = p.Cursor >= len(s.Reflections)
	s.tick()
	return nil
}
func (s *Session) finishReview(at int64) {
	rows := make([]Ranked, 0, len(s.Reflections))
	for _, r := range s.Reflections {
		flowers := 0
		for _, votes := range s.Votes {
			if votes[r.ID] == "flower" {
				flowers++
			}
		}
		rows = append(rows, Ranked{ID: r.ID, Label: r.Label, Text: r.Text, Flowers: flowers})
	}
	// The initial anonymous shuffle supplies the fixed order within equal scores.
	sort.SliceStable(rows, func(i, j int) bool { return rows[i].Flowers > rows[j].Flowers })
	for i := range rows {
		if i > 0 && rows[i].Flowers == rows[i-1].Flowers {
			rows[i].Rank = rows[i-1].Rank
		} else {
			rows[i].Rank = i + 1
		}
	}
	s.Ranking = rows
	s.phase("ranking", at, s.Config.RankingMS)
}
func (s *Session) closeQuestions() error {
	s.tick()
	if s.Phase != "empty" {
		return errors.New("The closing is not ready yet.")
	}
	s.phase("ending", s.now(), 0)
	return nil
}
func (s *Session) snapshot(id string) Snapshot {
	s.tick()
	s.serial++
	v := Snapshot{SessionID: s.ID, Phase: s.Phase, Now: s.now(), StartedAt: s.StartedAt, Deadline: s.Deadline, Joined: len(s.Participants), ReflectionCount: len(s.Reflections), WritingMS: s.Config.WritingMS, CardMS: s.Config.CardMS, RankingMS: s.Config.RankingMS, Ranking: []Ranked{}}
	v.Revision = s.serial
	for _, p := range s.Participants {
		if p.Submitted {
			v.Submitted++
		}
		if p.Audience {
			v.AudienceCount++
		}
		if p.Finished {
			v.FinishedCount++
		}
	}
	if p := s.Participants[id]; p != nil {
		v.ParticipantID = id
		v.HasSubmitted = p.Submitted
		v.IsAudience = p.Audience
		v.Cursor = p.Cursor
		v.Finished = p.Finished
		if s.Phase == "review" && !p.Finished && p.Cursor < len(s.Reflections) {
			r := s.Reflections[p.Cursor]
			v.Card = &Card{ID: r.ID, Label: r.Label, Text: r.Text, Own: r.Owner == id, Deadline: p.CardStart + s.Config.CardMS, Vote: s.Votes[id][r.ID]}
		}
	}
	if s.Phase == "ranking" || s.Phase == "question1" || s.Phase == "question2" || s.Phase == "ending" {
		v.Ranking = s.Ranking
	}
	return v
}
