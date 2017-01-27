export interface TVShow {
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
  seasons: Season[];
  cast: CastMember[];
  crew: CrewMember[];
}

interface Genre {
  name: string;
}

export interface Season {
  season_number: number;
  episode_number: number;
  episodes: Episode[];
  is_watched: boolean;
}

interface Episode {
  name: string;
  episode_number: number;
  is_watched: boolean;
}

export interface CastMember {
  name: string;
  character: string;
}

export interface CrewMember {
  name: string;
  job_title: string;
}
