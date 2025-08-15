import requests
import time
import re
import csv


def main(filename: str = "dump.txt", total_number_of_anime: int = 50):
    """
    Zapiše HTML podatke, pridobljene z `requests`, v datoteko.
    Arguments:
        filename (str): Pot do datoteke, kamor se shrani vsebina strani.
        total_number_of_anime (int): Število animejev, ki jih želimo pridobiti (v korakih po 50).
    """

    # Preverjanje tipov argumentov
    if not isinstance(filename, str) or not isinstance(total_number_of_anime, int):
        raise TypeError("filename mora biti str, total_number_of_anime mora biti int")

    url = "https://myanimelist.net/topanime.php?"
    # TODO: Preveri ali more biti headers kaj drugega ali je to uredu. Ali je to odvisno od napreave na kateri sem.
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/50.0.2661.102 Safari/537.36"
        )
    }
    encoding = "utf-8"
    anime_per_request = 50  # Število animejev na eno stran

    with open(file=filename, mode="w", encoding=encoding) as dump:
        # TODO: Če število animejev ni deljivo z 50, dodaj še tiste ki so med n*50 in total_number_of_anime.
        # TODO: Prenehaj s scrapeanjem, takrat ko anime nima več ocene, ali pa server verne error.
        for index in range(0, total_number_of_anime+1-anime_per_request, anime_per_request):
            new_url = f"{url}limit={index}"
            print(f"Prenašam: {new_url}")

            try:
                response = requests.get(new_url, headers=headers, timeout=10) # Odgovor od serverja. Timeout, če ne dobi odgovora toliko časa vrne napako.
                # Za pomoč pri errorjih: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
                response.raise_for_status() # Preveri ali je error. Maš več različnih errorjev. Če je error se izvede koda pod exeptiononm.
                site_content = response.text # Pridobi html kodo spletne strani.
                dump.write(site_content + "\n\n") # Shranimo html kodo v datoteko.
            except requests.RequestException as e:
                print(f"Napaka pri dostopu do {new_url}: {e}")
                continue

            # Kratek premor, da nas spletna stran ne blokira. Če pošljemo preveč requestov na isto spletno stran v kratem ćasu, bo stran mislila da jo napadamo in nas lahko blokira.
            time.sleep(1)


    # TODO: Get the info of a single anime. Dump it into a file. Get the link from the dump.txt file. 
    with open(file=filename, mode="r", encoding=encoding) as dump:
        dump_contents = dump.read()
        vzorec_animeja = r'<tr class="ranking-list">.*?<\/tr>'
        animeji = re.findall(pattern=vzorec_animeja, string=dump_contents, flags=re.DOTALL)

    csv_filename = "anime_data.csv"
    with open(csv_filename, mode="w", encoding=encoding) as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Rank", "Name", "ID", "Link", "Score", "Episodes", "Type", "Start Date", "End Date"])
        
        for en_anime in animeji:
            rank_pattern = r'<span class="lightLink top-anime-rank-text rank\d+">(\d+)</span>'
            rank = re.search(pattern=rank_pattern, string=en_anime).group(1)
            print(rank)

            name_pattern = r'<a href="https://myanimelist\.net/anime/\d+/[^"]+"[^>]*class="hoverinfo_trigger">(.*?)</a>'
            name = re.search(pattern=name_pattern, string=en_anime).group(1)
            print(name)

#            id_pattern = r''
#            id = re.search(pattern=id_pattern, string=en_anime)
#            print(id)
#
#            link_pattern = r''
#            link = re.search(pattern=link_pattern, string=en_anime)
#            print(link)
#
#            score_pattern = r''
#            score = re.search(pattern=score_pattern, string=en_anime)
#            print(score)
#
#            episodes_pattern = r''
#            episodes = re.search(pattern=episodes_pattern, string=en_anime)
#            print(episodes)
#
#            type_pattern = r''
#            type = re.search(pattern=type_pattern, string=en_anime)
#            print(type)
#
#            start_date_pattern = r''
#            start_date = re.search(pattern=start_date_pattern, string=en_anime)
#            print(start_date)
#
#            end_date_pattern = r''
#            end_date = re.search(pattern=end_date_pattern, string=en_anime)
#            print(end_date)
#
            filename = f"{rank}.html"
            folder = "single_anime_html"
            filepath = f"{folder}/{filename}"
            with open(file=filepath, mode="w", encoding=encoding) as en_anime_file:
                en_anime_file.write(en_anime)
            

            #writer.writerow([rank, name, id, link, score, episodes, type, start_date, end_date])
            writer.writerow([rank, name])

        
if __name__ == "__main__":
    main()