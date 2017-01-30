export interface Movie {
  movie_id: string;
  name: string;
  overview: string;
  status: string;
  release_date: string;
  poster: string;
  language: string;
  genres: Genre[];
  type: string;
  is_collection_item: boolean;
  is_watched: boolean;
}

interface Genre {
  name: string;
}
