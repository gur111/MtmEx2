def printCompetitor(competitor):
    '''
    Given the data of a competitor, the function prints it in a specific format.
    Arguments:
        competitor: {'competition name': competition_name, 'competition type': competition_type,
                        'competitor id': competitor_id, 'competitor country': competitor_country,
                        'result': result}
    '''
    competition_name = competitor['competition name']
    competition_type = competitor['competition type']
    competitor_id = competitor['competitor id']
    competitor_country = competitor['competitor country']
    result = competitor['result']

    print(f'Competitor {competitor_id} from {competitor_country} participated in {competition_name} ({competition_type}) and scored {result}')


def printCompetitionResults(competition_name, winning_gold_country, winning_silver_country, winning_bronze_country):
    '''
    Given a competition name and its champs countries, the function prints the winning countries
        in that competition in a specific format.
    Arguments:
        competition_name: the competition name
        winning_gold_country, winning_silver_country, winning_bronze_country: the champs countries
    '''
    undef_country = 'undef_country'
    countries = [country for country in [winning_gold_country,
                                         winning_silver_country, winning_bronze_country] if country != undef_country]
    print(
        f'The winning competitors in {competition_name} are from: {countries}')


def key_sort_competitor(competitor):
    '''
    A helper function that creates a special key for sorting competitors.
    Arguments:
        competitor: a dictionary contains the data of a competitor in the following format:
                    {'competition name': competition_name, 'competition type': competition_type,
                        'competitor id': competitor_id, 'competitor country': competitor_country,
                        'result': result}
    '''
    competition_name = competitor['competition name']
    result = competitor['result']
    return (competition_name, result)


def readParseData(file_name):
    '''
    Given a file name, the function returns a list of competitors.
    Arguments:
        file_name: the input file name. Assume that the input file is in the directory of this script.
    Return value:
        A list of competitors, such that every record is a dictionary, in the following format:
            {'competition name': competition_name, 'competition type': competition_type,
                'competitor id': competitor_id, 'competitor country': competitor_country,
                'result': result}
    '''
    competitors_in_competitions = []
    # Part A, Task 3.4
    contries_by_competitor_ids = {}

    with open(file_name, 'r') as input_file:
        for line in input_file:
            if line[0] == '#':
                continue

            entry_parts = line.strip().split(' ')
            if entry_parts[0] == 'competitor':
                contries_by_competitor_ids[int(
                    entry_parts[1])] = entry_parts[2]
            else:
                assert entry_parts[
                    0] == 'competition', f'Invalid line in input file:\n{line}'
                competitors_in_competitions.append({'competition name': entry_parts[1],
                                                    'competitor id': int(entry_parts[2]),
                                                    'competition type': entry_parts[3],
                                                    'result': int(entry_parts[4]),
                                                    'competitor country': None
                                                    })

    for entry in competitors_in_competitions:
        country = contries_by_competitor_ids.get(entry['competitor id'])
        assert country, f'Missing information for competitor: {entry["competitor id"]}'
        entry['competitor country'] = country

    return competitors_in_competitions


def getValidEntriesByCompetition(competitors_in_competitions):
    '''
    Converts the entries to a more convinient structure
    {
        'competition name': {
            'type': TYPE
            'entries': [
                entry0,
                entry1,
                entry2,
                ...
            ]
        }
    }
    '''
    entries_by_competition = {x['competition name']: {'type': x['competition type'], 'entries': []}
                              for x in competitors_in_competitions}
    # Init empty lists for each competition
    # banned_by_competition = {x['competition name']: []
    #                          for x in entries_by_competition}

    for entry in competitors_in_competitions:
        # Create a new competition key if doesn't exist
        competition = entries_by_competition[entry['competition name']]

        competitor_entries = [x for x in competitors_in_competitions
                              if x['competitor id'] == entry['competitor id'] and
                              x['competition name'] == entry['competition name']]

        if len(competitor_entries) == 1:
            competition['entries'].append({'competitor id': entry['competitor id'],
                                           'competitor country': entry['competitor country'],
                                           'result': entry['result']
                                           })

    entries_by_competition = {x: entries_by_competition[x] for x in entries_by_competition
                              if entries_by_competition[x]['entries']}

    return entries_by_competition


def calcCompetitionsResults(competitors_in_competitions):
    '''
    Given the data of the competitors, the function returns the champs countries for each competition.
    Arguments:
        competitors_in_competitions: A list that contains the data of the competitors
                                    (see readParseData return value for more info)
    Retuen value:
        A list of competitions and their champs (list of lists).
        Every record in the list contains the competition name and the champs, in the following format:
        [competition_name, winning_gold_country,
            winning_silver_country, winning_bronze_country]
    '''
    competitions_champs = []
    competitions = getValidEntriesByCompetition(competitors_in_competitions)
    # competitors = set([x['competitor id']
    #                    for x in competitors_in_competitions])

    for competition in competitions:
        competition_info = competitions[competition]
        if competition_info['type'] in ['knockout', 'timed']:
            reverse_results = False
        else:
            assert competition_info[
                'type'] == 'untimed', f'Unknown competition type: {competition_info["type"]}'
            reverse_results = True

        sorted_entries = sorted(competition_info['entries'], key=lambda x: x['result'],
                                reverse=reverse_results)

        winning_countries = [x['competitor country'] for x in sorted_entries]

        competitions_champs.append(
            [competition]+(winning_countries+['undef_country']*2)[0:3])

    # TODO Part A, Task 3.5

    return competitions_champs


def partA(file_name='input.txt', allow_prints=True):
    # read and parse the input file
    competitors_in_competitions = readParseData(file_name)
    if allow_prints:
        for competitor in sorted(competitors_in_competitions, key=key_sort_competitor):
            printCompetitor(competitor)

    # calculate competition results
    competitions_results = calcCompetitionsResults(competitors_in_competitions)
    if allow_prints:
        for competition_result_single in sorted(competitions_results):
            printCompetitionResults(*competition_result_single)

    return competitions_results


def partB(file_name='input.txt'):
    competitions_results = partA(file_name, allow_prints=False)
    import Olympics
    olympics = Olympics.OlympicsCreate()

    for champ in competitions_results:
        Olympics.OlympicsUpdateCompetitionResults(
            olympics, str(champ[1]), str(champ[2]), str(champ[3]))

    Olympics.OlympicsWinningCountry(olympics)
    Olympics.OlympicsDestroy(olympics)


if __name__ == "__main__":
    '''
    The main part of the script.
    __main__ is the name of the scope in which top-level code executes.

    To run only a single part, comment the line below which correspondes to the part you don't want to run.
    '''
    file_name = 'input.txt'

    partA(file_name)
    partB(file_name)
