import requests
import time
import re
import csv

encoding = 'utf-8'
headers = {'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) ' 'AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/50.0.2661.102 Safari/537.36')}



def dump_data(filename: str = 'dump.txt', total_number_of_anime: int = 50):
    """
    Zapiše HTML podatke, pridobljene z `requests`, v datoteko `filename`.
    Arguments:
        filename (str): Pot do datoteke, kamor se shrani vsebina strani.
        total_number_of_anime (int): Število animejev, ki jih želimo pridobiti (v korakih po 50).
    """
    if not isinstance(filename, str) or not isinstance(total_number_of_anime, int): # isinstnce se uporablja za preveranje tipa stvari.
        raise TypeError('filename mora biti str, total_number_of_anime mora biti int')

    url = 'https://myanimelist.net/topanime.php?'

    anime_per_request = 50
    pages = (total_number_of_anime + anime_per_request - 1) // anime_per_request # Zaokroževanje navzgor.

    with open(file=filename, mode='w', encoding=encoding) as dump:
        for page in range(pages):
            zacetek = page * anime_per_request
            new_url = f'{url}limit={zacetek}'
            print(f'Prenašam: {new_url}')

            try:
                response = requests.get(new_url, headers=headers, timeout=10) # Request je knjižnica za dostopanje spletnih strani. Pridobimo podatke ki so na spletnem mestu `new_url` v obliki HTML. Uporabimo header, zato, da povemu spletnemu mestu preko katere naprave dostopamo. Timout se uporabi v primeru, da pride no napake in nočemo da se program ustavi. Funkcija počaka 10 sekund in če ne dobi odgovora ali pride do errorja gre naprej. 
                response.raise_for_status() # Preveri ali je prišlo do napake. Se izvede except spodaj.
                site_content = response.text
                dump.write(site_content + '\n\n')
            except requests.RequestException as e:
                print(f'Napaka pri dostopu do {new_url}: {e}')
                continue

            time.sleep(5) # Če dostopamo do spletne strani prevečkrat v zelo kratkem času, bo spletna stran mislila, da jo hočemo podreti.
    print(f"Sem prensel v datoteko: {filename}")


def search_group(pattern, text):
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None


def make_csv_from_dump(input_file: str = 'dump.txt', output_csv_file: str = 'anime_data.csv'):
    """
    CSV je format datoteke. Naredi tabelco iz podatkov. Na vrhu je tip podatka, ostalo so podatki.
    Prebere in prefiltira (parsira) dump datoteko in shrani podatke o animejih v CSV.
    """
    with open(file=input_file, mode='r', encoding=encoding) as dump:
        dump_contents = dump.read()
        vzorec_animeja = r'<tr class="ranking-list">.*?<\/tr>'
        animeji = re.findall(pattern=vzorec_animeja, string=dump_contents, flags=re.DOTALL) # Dobimo [anime0.html, anime1.html, anime2.html, ...]
        # V regex-u ima pika pomen katerikoli znak razen nove vrstice. re.DOTALL pomeni, da je pika katerikoli znak ali nova vrstica.

    with open(output_csv_file, mode='w', encoding=encoding, newline='') as csv_file:
        writer = csv.writer(csv_file) # Kličeva funkcijo iz csv knjižnice, zato da ustvariva pisatelja.
        writer.writerow(['Rank', 'Score', 'Name', 'ID', 'Link', 'Type', 'Episodes', 'Start Date', 'End Date'])

        for en_anime in animeji:
            rank = search_group(r'<span class=".*?top-anime-rank-text.*?">(\d+)</span>', en_anime)
            name = search_group(r'<a href="https://myanimelist\.net/anime/\d+/[^"]+"[^>]*class="hoverinfo_trigger">(.*?)</a>', en_anime)
            id_ = search_group(r'<div class="detail"><div id="area(\d+)">', en_anime)
            link = search_group(r'<a href="(https://myanimelist.net/anime/[^\"]+)"', en_anime)
            score = search_group(r'<span class=".*?score-label.*?">(\d+\.\d+)</span>', en_anime)
            type_ = search_group(r'([A-Za-z]+) *\(\d+ eps\)<br>', en_anime)
            episodes = search_group(r'[A-Za-z]+ *\((\d+) eps\)<br>', en_anime)
            start_date = search_group(r'([A-Za-z]{3} \d{4}) - (?:[A-Za-z]{3} \d{4}|\?)?<br>', en_anime)
            end_date   = search_group(r'[A-Za-z]{3} \d{4} - (?:([A-Za-z]{3} \d{4})|\?)<br>', en_anime)

            if not score:
                print(f'Preskočim anime brez ocene: {link}')
                continue

            writer.writerow([rank, score, name, id_, link, type_, episodes, start_date, end_date])

    print(f'CSV datoteka ustvarjena: {output_csv_file}')


def get_more_data(csv_file_name: str = 'anime_data.csv', output_file: str = 'anime_data_premium.csv'):
    """
    For each Link in the CSV, fetch the page, extract Status, and append the HTML to dump_file.
    Prints the extracted Status (or 'N/A' if missing).
    """

    with open(output_file, mode='w', encoding=encoding, newline='') as csv_out:
        writer = csv.writer(csv_out)
        writer.writerow(['Rank', 'Score', 'Name', 'ID', 'Link', 'Type', 'Episodes', 'Start Date', 'End Date', 'Status', 'Premiered', 'Broadcast', 'Producers', 'Licensors', 'Studios', 'Source', 'Genres', 'Demographics', 'Duration', 'Rating', 'Popularity', 'Members', 'Favorites', 'Aired start', 'Aired end'])
    csv_out.close()

    csv_updates = []
    with open(csv_file_name, mode='r', encoding=encoding) as csv_file:

        reader = csv.reader(csv_file)

        for i, row in enumerate(reader):
            link = row[4]
            if not link or i == 0:
                print(f'[{i}] No Link in row, skipping.')
                continue

            try:
                response = requests.get(link, headers=headers, timeout=10)
                response.raise_for_status()
                content = response.text

                # TODO: Fix this it no work. The regex a problem
                # Status
                status_pattern = r'<span[^>]*>\s*Status:\s*</span>\s*([^<]+)'
                status = re.search(status_pattern, content)
                status = status.group(1).strip() if status else 'N/A'
                row.append(status)

                # Premiered
                premiered_pattern = r'<span[^>]*>\s*Premiered:\s*</span>\s*<a[^>]*>([^<]+)</a>'
                premiered = re.search(premiered_pattern, content)
                premiered = premiered.group(1).strip() if premiered else 'N/A'
                row.append(premiered)

                # Broadcast
                broadcast_pattern = r'<span[^>]*>\s*Broadcast:\s*</span>\s*([^<]+)'
                broadcast = re.search(broadcast_pattern, content)
                broadcast = broadcast.group(1).strip() if broadcast else 'N/A'
                row.append(broadcast)

                # Producers
                producers_pattern = r'<span[^>]*>\s*Producers:\s*</span>\s*([^<]+)'
                producers = re.search(producers_pattern, content)
                producers = producers.group(1).strip() if producers else 'N/A'
                row.append(producers)

                # Licensors
                licensors_pattern = r'<span[^>]*>\s*Licensors:\s*</span>\s*([^<]+)'
                licensors = re.search(licensors_pattern, content)
                licensors = licensors.group(1).strip() if licensors else 'N/A'
                row.append(licensors)

                # Studios
                studios_pattern = r'<span[^>]*>\s*Studios:\s*</span>\s*([^<]+)'
                studios = re.search(studios_pattern, content)
                studios = studios.group(1).strip() if studios else 'N/A'
                row.append(studios)

                # Source
                source_pattern = r'<span[^>]*>\s*Source:\s*</span>\s*([^<]+)'
                source = re.search(source_pattern, content)
                source = source.group(1).strip() if source else 'N/A'
                row.append(source)

                # Genres
                # genres_pattern = r'<span[^>]*>\s*Genres:\s*</span>\s*([^<]+)'
                # genres = re.search(genres_pattern, content)
                # genres = genres.group(1).strip() if genres else 'N/A'
                # row.append(genres)

                # Vse žanre
                block = re.search(r'<span[^>]*>\s*Genres:\s*</span>(.*?)</div>', content, re.S)
                if block:
                    # Vse žanre v list
                    genres = re.findall(r'<a [^>]*>(.*?)</a>', block.group(1))
                    if genres:
                        row.append(genres)
                    else:
                        row.append("N/A")

                # Demographics
                demographics_pattern = r'<span[^>]*>\s*Demographics:\s*</span>\s*([^<]+)'
                demographics = re.search(demographics_pattern, content)
                demographics = demographics.group(1).strip() if demographics else 'N/A'
                row.append(demographics)

                # Duration
                duration_pattern = r'<span[^>]*>\s*Duration:\s*</span>\s*([^<]+)'
                duration = re.search(duration_pattern, content)
                duration = duration.group(1).strip() if duration else 'N/A'
                row.append(duration)

                # Rating
                rating_pattern = r'<span[^>]*>\s*Rating:\s*</span>\s*([^<]+)'
                rating = re.search(rating_pattern, content)
                rating = rating.group(1).strip() if rating else 'N/A'
                row.append(rating)

                # Popularity
                popularity_pattern = r'<span[^>]*>\s*Popularity:\s*</span>\s*([^<]+)'
                popularity = re.search(popularity_pattern, content)
                popularity = popularity.group(1).strip() if popularity else 'N/A'
                row.append(popularity)

                # Members
                members_pattern = r'<span[^>]*>\s*Members:\s*</span>\s*([^<]+)'
                members = re.search(members_pattern, content)
                members = members.group(1).strip() if members else 'N/A'
                row.append(members)

                # Favorites
                favorites_pattern = r'<span[^>]*>\s*Favorites:\s*</span>\s*([^<]+)'
                favorites = re.search(favorites_pattern, content)
                favorites = favorites.group(1).strip() if favorites else 'N/A'
                row.append(favorites)

                # Aired
                # TODO: For consistency change the else to None
                aired_pattern = r'<span[^>]*>\s*Aired:\s*</span>\s*([A-Za-z]{3} \d{1,2}, \d{4})\s+to\s+([A-Za-z]{3} \d{1,2}, \d{4})'
                aired = re.search(aired_pattern, content)
                aired_start = aired.group(1).strip() if aired else 'N/A'
                aired_end = aired.group(2).strip() if aired else 'N/A'
                row.append(aired_start)
                row.append(aired_end)


            except requests.RequestException as e:
                print(f'[{i}] Request failed for {link}: {e}')
                continue

            csv_updates.append(row)
            print('Somethign is going on:', i)

            if i % 10 == 0:
                with open(output_file, mode='w', encoding=encoding, newline='') as csv_out:
                    writer = csv.writer(csv_out)
                    for row in csv_updates:
                        writer.writerow(row)
                csv_out.close()
                print("Wrote to file")

            time.sleep(5)

    print(f'Updated CSV written to {output_file}')


# Poženemo funkcije

# dump_data(total_number_of_anime=6000)
# make_csv_from_dump()
# get_more_data()
