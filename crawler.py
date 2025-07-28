import csv
from dataclasses import dataclass
from typing import List

from bs4 import BeautifulSoup
from loguru import logger
import click
import requests


@dataclass
class WeatherData:
    day: str
    avr_pressure: str
    avr_temperature: str
    max_temperature: str
    avr_humidity: str


def write_csv(weather_data_list: List[WeatherData], year: str, month: str):
    with open("output.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # ヘッダー書き込み
        writer.writerow(["day", "avr_pressure", "avr_temperature", "max_temperature", "avr_humidity"])

        # データを書き込む
        for weather_data in weather_data_list:
            date = f"{year}-{month.zfill(2)}-{weather_data.day.zfill(2)}"
            writer.writerow([
                date,
                weather_data.avr_pressure,
                weather_data.avr_temperature,
                weather_data.max_temperature,
                weather_data.avr_humidity
            ])

def get_from_td_tag(td_tag):
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
        weather_data = get_from_td_tag(td)
        weather_data_list.append(weather_data)

    return weather_data_list


@click.command()
@click.option("--year", type=str)
@click.option("--month", type=str)
def main(year: str, month: str):
    logger.info("target: {}/{}", year, month)

    url = f"https://www.data.jma.go.jp/stats/etrn/view/daily_s1.php?prec_no=44&block_no=47662&year={year}&month={month}"
    response = requests.get(url)
    weather_data_list = parse_html(response)
    write_csv(weather_data_list, year, month)

    logger.success("output done")


if __name__ == '__main__':
    main()
