import csv
from dataclasses import dataclass, asdict

from bs4 import BeautifulSoup
import requests


@dataclass
class WeatherData:
    day: str
    avr_pressure: str
    avr_temperature: str
    max_temperature: str
    avr_humidity: str


def parse_td_tag(td_tag):
    weather_data = WeatherData(
        day=td_tag[0].text,
        avr_pressure=td_tag[1].text,
        avr_temperature=td_tag[6].text,
        max_temperature=td_tag[7].text,
        avr_humidity=td_tag[9].text,
    )

    return weather_data


def parse_html(response):
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", {'id': 'tablefix1', 'class': 'data2_s'})
    rows = table.find_all("tr")

    weather_data_list = []
    for i, row in enumerate(rows):
        # 表のヘッダーをスキップ
        if i < 4:
            continue
        td = row.find_all("td")
        weather_data = parse_td_tag(td)
        weather_data_list.append(weather_data)

    return weather_data_list


def main():
    url = "https://www.data.jma.go.jp/stats/etrn/view/daily_s1.php?prec_no=44&block_no=47662&year=1994&month=08"
    response = requests.get(url)
    weather_data_list = parse_html(response)


if __name__ == '__main__':
    main()
