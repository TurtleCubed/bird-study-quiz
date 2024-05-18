import requests
from random import choices, sample, randint
import datetime



def quiz_data(bird_list: list, quizLength: int, month: int):
    data = choices(bird_list, k=quizLength)
    counts = {}
    for d in data:
        if d['bird_id'] in counts:
              counts[d['bird_id']] = counts[d['bird_id']] + 1
        else:
              counts[d['bird_id']] = 1
    ids = {}
    for bird_id in counts:
        k = counts[bird_id]
        asset_ids = get_asset_ids(birdid=bird_id, month=month)
        while len(asset_ids) < k:
            asset_ids = asset_ids + get_asset_ids(birdid=bird_id, month=month)
        ids[bird_id] = sample(asset_ids, k=k)
    out = [None] * quizLength
    for code in ids:
        for asset_id in ids[code]:
             for i in range(len(data)):
                  if out[i] is None and data[i]['bird_id'] == code:
                       out[i] = {
                            'species': data[i]['species'],
                            'mlTag': asset_id,
                       }
                       break
    return out


def get_asset_ids(birdid, month):
    # randomize year
    year = datetime.date.today().year - randint(1, 10)
    # month as a range of months
    if month == 1:
        start_month = 12
    else:
        start_month = month - 1
    if month == 12:
        end_month = 1
    else: 
        end_month = month + 1
    # perform url search
    url = ''.join([f'https://media.ebird.org/api/v2/search?'
            f'taxonCode={birdid}&',
            f'sort=id_desc&',
            f'beginYear={year}&',
            f'endYear={year}&',
            f'mediaType=photo&',
            f'birdOnly=true&',
            f'beginMonth={start_month}&',
            f'endMonth={end_month}'])
    print(url)
    out = requests.get(url, cookies={
            'ml-search-session': 'eyJ1c2VyIjp7ImFub255bW91cyI6dHJ1ZX19', 
            'ml-search-session.sig': 'SjUzp_aBI4snTlng2qDJ7TZcb2w'
        })
    out = [x['assetId'] for x in out.json()]
    return out


def main():
    s = [
        {"species": "Common Loon", "bird_id": "comloo"},
        {"species": "Pacific Loon", "bird_id": "pacloo"},
        {"species": "Red-throated Loon", "bird_id": "retloo"},
        {"species": "Yellow-billed Loon", "bird_id": "yebloo"}
    ]
    quiz = quizData(s, 10, 3)
    for q in quiz:
         print(q)


if __name__ == "__main__":
    main()
    # asyncio.run(main())
