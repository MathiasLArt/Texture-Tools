from PIL import Image
import os
import math
import statistics


class TexturePacker:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.images = [
            f
            for f in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, f))
        ]
        self.image_groups = {}
        self.pack_textures()

    def group_images(self):
        for img_file in self.images:
            name, _ = os.path.splitext(img_file)
            prefix = name.split("_")[-1]
            if prefix not in self.image_groups:
                self.image_groups[prefix] = []
            self.image_groups[prefix].append(img_file)

    def pack_textures(self):
        self.group_images()
        for prefix, img_files in self.image_groups.items():
            sizes = []
            for img_file in img_files:
                img_path = os.path.join(self.folder_path, img_file)
                img = Image.open(img_path)
                sizes.append(img.size)

            median_width = int(statistics.median([size[0] for size in sizes]))
            median_height = int(statistics.median([size[1] for size in sizes]))

            max_images_per_row = math.ceil(math.sqrt(len(img_files)))
            atlas_size = max_images_per_row * max(median_width, median_height)

            atlas = Image.new("RGBA", (atlas_size, atlas_size), (0, 0, 0, 0))

            x, y = 0, 0
            max_height_in_row = 0

            for img_file in img_files:
                img_path = os.path.join(self.folder_path, img_file)
                img = Image.open(img_path).convert("RGBA")
                img = img.resize((median_width, median_height))

                if x + img.width > atlas_size:
                    x = 0
                    y += max_height_in_row
                    max_height_in_row = 0

                atlas.paste(img, (x, y))
                x += img.width
                max_height_in_row = max(max_height_in_row, img.height)

            atlas.save(os.path.join(self.folder_path, f"texture_atlas_{prefix}.png"))
            print(f"Texture atlas for {prefix} saved as 'texture_atlas_{prefix}.png'")


if __name__ == "__main__":
    folder_path = r"C:\Users\Laptop\Desktop\Textures"
    packer = TexturePacker(folder_path)
