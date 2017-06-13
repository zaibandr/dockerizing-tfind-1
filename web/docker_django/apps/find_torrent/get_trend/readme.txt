kinipoisk.py

    main()
    Собирает популярные фильмы за день из кинопоиска

    в цикле пробегая по url
    ================================================
    https://www.kinopoisk.ru/popular/day/2016-12-07/
    https://www.kinopoisk.ru/popular/day/2016-12-06/
    и так далее
    ================================================

    pars_trend()
    Парсит тренды (название фильма/сериала) по строчкам и складывет в файл trend.txt


rutor_query.py

    get_search_result(q)
        на входе:
        q - строка запроса

        запрос на url вида:
            http://rutor.info/search/0/0/100/0/{название фильма/сериала}

        на выходе:
        html = resp.text

    rutor_to_torrent(html)
        парсит по строчкам ("tr")

            =====================================================
            d['title'] = a_list[2].text
            d['magnet'] = a_list[1].get('href')
            d['provider'] = provider_name
            d['provider_url'] = provider + a_list[2].get('href')
            =====================================================

        и кладет в БД

