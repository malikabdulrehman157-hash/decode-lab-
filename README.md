# Project 3 – AI Recommendation Logic

**DecodeLabs Artificial Intelligence Industrial Training – Batch 2026**
Intern: Malik Abdul Rehman Nasir

## Goal
Create a simple recommendation system based on user preferences.

## Features
- **User input:** pick interests (genres and moods) from a numbered menu and rate each one from 1 to 5.
- **Similarity matching:** the user's ratings form a weighted preference vector; each movie is a vector of its attributes. Movies are ranked by **cosine similarity**.
- **Recommendations:** top matches are shown with a match %, a score bar and the reasons they matched.
- **More like this:** finds movies similar to one you already like using **Jaccard similarity**.
- Doesn't repeat recommendations within a session; all input is validated.

## How it works
| Step | Logic |
|------|-------|
| Item profiles | Each of 30 movies has a set of attributes, e.g. `{sci-fi, space, visual}` |
| User profile | `{attribute: rating}` built from the user's choices |
| Scoring | `cosine = Σ(rating of matched attributes) / (‖user‖ × √(number of movie attributes))` |
| Ranking | Sort by score, show top N |

Cosine similarity measures how well a movie points in the same direction as the user's tastes, so a movie doesn't win just by having more attributes.

## How to run
Requires Python 3 only – no external libraries.

```bash
python recommender.py
```

## Sample output
```
Top picks for Malik
============================================================
1. Gravity
   Match:  63.6%  [#############       ]
   Because: sci-fi, space
2. The Martian
   Match:  63.6%  [#############       ]
   Because: sci-fi, space
3. Dune
   Match:  56.9%  [###########         ]
   Because: sci-fi, space
============================================================
```

## Skills demonstrated
Logic building, pattern matching, recommendation concepts (content-based filtering, cosine and Jaccard similarity).
