# import local modules
from config_settings import *

# Data management
import pandas as pd

# ----------------------------------------------------------------------------
# Data Passing
# ----------------------------------------------------------------------------
# Create default geojson feature object
data_init = {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [0, 0]
      },
      "properties": {
        "timestamp":"",
        "image_id":"",
        "narrative":"",
        "contact": {
            "firstname": "",
            "lastname": "",
            "email": "",
            "phone": "",
            "contactable":"false",
            "preferred_contact": "null"
        }
      }
    }

# ----------------------------------------------------------------------------
# Globals
# ----------------------------------------------------------------------------

photos_metadata_file = os.path.join(DATA_PATH,'mosth-beulah-metadata.csv')
photos_metadata = pd.read_csv(photos_metadata_file)
photos_metadata.dropna(inplace=True)

# drop weird records with data url - TO DO: figure out what these are
images = photos_metadata[photos_metadata['Image_url'].str.startswith( 'http' )].copy()
images = photos_metadata.copy()
images['Details'] = images.apply(lambda x: x['Title'] + '\n  ' + x['Description'] + '\n  ' +x['Entry_ID'], axis=1)
images['image_url_thumbnail'] = images.apply(lambda x: x['Image_url'] + '#thumbnail', axis=1)
images['Photo'] = images.apply(lambda x: '![]({})'.format(x['image_url_thumbnail']), axis=1)
images.drop(columns=['Index'], inplace=True)
images['index'] = images['Entry_ID']
images.set_index('index', inplace=True)
images_list = list(images.index)

selected_image = '2013.001.030'
image = images.loc[selected_image]
