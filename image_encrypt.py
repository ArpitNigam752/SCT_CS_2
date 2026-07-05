from PIL import Image,ImageOps
import numpy as np

# Encryption Key
KEY = 50


def encrypt_image():
    """Encrypt the image by adding a key to each pixel."""

    image = ImageOps.exif_transpose(Image.open("original.jpg"))
    img_array = np.array(image)

    encrypted_array = (img_array.astype(np.uint16) + KEY) % 256
    encrypted_array = encrypted_array.astype(np.uint8)

    encrypted_image = Image.fromarray(encrypted_array)
    encrypted_image.save("encrypted.png")

    print("Image Encrypted Successfully!")
    encrypted_image.show()


def decrypt_image():
    """Decrypt the image by subtracting the key from each pixel."""

    encrypted_image = Image.open("encrypted.png")
    encrypted_array = np.array(encrypted_image)

    decrypted_array = (encrypted_array.astype(np.int16) - KEY) % 256
    decrypted_array = decrypted_array.astype(np.uint8)

    decrypted_image = Image.fromarray(decrypted_array)
    decrypted_image.save("decrypted.png")

    print("Image Decrypted Successfully!")
    decrypted_image.show()


def main():
    encrypt_image()
    decrypt_image()


if __name__ == "__main__":
    main()