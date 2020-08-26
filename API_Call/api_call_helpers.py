import requests

# make API requests
def get_api_request(url,headers,request_name=''):
    '''
    This function makes the API request and returns the output in JSON format.
    '''
    r = requests.get(url,headers=headers)
    if r.status_code == 200:
#        print(f'{request_name} Request Successful')
        
        r_json = r.json()
        return r_json
    else: 
        print(r.status_code)
        
# get encrypted account ID from gamer tag
def get_encrypted_accid(username:str,headers):
    '''
    This function takes the gamer tag and returns the associated account ID. Need to pass headers for requests.
    '''
    SUMMONER_INFO_URL = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{username}"
    json = get_api_request(SUMMONER_INFO_URL,headers=headers)
    
    return json['accountId']
        
# get match lists
def get_match_list_by_accid(encrypted_acc_id:str,headers):
    '''
    This function takes the encrypted account ID and returns a list of matches. Need to pass headers for requests.
    '''
    beginIndex=0
    MATCHLIST_INFO_URL = f"https://euw1.api.riotgames.com/lol/match/v4/matchlists/by-account/{encrypted_acc_id}?beginIndex={beginIndex}"

    r_matchlists_json = get_api_request(MATCHLIST_INFO_URL,headers=headers)
    
    matches = r_matchlists_json['matches']

    beginIndex = r_matchlists_json['endIndex']
    totalGames = r_matchlists_json['totalGames']

    # keep fetching until all matches are fetched (riot api only returns 100 matches per call)
    while beginIndex < totalGames:

        MATCHLIST_INFO_URL = f"https://euw1.api.riotgames.com/lol/match/v4/matchlists/by-account/{encrypted_acc_id}?beginIndex={beginIndex}"

        r_matchlists_json = get_api_request(MATCHLIST_INFO_URL,headers=headers)
        matches += r_matchlists_json['matches']
        beginIndex = r_matchlists_json['endIndex']
        totalGames = r_matchlists_json['totalGames']

    print(f'Total {totalGames} Matches Retrieved')
    
    return matches

# get match stats for each match
def get_match_stats(username,match_id,headers):
    '''
    This function gets the match stats for each of the matches played by the specified user.
    '''
    #url from riot API
    MATCH_STATS_URL = f'https://euw1.api.riotgames.com/lol/match/v4/matches/{match_id}'
    match_stats = get_api_request(MATCH_STATS_URL,headers)
    
    #check all the participants in the match for the stats of the specified user
    for participant in match_stats['participantIdentities']:
        if participant['player']['summonerName'] == username:
            pid = participant['participantId'] -1
            stats = match_stats['participants'][pid]['stats']
            stats['matchID'] = str(match_id)
            stats['summonername'] = str(username)
            stats['gameCreationDate'] = match_stats['gameCreation']
            stats['gameDuration'] = match_stats['gameDuration']
            stats['gameType'] = match_stats['gameType']
            stats['gameMode'] = match_stats['gameMode']
    return stats