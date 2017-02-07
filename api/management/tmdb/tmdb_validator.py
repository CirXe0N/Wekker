def validate_tv_show_data(tv_show):
    if not tv_show:
        return False, 'DOES NOT EXIST'

    if tv_show.get('original_language', 'en') != 'en':
        return False, 'LANGUAGE NOT ENGLISH'

    if 'US' not in tv_show.get('origin_country', []):
        return False, 'COUNTRY NOT US'

    if tv_show.get('number_of_episodes', 0) == 0 or tv_show.get('number_of_seasons', 0) == 0:
        return False, 'NO EPISODES OR SEASONS'

    if not tv_show.get('overview'):
        return False, 'NO OVERVIEW'

    return True, ''


def validate_movie_data(movie):
    if not movie:
        return False, 'DOES NOT EXIST'

    if movie.get('original_language', 'en') != 'en':
        return False, 'LANGUAGE NOT ENGLISH'

    if movie.get('adult'):
        return False, 'ADULT MOVIE'

    if not movie.get('overview'):
        return False, 'NO OVERVIEW'

    return True, ''
