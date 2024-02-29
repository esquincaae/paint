import cv2

def draw_line(image, start, end, color=(0, 0, 0), thickness=2):
    """Dibuja una línea en una imagen."""
    cv2.line(image, start, end, color, thickness)

def draw_polyline(image, start, end, color=(0, 0, 0), thickness=2):
    """Dibuja segmentos de una polilínea en una imagen."""
    cv2.line(image, start, end, color, thickness)

def draw_rectangle(image, start, end, color=(0, 0, 0), thickness=2):
    """Dibuja un rectángulo en una imagen."""
    cv2.rectangle(image, start, end, color, thickness)

def draw_circle(image, center, radius, color=(0, 0, 0), thickness=2):
    """Dibuja un círculo en una imagen."""
    cv2.circle(image, center, radius, color, thickness)

def erase_area(image, top_left, bottom_right, color=(255, 255, 255), thickness=-1):
    """Borra un área rectangular en una imagen."""
    cv2.rectangle(image, top_left, bottom_right, color, thickness)
