from bs4 import BeautifulSoup
import urllib.request
from datetime import datetime,timedelta
import re
from enum import Enum
"""
import dekrr_parser
dekrr_parser.getDekrrData(parse.date, 2)
"""

DEKRR_AREAS = (
        (1    , 'S2 02 BR (buchbar: von allen)'),
        (5    , 'S2 02 C301 (buchbar: vom Dekanat, Fachschaft)'),
        (7    , 'S2 02 D103 ((Dekanat))'),
        (10   , 'S2 02 ISP Pool ((buchbar: ISP))'),
        (9    , 'S2 02 Lernzentrum-Freibereich ()'),
        (11   , 'S3 19 Rundeturmstrasse 12 ()'),
        (8    , 'S4 14 Mornewegstrasse 30 ()'),
    )

class RoomStatus(Enum):
    OK = 1
    BLOCKED = 2

def getAllDekrrData(date):
    rooms = []
    for area_id, area_desc in DEKRR_AREAS:
        rooms = rooms + getDekrrData(date, area_id)
    return rooms

def getDekrrData(date, area):
    url_format = "https://mrbs.informatik.tu-darmstadt.de/day.php?year=%d&month=%d&day=%d&area=%d"
    source_url = url_format % (date.year, date.month, date.day, area)
    
    with urllib.request.urlopen(source_url) as response:
       html_code = response.read()
    soup = BeautifulSoup(html_code)
    
    the_tab = soup.find("table", {"cellspacing": "0"})
    header = the_tab.tr
    content = the_tab.find_all('tr')[1:]
    
    cols = []
    for th in header.find_all('th')[1:]:
        match = re.match(r"(.*)\(([0-9]+)\)$", th.get_text())
        cols.append( ( match.group(1) , match.group(2) , [] ) )
    
    zeit = date
    for row in content:
        tds = row.find_all('td')
        (z_hour, z_min) = tds[0].get_text().strip().split(':')
        zeit = date.replace(hour=int(z_hour), minute=int(z_min), second=0, microsecond=0)
        for idx, col in enumerate(tds[1:]):
            if col.get_text().strip() == '"':
                # continuation, extend last event by 15 minutes
                cols[idx][2][-1]['end_time'] += timedelta(minutes=15)
            elif col.a != None:
                match = re.search(r"id=([0-9]+)", col.a['href'])
                if match == None: continue
                komm =  col.get_text().strip()
                status = RoomStatus.BLOCKED
                if 'KIF' in komm or 'Konferenz der Informatikfachschaften' in komm:
                    status = RoomStatus.OK
                cols[idx][2].append({
                    'start_time': zeit,
                    'end_time': zeit + timedelta(minutes=15),
                    'room': cols[idx][0],
                    'kommentar': komm,
                    'mgmt_id': match.group(1),
                    'status': status,
                })
    return cols


date = datetime.now()


