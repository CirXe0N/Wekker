export interface Movie {
  movie_id: string;
  name: string;
  overview: string;
  status: string;
  release_date: string;
  poster: string;
  runtime: string;
  original_language: string;
  genres: Genre[];
  type: string;
  is_collection_item: boolean;
  is_watched: boolean;
}

interface Genre {
  name: string;
}

export interface Recommendation {
  recipient: string;
  media_type: string;
  movie_id: string;
}
