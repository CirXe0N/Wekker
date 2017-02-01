export interface TVShow {
  tv_show_id: string;
  name: string;
  overview: string;
  status: string;
  first_air_date: string;
  poster: string;
  backdrop: string;
  origin_country: string;
  episode_run_time: string;
  genres: Genre[];
  language: string;
  type: string;
  is_collection_item: boolean;
  seasons: Season[];
  cast: CastMember[];
  crew: CrewMember[];
}

export interface Season {
  season_number: number;
  episode_number: number;
  episodes: Episode[];
  is_watched: boolean;
}

export interface Episode {
  episode_id: string;
  name: string;
  episode_number: number;
  is_watched: boolean;
  air_date: string;
  overview: string;
  isRequestingWatched: boolean;
}

export interface CastMember {
  name: string;
  character: string;
}

export interface CrewMember {
  name: string;
  job_title: string;
}

interface Genre {
  name: string;
}

export interface Recommendation {
  recipient: string;
  media_type: string;
  tv_movie_id: string;
}
