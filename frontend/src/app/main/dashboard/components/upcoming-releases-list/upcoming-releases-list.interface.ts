export interface UpcomingReleaseDate {
  date: string;
  releases: UpcomingRelease[];
}

export interface UpcomingRelease {
  poster_url: string;
  title: string;
  season: string;
  episode: string;
  type: string;
}
