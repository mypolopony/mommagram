from exif import Image
from instagrapi import Client
from instagrapi.types import Location

ACCOUNT_USERNAME='mypolopony'
ACCOUNT_PASSWORD='z!bB3!UL'

def dms_to_dd(gps_coords, gps_coords_ref):
    '''
    The GPS coordinates from exif are in degrees, minutes, seconds (DMS) format.
    
    To convert to decimal degrees, the basic formula is:
    
    degrees + minutes / 60 + seconds / 3600
    
    Note that 'W' longitudes and 'S' latitudes are negative, so we need to use the
    gps_latitude_ref and gps_longitude_ref properties to determine that.
    '''
    
    d, m, s =  gps_coords
    dd = d + m / 60 + s / 3600
    
    if gps_coords_ref.upper() in ('S', 'W'):
        return -dd
    elif gps_coords_ref.upper() in ('N', 'E'):
        return dd
    else:
        raise RuntimeError('Incorrect gps_coords_ref {}'.format(gps_coords_ref))


def reverse_geocode(lat_dd, lon_dd):
    '''
    Simple wrapper to return a place name from lat/lon decimals
    '''
    
    return loc.reverse('{}, {}'.format(lat_dd, lon_dd))


if __name__ == '__main__':
    # Open
    print('Running')
    
    # Client
    cl = Client()

    # Authentication
    cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)

    # Sanity Test
    user_id = cl.user_id_from_username('mypolopony')
    medias = cl.user_medias(user_id, 20)

    # JPEG Example
    img_path = '/Users/mypolopony/Pictures/mom/IMG_2260.jpeg'

    # JPEG Image info and Post
    with open(img_path, 'rb') as src:
        img = Image(src)
        lat_dd = dms_to_dd(img.gps_latitude, img.gps_latitude_ref)
        lon_dd = dms_to_dd(img.gps_longitude, img.gps_longitude_ref)

        print('Location: {}'.format(reverse_geocode(lat_dd, clon_dd)))

        # Post
        media = cl.photo_upload(
            fn,
            "Test caption for photo with #nails and mention users such @mypolopony",
            location = Location(name=locname[0], lat=lat_dd, lng=lon_dd),
            extra_data={
                "custom_accessibility_caption": "overridden custom accessibility caption"
            }
        )
