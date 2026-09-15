"""
Letterboxd "People You May Know" — Friend Suggestion Prototype
----------------------------------------------------------------
PROBLEM: Letterboxd's only friend-discovery tools are (1) searching an
exact username, or (2) a Facebook-sync feature users report as broken.
There is no "people you may know" style suggestion, unlike most social
platforms (Instagram, Spotify, Goodreads).

THIS SCRIPT: Simulates how a "people you may know" feature could work,
using mock user data (fake usernames + the films they've rated highly).
It calculates taste similarity between users using Jaccard similarity
(a standard technique for comparing sets of shared items) and returns
ranked friend suggestions for a given user.

This is a prototype/demo using invented data — not connected to
Letterboxd's real API or real user data.
"""

from itertools import combinations

# ----------------------------------------------------------------
# MOCK DATA: pretend users and the films each rated 4+ stars (out of 5)
# In a real version, this would come from a database query instead.
# ----------------------------------------------------------------
user_top_films = {
    "cinephile_casey":   {"Parasite", "Whiplash", "Moonlight", "The Lighthouse", "Portrait of a Lady on Fire"},
    "filmbro_jordan":    {"Whiplash", "The Dark Knight", "Fight Club", "Parasite", "Inception"},
    "arthouse_avery":    {"Moonlight", "Portrait of a Lady on Fire", "The Lighthouse", "Aftersun", "Past Lives"},
    "popcorn_pat":       {"The Dark Knight", "Inception", "Top Gun: Maverick", "Fight Club"},
    "indie_iris":        {"Aftersun", "Past Lives", "The Lighthouse", "Moonlight", "Minari"},
    "new_user_lily":     {"Parasite", "Moonlight", "Portrait of a Lady on Fire", "Minari"},
}


def jaccard_similarity(set_a: set, set_b: set) -> float:
    """
    Jaccard similarity = (shared items) / (total unique items across both).
    Returns a score from 0 (no overlap) to 1 (identical taste).
    This is the same core concept used by real recommendation systems
    to measure how similar two users' preferences are.
    """
    if not set_a or not set_b:
        return 0.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union


def suggest_friends(target_user: str, data: dict, top_n: int = 3):
    """
    For a given user, rank every other user by taste similarity
    and return the top_n most similar people, along with the
    specific films they have in common (this becomes the
    "You both loved Parasite and Moonlight" suggestion text).
    """
    target_films = data[target_user]
    scores = []

    for other_user, films in data.items():
        if other_user == target_user:
            continue
        score = jaccard_similarity(target_films, films)
        shared_films = target_films & films
        scores.append((other_user, score, shared_films))

    # Sort by similarity score, highest first
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_n]


def print_suggestions(target_user: str, data: dict, top_n: int = 3):
    print(f"\n'People You May Know' suggestions for: {target_user}")
    print(f"(based on {len(data[target_user])} films they've rated highly)\n")

    results = suggest_friends(target_user, data, top_n)
    for rank, (user, score, shared) in enumerate(results, start=1):
        pct = round(score * 100)
        shared_list = ", ".join(sorted(shared)) if shared else "no direct overlap yet"
        print(f"{rank}. {user}  —  {pct}% taste match")
        print(f"   You both liked: {shared_list}\n")


if __name__ == "__main__":
    # Demo: show suggestions for a brand-new user, "new_user_lily"
    print_suggestions("new_user_lily", user_top_films, top_n=3)

    print("-" * 55)

    # Demo: show suggestions for an existing user too
    print_suggestions("filmbro_jordan", user_top_films, top_n=3)
