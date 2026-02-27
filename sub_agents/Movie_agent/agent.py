from google.adk.agents import Agent
import requests

OMDB_API_KEY = "d31dbbca"  # your real key
OMDB_BASE_URL = "http://www.omdbapi.com/"

def get_movie_recommendation(movie_name: str) -> dict:
    print(f"--- Tool: get_movie_recommendation called for movie: {movie_name} ---")
    movie_normalized = movie_name.strip()

    # Step 1: Get the main movie details
    params = {"t": movie_normalized, "apikey": OMDB_API_KEY}
    try:
        response = requests.get(OMDB_BASE_URL, params=params)
        data = response.json()
        print("DEBUG main movie:", data)

        if data.get("Response") != "True":
            return {"status": "error", "error_message": data.get("Error", "Movie not found.")}

        title = data.get("Title")
        year = data.get("Year")
        genre = data.get("Genre")
        plot = data.get("Plot")
        imdb_rating = data.get("imdbRating")

        main_genre = genre.split(",")[0].strip()

        # Step 2: Search for similar movies by genre keyword
        search_params = {"s": main_genre, "apikey": OMDB_API_KEY}
        search_response = requests.get(OMDB_BASE_URL, params=search_params)
        search_data = search_response.json()
        print("DEBUG recommendations:", search_data)

        recommendations = []
        if search_data.get("Response") == "True":
            for movie in search_data.get("Search", []):
                if movie.get("Title") != title:  # avoid repeating same movie
                    recommendations.append(movie.get("Title"))
                if len(recommendations) >= 5:  # limit to 5 recommendations
                    break

        rec_message = (
            f"If you enjoyed {title}, here are some other {main_genre} movies you might like: "
            + ", ".join(recommendations) if recommendations else "No similar movies found."
        )

        return {
            "status": "success",
            "report": f"🎬 {title} ({year})\n⭐ IMDb Rating: {imdb_rating}\n🎭 Genre: {genre}\n📖 Plot: {plot}\n\nRecommendation: {rec_message}"
        }

    except Exception as e:
        return {"status": "error", "error_message": str(e)}

Movie_agent = Agent(
    name="Movie_agent",
    model="gemini-2.0-flash",
    description="Movie recommendation agent",
    instruction="You are a movie recommendation assistant. When the user asks about a movie, fetch details using the tool and provide recommendations.",
    tools=[get_movie_recommendation],
)
