import os
import shutil
import glob
import pandas as pd
from tqdm import tqdm

CSV_FILENAME = "_classes.csv"
LABELS = ['Diff_Direction', 'Non_Pedestrain', 'Opp_Direction', 'Running', 'Sitting', 'Sleeping', 'Standing']

train_path = "../dataset/train"
test_path = "../dataset/test"
valid_path = "../dataset/valid"

train_updatednames_path = "../dataset/output/train_updatednames"
test_updatednames_path = "../dataset/output/test_updatednames"
valid_updatednames_path = "../dataset/output/valid_updatednames"

train_splited_path = "../dataset/output/train_splited"
test_splited_path = "../dataset/output/test_splited"
valid_splited_path = "../dataset/output/valid_splited"



class ImageProcessor:

    @staticmethod
    def create_folder(path):
        if not os.path.exists(path):
            os.makedirs(path)

    def copy_images_with_updated_filenames(self, input_path, output_path):
        self.create_folder(output_path)

        csv_path = os.path.join(input_path, self.CSV_FILENAME)
        df = pd.read_csv(csv_path)

        total = len(df)
        pbar = tqdm(total=total)

        for _, row in df.iterrows():
            image_filename = row['filename']
            image_classes = row[self.LABELS]

            image_path = os.path.join(input_path, image_filename)

            selected_labels = [label for label, value in image_classes.items() if value == 1]
            selected_labels = [label.replace(" ", "") for label in selected_labels]

            updated_filename = f"{os.path.splitext(image_filename)[0]}-{'-'.join(selected_labels)}.jpg"
            new_image_path = os.path.join(output_path, updated_filename)

            try:
                shutil.copyfile(image_path, new_image_path)
            except Exception as e:
                print(new_image_path)
                print("#" * 50)
                print(e)
                print("#" * 50)

            pbar.update(1)

        pbar.close()
        image_number = len(glob.glob(output_path + "/*.jpg"))
        print(f"{image_number} images in {output_path}")

    def split_images(self, input_path, output_path):
        self.create_folder(output_path)

        total = len(os.listdir(input_path))
        pbar = tqdm(total=total)

        labels = [label.strip() for label in self.LABELS]
        for label in labels:
            folder_path = os.path.join(output_path, label)
            self.create_folder(folder_path)

        for filename in os.listdir(input_path):
            for label in labels:
                if label in filename:
                    src = os.path.join(input_path, filename)
                    dest = os.path.join(output_path, label, filename)
                    try:
                        shutil.copyfile(src, dest)
                    except Exception as e:
                        print(dest)
                        print("#" * 50)
                        print(e)
                        print("#" * 50)
            pbar.update(1)

        pbar.close()

    def count_images_in_folder(self, folder_path, labels=None):
        # folder_path: folder that contains labels / images (if labels is None)

        assert isinstance(labels, list) or labels is None
        assert os.path.exists(folder_path)

        if labels:
            for label in labels:
                path = os.path.join(folder_path, label)
                image_number = len(glob.glob(path + "/*.jpg"))
                print(f"{image_number} images in {label}")
        else:
            image_number = len(glob.glob(folder_path + "/*.jpg"))
            print(f"{image_number} images in {folder_path}")


if __name__ == "__main__":
    image_processor = ImageProcessor()

    image_processor.copy_images_with_updated_filenames(train_path, train_updatednames_path)
    image_processor.copy_images_with_updated_filenames(test_path, test_updatednames_path)
    image_processor.copy_images_with_updated_filenames(valid_path, valid_updatednames_path)

    image_processor.split_images(train_updatednames_path, train_splited_path)
    image_processor.split_images(test_updatednames_path, test_splited_path)
    image_processor.split_images(valid_updatednames_path, valid_splited_path)

    image_processor.count_images_in_folder(train_splited_path, labels=LABELS)
    image_processor.count_images_in_folder(test_splited_path, labels=LABELS)
    image_processor.count_images_in_folder(valid_splited_path, labels=LABELS)

