export interface User {
  first_name: string;
  last_name: string;
  email_address: string;
  old_password: string;
  password: string;
  access_token: string;
  photo: string;
  photo_name: string;
  is_verified: boolean;
}

export interface CollectionTVShow {
  tv_show_id: string;
  name: string;
  status: string;
  last_seen_episode: CollectionTVShowEpisode,
  last_released_episode: CollectionTVShowEpisode
}

interface CollectionTVShowEpisode {
  episode_number: number;
  season_number: number;
}

export interface CollectionMovie {
  movie_id: string;
  name: string;
  status: string;
}

export interface DashboardStatistics {
  collected_tv_shows: number;
  collected_movies: number;
  watched_tv_show_episodes: number;
  watched_movies: number;
}
