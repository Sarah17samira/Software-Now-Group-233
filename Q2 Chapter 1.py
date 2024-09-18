from PIL import Image
import time

current_time = int(time.time())
generated_number = (current_time % 100) + 50
if generated_number % 2 == 0:
    generated_number += 10

print(f"Generated number: {generated_number}")

image = Image.open("Chapter1.jpg")
pixels = image.load()  # Get pixel data

width, height = image.size
total_red_sum = 0

for x in range(width):
    for y in range(height):
        r, g, b = pixels[x, y]
        new_r = min(r + generated_number, 255)  # Ensure it doesn't exceed 255
        new_g = min(g + generated_number, 255)
        new_b = min(b + generated_number, 255)
        pixels[x, y] = (new_r, new_g, new_b)
        total_red_sum += new_r


image.save("chapter1out.jpg")


print(f"Total sum of red pixel values: {total_red_sum}")
