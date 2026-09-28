"""Example demonstrating Geohash encoding and decoding."""
from client import GeohashEngine

def main():
    lat, lon = 37.7749, -122.4194
    gh = GeohashEngine.encode(lat, lon, precision=9)
    print(f"Encoded ({lat}, {lon}) -> {gh}")
    dec_lat, dec_lon = GeohashEngine.decode(gh)
    print(f"Decoded {gh} -> ({dec_lat}, {dec_lon})")

if __name__ == "__main__":
    main()
