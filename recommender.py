"""
DecodeLabs AI Internship - Project 3: AI Recommendation Logic
A content-based movie recommender built with pure Python (no libraries).

How it works
------------
1. Every movie is described by a set of attributes (genres + mood/style tags).
2. The user picks interests and rates how much they like each one (1-5).
3. The user's ratings become a "preference vector"; each movie becomes an
   "item vector" over the same attributes.
4. Cosine similarity scores how well each movie aligns with the user.
5. The top matches are shown with a match % and the reasons they matched.

Extra feature: "More like this" finds movies similar to one you already like,
using Jaccard similarity between attribute sets.
"""

import math

# ---------------------------------------------------------------------------
# 1. Item catalogue: each movie -> set of attributes
# ---------------------------------------------------------------------------
MOVIES = {
    "Inception":                {"sci-fi", "thriller", "action", "mind-bending", "visual"},
    "Interstellar":             {"sci-fi", "drama", "space", "emotional", "visual"},
    "The Matrix":               {"sci-fi", "action", "mind-bending", "classic"},
    "The Dark Knight":          {"action", "crime", "thriller", "dark", "superhero"},
    "Avengers: Endgame":        {"action", "superhero", "adventure", "feel-good", "visual"},
    "Spider-Man: Into the Spider-Verse": {"animation", "superhero", "action", "feel-good", "family"},
    "Toy Story":                {"animation", "comedy", "family", "feel-good", "classic"},
    "Up":                       {"animation", "family", "adventure", "emotional"},
    "Spirited Away":            {"animation", "fantasy", "adventure", "visual", "classic"},
    "The Lord of the Rings":    {"fantasy", "adventure", "epic", "classic", "visual"},
    "Harry Potter":             {"fantasy", "adventure", "family", "feel-good"},
    "Gladiator":                {"action", "drama", "epic", "historical"},
    "Titanic":                  {"romance", "drama", "historical", "emotional", "epic"},
    "La La Land":               {"romance", "musical", "drama", "feel-good"},
    "The Notebook":             {"romance", "drama", "emotional"},
    "The Shawshank Redemption": {"drama", "crime", "emotional", "classic"},
    "The Godfather":            {"crime", "drama", "classic", "dark"},
    "Se7en":                    {"crime", "thriller", "dark", "mystery"},
    "Knives Out":               {"mystery", "comedy", "crime", "feel-good"},
    "Get Out":                  {"horror", "thriller", "mystery", "mind-bending"},
    "A Quiet Place":            {"horror", "thriller", "sci-fi", "dark"},
    "The Conjuring":            {"horror", "mystery", "dark"},
    "Superbad":                 {"comedy", "feel-good"},
    "The Grand Budapest Hotel": {"comedy", "adventure", "visual", "mystery"},
    "Mad Max: Fury Road":       {"action", "adventure", "sci-fi", "visual"},
    "Gravity":                  {"sci-fi", "space", "thriller", "visual"},
    "The Martian":              {"sci-fi", "space", "comedy", "feel-good"},
    "Dune":                     {"sci-fi", "epic", "adventure", "visual", "space"},
    "Oppenheimer":              {"drama", "historical", "epic", "mind-bending"},
    "Coco":                     {"animation", "family", "musical", "emotional"},
}

# The full vocabulary of attributes, sorted so menus are stable
ATTRIBUTES = sorted({attr for attrs in MOVIES.values() for attr in attrs})


# ---------------------------------------------------------------------------
# 2. Similarity logic
# ---------------------------------------------------------------------------
def cosine_similarity(user_prefs, item_attrs):
    """
    Cosine similarity between a weighted user vector and a binary item vector.

    user_prefs : dict  {attribute: rating 1-5}
    item_attrs : set   {attribute, ...}  (each present attribute = 1)
    """
    dot = sum(rating for attr, rating in user_prefs.items() if attr in item_attrs)
    user_norm = math.sqrt(sum(r * r for r in user_prefs.values()))
    item_norm = math.sqrt(len(item_attrs))
    if user_norm == 0 or item_norm == 0:
        return 0.0
    return dot / (user_norm * item_norm)


def jaccard_similarity(set_a, set_b):
    """Shared attributes / total distinct attributes."""
    union = set_a | set_b
    return len(set_a & set_b) / len(union) if union else 0.0


def recommend(user_prefs, top_n=5, exclude=()):
    """Score every movie against the user's preferences and return the best."""
    results = []
    for title, attrs in MOVIES.items():
        if title in exclude:
            continue
        score = cosine_similarity(user_prefs, attrs)
        if score > 0:
            matched = sorted(attrs & user_prefs.keys(),
                             key=lambda a: -user_prefs[a])
            results.append((title, score, matched))
    results.sort(key=lambda r: (-r[1], r[0]))   # best score first, then A-Z
    return results[:top_n]


def similar_to(title, top_n=5):
    """Find movies whose attributes overlap most with a given movie."""
    base = MOVIES[title]
    results = []
    for other, attrs in MOVIES.items():
        if other == title:
            continue
        score = jaccard_similarity(base, attrs)
        if score > 0:
            results.append((other, score, sorted(base & attrs)))
    results.sort(key=lambda r: (-r[1], r[0]))
    return results[:top_n]


# ---------------------------------------------------------------------------
# 3. Input helpers (with validation)
# ---------------------------------------------------------------------------
def ask_int(prompt, low, high):
    """Keep asking until the user types a whole number in [low, high]."""
    while True:
        raw = input(prompt).strip()
        if raw.isdigit() and low <= int(raw) <= high:
            return int(raw)
        print(f"  Please enter a number from {low} to {high}.")


def choose_interests():
    """Let the user pick attributes by number, e.g. '1, 4, 9'."""
    print("\nAvailable interests:")
    for i, attr in enumerate(ATTRIBUTES, start=1):
        end = "\n" if i % 4 == 0 else ""
        print(f"  {i:>2}. {attr:<14}", end=end)
    print()

    while True:
        raw = input("\nPick your interests (numbers separated by commas): ")
        parts = [p.strip() for p in raw.replace(" ", ",").split(",") if p.strip()]
        if parts and all(p.isdigit() and 1 <= int(p) <= len(ATTRIBUTES) for p in parts):
            # dict.fromkeys removes duplicates but keeps order
            return list(dict.fromkeys(ATTRIBUTES[int(p) - 1] for p in parts))
        print(f"  Invalid choice. Use numbers between 1 and {len(ATTRIBUTES)}, e.g. 2, 7, 15")


def rate_interests(interests):
    """Ask how much the user likes each chosen interest (1-5)."""
    print("\nRate each interest (1 = slightly, 5 = love it):")
    return {attr: ask_int(f"  {attr}: ", 1, 5) for attr in interests}


def choose_movie():
    """Pick a movie from the catalogue by number."""
    titles = sorted(MOVIES)
    print()
    for i, t in enumerate(titles, start=1):
        print(f"  {i:>2}. {t}")
    return titles[ask_int("\nWhich movie do you like? ", 1, len(titles)) - 1]


# ---------------------------------------------------------------------------
# 4. Output
# ---------------------------------------------------------------------------
def show_results(results, heading):
    print("\n" + "=" * 60)
    print(heading)
    print("=" * 60)
    if not results:
        print("No matches found - try picking different interests.")
        return
    for rank, (title, score, matched) in enumerate(results, start=1):
        bar = "#" * round(score * 20)
        print(f"{rank}. {title}")
        print(f"   Match: {score * 100:5.1f}%  [{bar:<20}]")
        print(f"   Because: {', '.join(matched)}")
    print("=" * 60)


# ---------------------------------------------------------------------------
# 5. Main program loop
# ---------------------------------------------------------------------------
def main():
    print("=" * 60)
    print("   DecodeLabs Movie Recommender - Pattern Alignment Engine")
    print("=" * 60)
    name = input("What's your name? ").strip() or "Friend"
    profile = {}       # the user's preference vector, kept between rounds
    seen = set()       # movies already recommended this session

    while True:
        print(f"\n--- Menu ({name}) ---")
        print("1. Build / update my preference profile")
        print("2. Get recommendations")
        print("3. More like a movie I already like")
        print("4. Show my profile")
        print("5. Exit")
        choice = ask_int("Choose an option: ", 1, 5)

        if choice == 1:
            interests = choose_interests()
            profile.update(rate_interests(interests))
            seen.clear()
            print("\nProfile updated!")

        elif choice == 2:
            if not profile:
                print("\nBuild your profile first (option 1).")
                continue
            how_many = ask_int("How many recommendations (1-10)? ", 1, 10)
            results = recommend(profile, top_n=how_many, exclude=seen)
            seen.update(title for title, _, _ in results)
            show_results(results, f"Top picks for {name}")

        elif choice == 3:
            title = choose_movie()
            show_results(similar_to(title), f"Because you liked {title}")

        elif choice == 4:
            if not profile:
                print("\nYour profile is empty.")
            else:
                print("\nYour preferences:")
                for attr, rating in sorted(profile.items(), key=lambda x: -x[1]):
                    print(f"  {attr:<14} {'*' * rating}")

        else:
            print(f"\nThanks for using the recommender, {name}. Goodbye!")
            break


if __name__ == "__main__":
    main()
