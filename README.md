# Geohash Spatial Encoding Skill

Hierarchical Z-order curve space-filling spatial hashing engine in standard base32.

```mermaid
flowchart LR
    LatLon["Lat/Lon Coordinate"] --> Bisection["Recursive Interval Bisection"]
    Bisection --> Interleave["Interleave Lon/Lat Bits (Z-Order Morton Curve)"]
    Interleave --> Base32["Base-32 Character Grouping"]
    Base32 --> String["Compact Geohash String"]
```

## Features
- **100% Python Standard Library**: Bitwise interval subdivision.
- **Prefix Locality**: Shared prefixes correspond to spatial proximity.
