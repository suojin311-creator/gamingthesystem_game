package main

import (
	"encoding/json"
	"fmt"
	"strings"
	"sync"
	"testing"
)

func fixture(t *testing.T, count int) (*Session, *int64, []string) {
	t.Helper()
	now := int64(1000000)
	s := newSession(standardConfig, func() int64 { return now })
	ids := []string{}
	for i := 0; i < count; i++ {
		id, err := s.join("")
		if err != nil {
			t.Fatal(err)
		}
		ids = append(ids, id)
	}
	if err := s.start(); err != nil {
		t.Fatal(err)
	}
	return s, &now, ids
}
func share(t *testing.T, s *Session, ids []string) {
	t.Helper()
	for i, id := range ids {
		if err := s.submit(id, fmt.Sprintf("Claim %d: reward understanding, not appearances.", i), false); err != nil {
			t.Fatal(err)
		}
	}
}
func TestProductionWritingAndUntimedReview(t *testing.T) {
	s, now, ids := fixture(t, 21)
	share(t, s, ids)
	*now = s.Deadline - 1
	s.tick()
	if s.Phase != "writing" {
		t.Fatal("writing ended early")
	}
	*now++
	s.tick()
	if s.Phase != "review" || s.Deadline != 0 {
		t.Fatal("review must have no deadline")
	}
	card := s.snapshot(ids[0]).Card
	*now += 3600000
	s.tick()
	next := s.snapshot(ids[0]).Card
	if s.Phase != "review" || card == nil || next == nil || card.ID != next.ID {
		t.Fatal("an unanswered card advanced with time")
	}
	if len(s.Votes[ids[0]]) != 0 {
		t.Fatal("waiting must not create a vote")
	}
	if s.Config.RankingMS != 12000 || s.Config.WritingMS != 90000 {
		t.Fatal("production timing changed")
	}
}
func TestEachAuthorSeesOnlyOthersExactlyOnce(t *testing.T) {
	s, now, ids := fixture(t, 21)
	share(t, s, ids)
	*now = s.Deadline
	s.tick()
	for _, id := range ids {
		seen := map[string]bool{}
		for !s.Participants[id].Finished {
			view := s.snapshot(id)
			c := view.Card
			if c == nil || view.ReviewTotal != 20 || view.Cursor != len(seen) {
				t.Fatal("incorrect personal queue")
			}
			for _, r := range s.Reflections {
				if r.ID == c.ID && r.Owner == id {
					t.Fatal("author received their own card")
				}
			}
			if seen[c.ID] {
				t.Fatal("duplicate reflection")
			}
			seen[c.ID] = true
			if err := s.vote(id, c.ID, "flower"); err != nil {
				t.Fatal(err)
			}
			if err := s.advance(id, c.ID); err != nil {
				t.Fatal(err)
			}
		}
		if len(seen) != 20 {
			t.Fatal("missing other authors")
		}
	}
	if s.Phase != "ranking" {
		t.Fatal(s.Phase)
	}
}
func TestVoteLocksAndNextIsPersonal(t *testing.T) {
	s, now, ids := fixture(t, 3)
	share(t, s, ids)
	*now = s.Deadline
	s.tick()
	id := ids[0]
	card := s.snapshot(id).Card
	if err := s.advance(id, card.ID); err == nil {
		t.Fatal("early Next without a choice must not submit a skip")
	}
	if err := s.vote(id, card.ID, "flower"); err != nil {
		t.Fatal(err)
	}
	if err := s.vote(id, card.ID, "bomb"); err == nil {
		t.Fatal("a submitted choice changed")
	}
	if err := s.vote(id, card.ID, "flower"); err != nil {
		t.Fatal("same-choice network retry should be harmless")
	}
	other := s.Participants[ids[1]].Cursor
	if err := s.advance(id, card.ID); err != nil {
		t.Fatal(err)
	}
	if s.Participants[ids[1]].Cursor != other {
		t.Fatal("one person's Next moved another person")
	}
	if s.Votes[id][card.ID] != "flower" {
		t.Fatal("choice was not retained")
	}
}
func TestEarlyFinisherWaitsUntilAllChoicesAreMade(t *testing.T) {
	s, now, ids := fixture(t, 3)
	share(t, s, ids)
	*now = s.Deadline
	s.tick()
	id := ids[0]
	for !s.Participants[id].Finished {
		c := s.snapshot(id).Card
		if err := s.vote(id, c.ID, "flower"); err != nil {
			t.Fatal(err)
		}
		if err := s.advance(id, c.ID); err != nil {
			t.Fatal(err)
		}
	}
	if s.Phase != "review" || !s.snapshot(id).Finished {
		t.Fatal("early finisher did not enter waiting")
	}
	for _, other := range ids[1:] {
		for !s.Participants[other].Finished {
			c := s.snapshot(other).Card
			_ = s.vote(other, c.ID, "bomb")
			if err := s.advance(other, c.ID); err != nil {
				t.Fatal(err)
			}
		}
	}
	if s.Phase != "ranking" || s.StartedAt >= s.Deadline {
		t.Fatal("all finished should end sharing early")
	}
}
func TestRankingUsesFlowersOnlyAndStableCompetitionTies(t *testing.T) {
	s, now, ids := fixture(t, 4)
	share(t, s, ids)
	*now = s.Deadline
	s.tick()
	a, b, c, d := s.Reflections[0].ID, s.Reflections[1].ID, s.Reflections[2].ID, s.Reflections[3].ID
	s.Votes = map[string]map[string]string{"v1": {a: "flower", b: "flower", c: "bomb", d: "bomb"}, "v2": {a: "flower", b: "flower", c: "flower", d: "bomb"}}
	s.finishReview(*now)
	wantRanks := []int{1, 1, 3, 4}
	wantCounts := []int{2, 2, 1, 0}
	for i, r := range s.Ranking {
		if r.Rank != wantRanks[i] || r.Flowers != wantCounts[i] {
			t.Fatalf("unexpected ranking: %+v", s.Ranking)
		}
	}
	if s.Ranking[0].ID != a || s.Ranking[1].ID != b {
		t.Fatal("tied reflections reordered")
	}
	frozen, _ := json.Marshal(s.Ranking)
	for i := 0; i < 5; i++ {
		s.tick()
		s.snapshot(ids[0])
	}
	after, _ := json.Marshal(s.Ranking)
	if string(frozen) != string(after) {
		t.Fatal("ranking changed during presentation")
	}
	if err := s.vote(ids[0], a, "flower"); err == nil {
		t.Fatal("votes reopened after ranking")
	}
}
func TestSnapshotNeverPublishesAuthorsOrVotesBeforeRanking(t *testing.T) {
	s, now, ids := fixture(t, 2)
	share(t, s, ids)
	before, _ := json.Marshal(s.snapshot(ids[0]))
	if strings.Contains(string(before), "Claim 0") || strings.Contains(string(before), "Claim 1") {
		t.Fatal("writing leaked other work")
	}
	*now = s.Deadline
	s.tick()
	b, _ := json.Marshal(s.snapshot(ids[0]))
	for _, id := range ids[1:] {
		if strings.Contains(string(b), id) {
			t.Fatal("another participant's identity was published")
		}
	}
	if len(s.snapshot(ids[0]).Ranking) != 0 {
		t.Fatal("live ranking exposed during voting")
	}
}
func TestClosingSequenceAndEmptyClass(t *testing.T) {
	s, now, ids := fixture(t, 1)
	share(t, s, ids)
	*now = s.Deadline
	s.tick()
	if s.snapshot(ids[0]).Card != nil {
		t.Fatal("the only author must not review their own work")
	}
	if s.Phase != "ranking" {
		t.Fatal(s.Phase)
	}
	*now = s.Deadline
	s.tick()
	if s.Phase != "question1" || s.Deadline-s.StartedAt != 4000 {
		t.Fatal(s.Phase)
	}
	*now = s.Deadline - 1
	s.tick()
	if s.Phase != "question1" {
		t.Fatal("first question ended early")
	}
	*now = s.Deadline
	s.tick()
	if s.Phase != "question2" {
		t.Fatal(s.Phase)
	}
	if s.Deadline-s.StartedAt != 4000 {
		t.Fatal("each closing question must last four seconds")
	}
	if err := s.closeQuestions(); err == nil {
		t.Fatal("a manual reveal must not shorten the closing question")
	}
	*now = s.Deadline - 1
	s.tick()
	if s.Phase != "question2" {
		t.Fatal("second question ended early")
	}
	*now++
	s.tick()
	if s.Phase != "ending" || s.Deadline != 0 {
		t.Fatal("second question must advance automatically to the theory")
	}

	empty, clock, _ := fixture(t, 2)
	*clock = empty.Deadline
	empty.tick()
	if empty.Phase != "empty" {
		t.Fatal("empty class tried to rank nonexistent work")
	}
	if err := empty.closeQuestions(); err != nil {
		t.Fatal(err)
	}
}
func TestConcurrentClassSubmissionsAndVotes(t *testing.T) {
	s, now, ids := fixture(t, 21)
	var wg sync.WaitGroup
	for i, id := range ids {
		wg.Add(1)
		go func(i int, id string) {
			defer wg.Done()
			s.mu.Lock()
			defer s.mu.Unlock()
			if err := s.submit(id, fmt.Sprintf("Class contribution %d", i), false); err != nil {
				t.Error(err)
			}
		}(i, id)
	}
	wg.Wait()
	*now = s.Deadline
	s.tick()
	for _, id := range ids {
		wg.Add(1)
		go func(id string) {
			defer wg.Done()
			for {
				s.mu.Lock()
				if s.Participants[id].Finished {
					s.mu.Unlock()
					return
				}
				c := s.snapshot(id).Card
				if err := s.vote(id, c.ID, "flower"); err != nil {
					t.Error(err)
				}
				if err := s.advance(id, c.ID); err != nil {
					t.Error(err)
				}
				s.mu.Unlock()
			}
		}(id)
	}
	wg.Wait()
	if s.Phase != "ranking" || len(s.Ranking) != 21 {
		t.Fatal("class did not finish")
	}
	for _, r := range s.Ranking {
		if r.Flowers != 20 || r.Rank != 1 {
			t.Fatalf("lost or duplicated votes: %+v", r)
		}
	}
}

func TestSleepingBrowserCatchesUpThroughBothQuestions(t *testing.T) {
	s, now, ids := fixture(t, 1)
	share(t, s, ids)
	*now = s.Deadline
	s.tick()
	rankingEnd := s.Deadline
	*now = rankingEnd + 2*s.Config.QuestionMS
	s.tick()
	if s.Phase != "ending" || s.StartedAt != rankingEnd+8000 {
		t.Fatal("closing deadlines drifted after a sleeping browser")
	}
}

func TestUnsubmittedParticipantReviewsEveryAuthor(t *testing.T) {
	s, now, ids := fixture(t, 2)
	if err := s.submit(ids[0], "A single reflection", false); err != nil {
		t.Fatal(err)
	}
	*now = s.Deadline
	s.tick()
	if !s.snapshot(ids[0]).Finished || s.snapshot(ids[0]).Card != nil {
		t.Fatal("author saw their own work")
	}
	v := s.snapshot(ids[1])
	if v.ReviewTotal != 1 || v.Card == nil {
		t.Fatal("non-author must see the available reflection")
	}
	if err := s.advance(ids[1], v.Card.ID); err == nil {
		t.Fatal("an unanswered card was skipped")
	}
	if err := s.vote(ids[1], v.Card.ID, "flower"); err != nil {
		t.Fatal(err)
	}
	if err := s.advance(ids[1], v.Card.ID); err != nil {
		t.Fatal(err)
	}
	if s.Phase != "ranking" || s.Ranking[0].Flowers != 1 {
		t.Fatal("class did not finish after its final choice")
	}
}
