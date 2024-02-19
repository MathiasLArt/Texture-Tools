from PIL import Image
import os
import math
import statistics


def pack_textures(folder_path):
    # Scan the folder for images
    images = [
        f
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]

    # Group images based on their suffixes
    image_groups = {}
    for img_file in images:
        name, _ = os.path.splitext(img_file)
        prefix = name.split("_")[-1]  # Use the last part as the suffix
        if prefix not in image_groups:
            image_groups[prefix] = []
        image_groups[prefix].append(img_file)

    # Process each group and create a texture atlas
    for prefix, img_files in image_groups.items():
        # Get the sizes of all images in the group
        sizes = []
        for img_file in img_files:
            img_path = os.path.join(folder_path, img_file)
            img = Image.open(img_path)
            sizes.append(img.size)

        # Calculate median width and height
        median_width = int(statistics.median([size[0] for size in sizes]))
        median_height = int(statistics.median([size[1] for size in sizes]))

        # Calculate maximum number of images per row based on median size
        max_images_per_row = math.ceil(math.sqrt(len(img_files)))

        # Calculate atlas size based on median size and max images per row
        atlas_size = max_images_per_row * max(median_width, median_height)

        # Create the texture atlas
        atlas = Image.new("RGBA", (atlas_size, atlas_size), (0, 0, 0, 0))

        x, y = 0, 0
        max_height_in_row = 0

        for img_file in img_files:
            img_path = os.path.join(folder_path, img_file)
            img = Image.open(img_path).convert("RGBA")
            img = img.resize((median_width, median_height))  # Resize to 2048x2048

            # If the next image doesn't fit in the current row, move to the next row
            if x + img.width > atlas_size:
                x = 0
                y += max_height_in_row
                max_height_in_row = 0

            # Paste the image onto the atlas
            atlas.paste(img, (x, y))

            # Update x and max_height_in_row for the next image
            x += img.width
            max_height_in_row = max(max_height_in_row, img.height)

        # Save the texture atlas
        atlas.save(os.path.join(folder_path, f"texture_atlas_{prefix}.png"))
        print(f"Texture atlas for {prefix} saved as 'texture_atlas_{prefix}.png'")


# Example usage:
folder_path = r"C:\Users\Laptop\Desktop\Textures"
pack_textures(folder_path)
