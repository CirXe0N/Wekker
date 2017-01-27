export interface tvShow {
  title: string;
  poster_url: string;
  status: string;
  last_seen_episode: string;
  last_released_episode: string;
  is_up_to_date: boolean;
  amount_comments: number;
  has_new_episode: boolean;
  type: string;
}

export interface movie {
  title: string;
  poster_url: string;
  status: string;
  release_date: string;
  amount_comments: number;
  is_watched: boolean;
  type: string;
}
