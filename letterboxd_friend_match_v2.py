"""
Letterboxd "People You May Know" — Friend Suggestion Prototype (v2)
----------------------------------------------------------------
PROBLEM: Letterboxd's only friend-discovery tools are (1) searching an
exact username, or (2) a Facebook-sync feature users report as broken.
There is no "people you may know" style suggestion, unlike most social
platforms (Instagram, Spotify, Goodreads).

THIS SCRIPT: Simulates a multi-signal "people you may know" feature,
combining THREE real-world signals instead of just one:

  1. TASTE SIMILARITY   — do they rate similar films highly?
  2. LOCATION            — are they in the same city? (real-world friends
                            are often geographically close, e.g. film
                            club members, college friends, coworkers)
  3. MUTUAL CONNECTIONS  — do they already follow people in common?
                            (the strongest real-world signal — if 3 of
                            your friends already follow someone, you
                            probably know them too)

Each signal is scored separately, then combined into one weighted
"match score" — similar to how real recommendation systems blend
multiple signals rather than relying on just one.

This is a prototype/demo using invented data — not connected to
Letterboxd's real API or real user data.
"""

# ----------------------------------------------------------------
# MOCK DATA
# ----------------------------------------------------------------

# Films each user rated 4+ stars
user_top_films = {
    "cinephile_casey":   {"Parasite", "Whiplash", "Moonlight", "The Lighthouse", "Portrait of a Lady on Fire"},
    "filmbro_jordan":    {"Whiplash", "The Dark Knight", "Fight Club", "Parasite", "Inception"},
    "arthouse_avery":    {"Moonlight", "Portrait of a Lady on Fire", "The Lighthouse", "Aftersun", "Past Lives"},
    "popcorn_pat":       {"The Dark Knight", "Inception", "Top Gun: Maverick", "Fight Club"},
    "indie_iris":        {"Aftersun", "Past Lives", "The Lighthouse", "Moonlight", "Minari"},
    "new_user_lily":     {"Parasite", "Moonlight", "Portrait of a Lady on Fire", "Minari"},
}

# Self-reported city (optional field a user could add to their profile)
user_location = {
    "cinephile_casey":  "Gainesville, FL",
    "filmbro_jordan":   "Orlando, FL",
    "arthouse_avery":   "Gainesville, FL",
    "popcorn_pat":      "Atlanta, GA",
    "indie_iris":       "Gainesville, FL",
    "new_user_lily":    "Gainesville, FL",
}

# Who each user already follows on the platform (existing social graph)
user_already_follows = {
    "cinephile_casey":  {"arthouse_avery", "indie_iris"},
    "filmbro_jordan":   {"popcorn_pat"},
    "arthouse_avery":   {"cinephile_casey", "indie_iris"},
    "popcorn_pat":      {"filmbro_jordan"},
    "indie_iris":       {"cinephile_casey", "arthouse_avery"},
    "new_user_lily":    {"cinephile_casey"},   # Lily already follows one person
}


# ----------------------------------------------------------------
# SIGNAL 1: Taste similarity (Jaccard similarity on shared films)
# ----------------------------------------------------------------
def taste_score(user_a: str, user_b: str) -> float:
    films_a = user_top_films.get(user_a, set())
    films_b = user_top_films.get(user_b, set())
    if not films_a or not films_b:
        return 0.0
    intersection = len(films_a & films_b)
    union = len(films_a | films_b)
    return intersection / union


# ----------------------------------------------------------------
# SIGNAL 2: Location match (same city = 1, different city = 0)
# A real version could use distance in miles instead of exact match.
# ----------------------------------------------------------------
def location_score(user_a: str, user_b: str) -> float:
    loc_a = user_location.get(user_a)
    loc_b = user_location.get(user_b)
    if loc_a and loc_b and loc_a == loc_b:
        return 1.0
    return 0.0


# ----------------------------------------------------------------
# SIGNAL 3: Mutual connections (how many people they both already follow)
# Normalized against the smaller of the two users' follow-lists.
# ----------------------------------------------------------------
def mutual_connections(user_a: str, user_b: str) -> set:
    follows_a = user_already_follows.get(user_a, set())
    follows_b = user_already_follows.get(user_b, set())
    return follows_a & follows_b


def mutual_score(user_a: str, user_b: str) -> float:
    shared = mutual_connections(user_a, user_b)
    follows_a = user_already_follows.get(user_a, set())
    follows_b = user_already_follows.get(user_b, set())
    smaller_list = min(len(follows_a), len(follows_b)) or 1  # avoid divide-by-zero
    return len(shared) / smaller_list


# ----------------------------------------------------------------
# COMBINED SCORE
# Weights reflect that mutual connections are usually the strongest
# real-world signal, taste similarity is a solid secondary signal,
# and location is a nice-to-have booster rather than a dealbreaker.
# ----------------------------------------------------------------
WEIGHTS = {
    "taste": 0.4,
    "location": 0.2,
    "mutual": 0.4,
}


def combined_score(user_a: str, user_b: str) -> dict:
    t = taste_score(user_a, user_b)
    l = location_score(user_a, user_b)
    m = mutual_score(user_a, user_b)
    total = (t * WEIGHTS["taste"]) + (l * WEIGHTS["location"]) + (m * WEIGHTS["mutual"])
    return {"taste": t, "location": l, "mutual": m, "total": total}


def suggest_friends(target_user: str, top_n: int = 3):
    already_following = user_already_follows.get(target_user, set())
    scores = []

    for other_user in user_top_films:
        if other_user == target_user or other_user in already_following:
            continue  # skip yourself and people you already follow
        breakdown = combined_score(target_user, other_user)
        scores.append((other_user, breakdown))

    scores.sort(key=lambda x: x[1]["total"], reverse=True)
    return scores[:top_n]


def print_suggestions(target_user: str, top_n: int = 3):
    print(f"\n'People You May Know' suggestions for: {target_user}")
    print(f"(currently follows: {', '.join(sorted(user_already_follows.get(target_user, []))) or 'no one yet'})\n")

    results = suggest_friends(target_user, top_n)
    for rank, (user, b) in enumerate(results, start=1):
        shared_films = user_top_films[target_user] & user_top_films[user]
        shared_conns = mutual_connections(target_user, user)
        same_city = user_location.get(target_user) == user_location.get(user)

        print(f"{rank}. {user}  —  match score: {round(b['total'] * 100)}%")
        if shared_films:
            print(f"   Taste: you both liked {', '.join(sorted(shared_films))}")
        if same_city:
            print(f"   Location: both in {user_location.get(target_user)}")
        if shared_conns:
            print(f"   Mutual: you both follow {', '.join(sorted(shared_conns))}")
        print()


if __name__ == "__main__":
    print_suggestions("new_user_lily", top_n=3)
    print("-" * 55)
    print_suggestions("filmbro_jordan", top_n=3)
