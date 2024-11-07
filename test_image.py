from PIL import Image

try:
    img = Image.open("C:\\Users\\S\\OneDrive\\Desktop\\python\\microphone.png")
    img.show() 
except Exception as e:
    print(f"Error: {e}")
