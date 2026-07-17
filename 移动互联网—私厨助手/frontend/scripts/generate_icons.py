import zlib
import struct

def create_png(width, height, pixels):
    def chunk(chunk_type, data):
        chunk_data = chunk_type + data
        crc = zlib.crc32(chunk_data) & 0xffffffff
        return struct.pack('>I', len(data)) + chunk_data + struct.pack('>I', crc)
    
    signature = b'\x89PNG\r\n\x1a\n'
    
    ihdr = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    ihdr_chunk = chunk(b'IHDR', ihdr)
    
    raw_data = b''
    for y in range(height):
        raw_data += b'\x00'
        for x in range(width):
            r, g, b, a = pixels[y][x]
            raw_data += bytes([r, g, b, a])
    
    compressed = zlib.compress(raw_data)
    idat_chunk = chunk(b'IDAT', compressed)
    
    iend_chunk = chunk(b'IEND', b'')
    
    return signature + ihdr_chunk + idat_chunk + iend_chunk

def create_icon_pixels(color, icon_type, size=48):
    pixels = [[(255, 255, 255, 0) for _ in range(size)] for _ in range(size)]
    cx, cy = size // 2, size // 2
    
    if icon_type == 'home':
        for y in range(size):
            for x in range(size):
                if y < cy - 4:
                    if (x - cx) * (cy - 4 - y) <= (y - (cy - 4)) * (cx - x) and \
                       (cx - x) * (cy - 4 - y) <= (y - (cy - 4)) * (x - cx):
                        pixels[y][x] = color
                elif y >= cy - 4 and y < cy + 8:
                    if x >= cx - 12 and x <= cx + 12:
                        pixels[y][x] = color
                elif y >= cy + 8:
                    if x >= cx - 6 and x <= cx + 6:
                        pixels[y][x] = color
    
    elif icon_type == 'star':
        points = []
        for i in range(5):
            angle = math.radians(90 + i * 72)
            x = cx + int(14 * math.cos(angle))
            y = cy + int(14 * math.sin(angle))
            points.append((x, y))
        
        for y in range(size):
            for x in range(size):
                inside = True
                for i in range(5):
                    j = (i + 1) % 5
                    if ((points[j][0] - points[i][0]) * (y - points[i][1]) - 
                        (points[j][1] - points[i][1]) * (x - points[i][0])) < 0:
                        inside = False
                        break
                if inside:
                    pixels[y][x] = color
    
    elif icon_type == 'history':
        for y in range(size):
            for x in range(size):
                dx = x - cx
                dy = y - cy
                dist = (dx * dx + dy * dy) ** 0.5
                if 10 <= dist <= 14:
                    pixels[y][x] = color
            pixels[cy - 6][cx] = color
            pixels[cy - 6][cx + 6] = color
            for yy in range(cy - 6, cy + 1):
                pixels[yy][cx] = color
    
    return pixels

import math

normal_color = (138, 138, 138, 255)
active_color = (255, 107, 107, 255)

icons = ['home', 'star', 'history']
for icon in icons:
    pixels = create_icon_pixels(normal_color, icon)
    png_data = create_png(48, 48, pixels)
    with open(f'C:/Users/CBY/Desktop/移动互联网—私厨助手/frontend/static/{icon}.png', 'wb') as f:
        f.write(png_data)
    
    pixels_active = create_icon_pixels(active_color, icon)
    png_data_active = create_png(48, 48, pixels_active)
    with open(f'C:/Users/CBY/Desktop/移动互联网—私厨助手/frontend/static/{icon}-active.png', 'wb') as f:
        f.write(png_data_active)

print("Icons generated successfully!")
