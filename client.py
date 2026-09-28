"""Geohash Hierarchical Base32 Spatial Engine.
100% Python Standard Library.
"""

class GeohashEngine:
    BASE32 = "0123456789bcdefghjkmnpqrstuvwxyz"
    BASE32_MAP = {c: i for i, c in enumerate(BASE32)}

    @staticmethod
    def encode(latitude, longitude, precision=12):
        lat_interval = [-90.0, 90.0]
        lon_interval = [-180.0, 180.0]
        geohash = []
        bits = [16, 8, 4, 2, 1]
        bit = 0
        ch = 0
        even = True
        
        while len(geohash) < precision:
            if even:
                mid = (lon_interval[0] + lon_interval[1]) / 2.0
                if longitude >= mid:
                    ch |= bits[bit]
                    lon_interval[0] = mid
                else:
                    lon_interval[1] = mid
            else:
                mid = (lat_interval[0] + lat_interval[1]) / 2.0
                if latitude >= mid:
                    ch |= bits[bit]
                    lat_interval[0] = mid
                else:
                    lat_interval[1] = mid
            even = not even
            if bit < 4:
                bit += 1
            else:
                geohash.append(GeohashEngine.BASE32[ch])
                bit = 0
                ch = 0
        return "".join(geohash)

    @staticmethod
    def decode(geohash):
        lat_interval = [-90.0, 90.0]
        lon_interval = [-180.0, 180.0]
        even = True
        bits = [16, 8, 4, 2, 1]
        for c in geohash.lower():
            cd = GeohashEngine.BASE32_MAP.get(c, 0)
            for mask in bits:
                if even:
                    mid = (lon_interval[0] + lon_interval[1]) / 2.0
                    if cd & mask:
                        lon_interval[0] = mid
                    else:
                        lon_interval[1] = mid
                else:
                    mid = (lat_interval[0] + lat_interval[1]) / 2.0
                    if cd & mask:
                        lat_interval[0] = mid
                    else:
                        lat_interval[1] = mid
                even = not even
        lat = (lat_interval[0] + lat_interval[1]) / 2.0
        lon = (lon_interval[0] + lon_interval[1]) / 2.0
        return round(lat, 6), round(lon, 6)
