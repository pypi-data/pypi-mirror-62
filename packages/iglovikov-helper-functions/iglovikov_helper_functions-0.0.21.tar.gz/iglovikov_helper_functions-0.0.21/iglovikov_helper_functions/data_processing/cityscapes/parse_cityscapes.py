import argparse
from collections import namedtuple
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm

Label = namedtuple(
    "Label",
    [
        "name",  # The identifier of this label, e.g. 'car', 'person', ... . We use them to uniquely name a class
        "id",  # An integer ID that is associated with this label. The IDs are used to represent the label in ground
        # truth images. An ID of -1 means that this label does not have an ID and thus is ignored when creating
        # ground truth images (e.g. license plate).
        # Do not modify these IDs, since exactly these IDs are expected by the evaluation server.
        "trainId",  # Feel free to modify these IDs as suitable for your method. Then create ground truth images with
        # train IDs, using the tools provided in the 'preparation' folder. However, make sure to validate or submit
        # results to our evaluation server using the regular IDs above! For trainIds, multiple labels
        # might have the same ID. Then, these labels are mapped to the same class in the ground truth images.
        # For the inverse mapping, we use the label that is defined first in the list below.
        # For example, mapping all void-type classes to the same ID in training, might make sense for some approaches.
        # Max value is 255!
        "category",  # The name of the category that this label belongs to
        "categoryId",  # The ID of this category. Used to create ground truth images on category level.
        "hasInstances",  # Whether this label distinguishes between single instances or not
        "ignoreInEval",  # Whether pixels having this class as ground truth label are ignored during evaluations or not
        "color",  # The color of this label
    ],
)

# --------------------------------------------------------------------------------
# A list of all labels
# --------------------------------------------------------------------------------

# Please adapt the train IDs as appropriate for your approach.
# Note that you might want to ignore labels with ID 255 during training.
# Further note that the current train IDs are only a suggestion. You can use whatever you like.
# Make sure to provide your results using the original IDs and not the training IDs.
# Note that many IDs are ignored in evaluation and thus you never need to predict these!

labels = [
    #       name id trainId category catId hasInstances ignoreInEval color
    Label("unlabeled", 0, 255, "void", 0, False, True, (0, 0, 0)),
    Label("ego vehicle", 1, 255, "void", 0, False, True, (0, 0, 0)),
    Label("rectification border", 2, 255, "void", 0, False, True, (0, 0, 0)),
    Label("out of roi", 3, 255, "void", 0, False, True, (0, 0, 0)),
    Label("static", 4, 255, "void", 0, False, True, (0, 0, 0)),
    Label("dynamic", 5, 255, "void", 0, False, True, (111, 74, 0)),
    Label("ground", 6, 255, "void", 0, False, True, (81, 0, 81)),
    Label("road", 7, 0, "flat", 1, False, False, (128, 64, 128)),
    Label("sidewalk", 8, 1, "flat", 1, False, False, (244, 35, 232)),
    Label("parking", 9, 255, "flat", 1, False, True, (250, 170, 160)),
    Label("rail track", 10, 255, "flat", 1, False, True, (230, 150, 140)),
    Label("building", 11, 2, "construction", 2, False, False, (70, 70, 70)),
    Label("wall", 12, 3, "construction", 2, False, False, (102, 102, 156)),
    Label("fence", 13, 4, "construction", 2, False, False, (190, 153, 153)),
    Label("guard rail", 14, 255, "construction", 2, False, True, (180, 165, 180)),
    Label("bridge", 15, 255, "construction", 2, False, True, (150, 100, 100)),
    Label("tunnel", 16, 255, "construction", 2, False, True, (150, 120, 90)),
    Label("pole", 17, 5, "object", 3, False, False, (153, 153, 153)),
    Label("polegroup", 18, 255, "object", 3, False, True, (153, 153, 153)),
    Label("traffic light", 19, 6, "object", 3, False, False, (250, 170, 30)),
    Label("traffic sign", 20, 7, "object", 3, False, False, (220, 220, 0)),
    Label("vegetation", 21, 8, "nature", 4, False, False, (107, 142, 35)),
    Label("terrain", 22, 9, "nature", 4, False, False, (152, 251, 152)),
    Label("sky", 23, 10, "sky", 5, False, False, (70, 130, 180)),
    Label("person", 24, 11, "human", 6, True, False, (220, 20, 60)),
    Label("rider", 25, 12, "human", 6, True, False, (255, 0, 0)),
    Label("car", 26, 13, "vehicle", 7, True, False, (0, 0, 142)),
    Label("truck", 27, 14, "vehicle", 7, True, False, (0, 0, 70)),
    Label("bus", 28, 15, "vehicle", 7, True, False, (0, 60, 100)),
    Label("caravan", 29, 255, "vehicle", 7, True, True, (0, 0, 90)),
    Label("trailer", 30, 255, "vehicle", 7, True, True, (0, 0, 110)),
    Label("train", 31, 16, "vehicle", 7, True, False, (0, 80, 100)),
    Label("motorcycle", 32, 17, "vehicle", 7, True, False, (0, 0, 230)),
    Label("bicycle", 33, 18, "vehicle", 7, True, False, (119, 11, 32)),
    Label("license plate", -1, -1, "vehicle", 7, False, True, (0, 0, 142)),
]


def get_mapping_dict():
    """
    Returns: Dictionary with
        keys: original mask values
        values: target mask values
    """
    labels_df = pd.DataFrame(labels)
    labels_df = labels_df[~labels_df["ignoreInEval"]]
    mapping_dict = dict(zip(labels_df["id"].values, labels_df["trainId"]))
    return mapping_dict


def process_image(file_name: Path, target_folder: Path) -> None:
    img = cv2.imread(str(file_name))
    cv2.imwrite(str(target_folder / file_name.stem).replace("_leftImg8bit", "") + ".jpg", img)


def prepare_images(data_path: Path, sets=("train", "val", "test")) -> None:
    for _set in sets:
        set_folder = data_path / _set
        set_folder.mkdir(exist_ok=True, parents=True)

        target_folder = set_folder / "images"
        target_folder.mkdir(exist_ok=True)

        input_path = data_path / "leftImg8bit" / _set
        input_files = input_path.glob("**/*_leftImg8bit.png")

        for file_name in tqdm(sorted(input_files)):
            process_image(file_name, target_folder)


def process_mask(file_name: Path, mapping_dict: dict, target_folder: Path) -> None:
    old_mask = cv2.imread(str(file_name), 0)
    new_mask = np.ones(old_mask.shape) * 255
    for key, value in mapping_dict.items():
        ind = old_mask == key
        new_mask[ind] = value

        cv2.imwrite(str(target_folder / file_name.name).replace("_gtFine_labelIds", ""), new_mask)


def prepare_masks(data_path: Path, sets=("train", "val", "test")) -> None:
    mapping_dict = get_mapping_dict()

    for _set in sets:
        set_folder = data_path / _set
        set_folder.mkdir(exist_ok=True, parents=True)

        target_folder = set_folder / "masks"
        target_folder.mkdir(exist_ok=True)

        input_path = data_path / "gtFine" / _set
        input_files = input_path.glob("**/*_labelIds.png")

        for file_name in tqdm(sorted(input_files)):
            process_mask(file_name, mapping_dict, target_folder)


def main():
    parser = argparse.ArgumentParser("Convert Cityscapes to standard format.")
    arg = parser.add_argument
    arg("-d", "--data_path", type=Path, help="Path to unpacked zip files", required=True)
    args = parser.parse_args()

    prepare_images(args.data_path, ("train", "val", "test"))
    prepare_masks(args.data_path, ("train", "val", "test"))


if __name__ == "__main__":
    main()
