from math import radians, cos, sin, asin, sqrt

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calcula a distância entre dois pontos geográficos em km (Haversine)
    """
    # Converter para radianos
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    # Diferenças
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    
    # Fórmula de Haversine
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371  # Raio da Terra em km
    
    return c * r

def get_distance_string(lat1, lon1, lat2, lon2):
    """Retorna distância formatada"""
    dist_km = calculate_distance(lat1, lon1, lat2, lon2)
    
    if dist_km < 1:
        return f"{dist_km*1000:.0f}m"
    else:
        return f"{dist_km:.2f}km"

def is_within_radius(user_lat, user_lon, venue_lat, venue_lon, radius_km=0.1):
    """Verifica se o usuário está dentro do raio permitido"""
    distance = calculate_distance(user_lat, user_lon, venue_lat, venue_lon)
    return distance <= radius_km
