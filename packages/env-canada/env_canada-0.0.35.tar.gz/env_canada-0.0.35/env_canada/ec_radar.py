import datetime
from io import BytesIO
import json
import os
from PIL import Image

from bs4 import BeautifulSoup
from geopy import distance
import imageio
import requests
from requests_futures.sessions import FuturesSession

IMAGES_URL = 'https://dd.weather.gc.ca/radar/PRECIPET/GIF/{0}/?C=M;O=D'
FRAME_URL = 'https://dd.weather.gc.ca/radar/PRECIPET/GIF/{0}/{1}'
CITIES_URL = 'https://weather.gc.ca/cacheable/images/radar/layers/default_cities/{0}_towns.gif'
ROADS_URL = 'https://weather.gc.ca/cacheable/images/radar/layers/roads/{0}_roads.gif'

"""Load list of radar sites."""
with open(os.path.join(os.path.dirname(__file__), 'radar_sites.json')) as sites_file:
    site_dict = json.loads(sites_file.read())


def closest_site(lat, lon):
    """Return the site code of the closest radar to our lat/lon."""

    def site_distance(measure_site):
        """Calculate distance to a site."""
        return distance.distance((lat, lon), (measure_site[1]['lat'], measure_site[1]['lon']))

    closest = min(site_dict.items(), key=site_distance)

    return closest


class ECRadar(object):
    def __init__(self, station_id=None, coordinates=None, precip_type=None):
        """Initialize the data object."""
        if station_id:
            self.station_code = station_id
        elif coordinates:
            self.station_code = closest_site(coordinates[0], coordinates[1])[0]

        self.station_name = site_dict[self.station_code]['name']

        if precip_type:
            self.user_precip_type = precip_type
        else:
            self.user_precip_type = None

        cities_bytes = requests.get(CITIES_URL.format(self.station_code.lower())).content
        self.cities = Image.open(BytesIO(cities_bytes)).convert('RGBA')
        roads_bytes = requests.get(ROADS_URL.format(self.station_code.upper())).content
        self.roads = Image.open(BytesIO(roads_bytes)).convert('RGBA')

        self.timestamp = datetime.datetime.now()

    def get_precip_type(self):
        """Determine the precipitation type"""
        if self.user_precip_type:
            return self.user_precip_type
        elif datetime.date.today().month in range(4, 11):
            return 'RAIN'
        else:
            return 'SNOW'

    def get_frames(self, count):
        """Get a list of images from Environment Canada."""
        soup = BeautifulSoup(requests.get(IMAGES_URL.format(self.station_code)).text, 'html.parser')
        image_links = [tag['href'] for tag in soup.find_all('a') if '.gif' in tag['href']]

        if len([i for i in image_links[:8] if 'COMP' in i]) > 4:
            image_string = '_'.join([self.station_code, 'COMP_PRECIPET', self.get_precip_type() + '.gif'])
        else:
            image_string = '_'.join([self.station_code, 'PRECIPET', self.get_precip_type() + '.gif'])

        images = [tag['href'] for tag in soup.find_all('a') if image_string in tag['href']]

        """Update timestamp."""
        self.timestamp = datetime.datetime.strptime(images[0].split('_')[0],
                                                    '%Y%m%d%H%M')

        """Build GIF."""
        futures = []
        session = FuturesSession(max_workers=count)

        for i in reversed(images[:count]):
            url = FRAME_URL.format(self.station_code, i)
            futures.append(session.get(url=url).result().content)

        def add_layers(frame):
            frame_bytesio = BytesIO()
            base = Image.open(BytesIO(frame)).convert('RGBA')
            base.alpha_composite(self.roads)
            base.alpha_composite(self.cities)
            base.save(frame_bytesio, 'GIF')
            frame_bytesio.seek(0)
            return frame_bytesio.read()

        frames = [add_layers(f) for f in futures if f[0:3] == b'GIF']

        """Repeat last frame."""
        for i in range(0, 2):  # pylint: disable=unused-variable
            frames.append(frames[count - 1])

        return frames

    def get_latest_frame(self):
        """Get the latest image from Environment Canada."""
        return self.get_frames(1)[0]

    def get_loop(self):
        """Build an animated GIF of recent radar images."""
        if len(self.station_code) == 5:
            count = 20
            fps = 10
        else:
            count = 12
            fps = 6

        frames = self.get_frames(count)
        gifs = [imageio.imread(f) for f in frames]

        return imageio.mimwrite(imageio.RETURN_BYTES,
                                gifs,
                                format='GIF',
                                fps=fps)
