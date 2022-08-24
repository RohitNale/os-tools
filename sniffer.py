import os
import time
import argparse
import shutil
from tqdm import tqdm
import concurrent.futures


def create_folder(folder_name):
    """Create folder_name if not exists in the folder.
    """
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


class sniffer:
    """ Perform basic task without threading or multiprocessing
    """
    def __init__(
        self, src, dst, topdown, show, empty, del_empty, copy, move, del_folder
    ):
        self.src = src
        self.dst = dst
        self.topdown = topdown
        self.show = show
        self.empty = empty
        self.del_empty = del_empty
        self.copy = copy
        self.move = move
        self.del_folder = del_folder

    def main(self):
        if self.show:
            self.isShow()
        if self.empty:
            self.isEmpty()
        if self.del_empty:
            self.delEmpty()

        lst = os.listdir(self.src)

        if self.copy:
            create_folder(self.dst)
            for _ in tqdm(map(self.isCopy, lst), total=len(lst), desc="Copying"):
                continue

        if self.move:
            create_folder(self.dst)
            for _ in tqdm(map(self.isMove, lst), total=len(lst), desc="Moving"):
                continue

        if self.del_folder:
            for _ in tqdm(map(self.isDel, lst), total=len(lst), desc="Deleting"):
                continue

    def isShow(self):
        # Show all files and folders
        for root, dirs, files in os.walk(self.src, topdown=self.topdown):
            print("ROOT =", root)
            print("Dir:", len(dirs), "|", "Files:", len(files))
            if len(dirs) > 0:
                for dir in dirs:  # Show Folder
                    subfolders = os.path.join(root, dir)
                    print(subfolders)

    def isEmpty(self):
        # Check for empty directories
        empty = []
        for root, dirs, files in os.walk(self.src, topdown=self.topdown):
            if not len(dirs) and not len(files):
                print(root)
                empty.append(root)
        return empty

    def delEmpty(self):
        # Delete for empty directories
        empty_folder = self.isEmpty(self)
        map(self.isDel, empty_folder)
        print(f"Delete all empty folder from {self.src}")

    def isCopy(self, file):
        # Copy all files and folders
        try:
            file_name = os.path.join(self.src, file)
            shutil.copy(file_name, self.dst)
        except:  # If source and destination are same
            pass

    def isMove(self, file):
        # Move all files and folders
        try:
            file_name = os.path.join(self.src, file)
            shutil.move(file_name, self.dst)
        except:  # If source and destination are same
            pass

    def isDel(self, file):
        # Remove all filezs and folders
        try:
            os.remove(file)
        except:  # If file not exists
            pass


class mpsniffer(sniffer):
    """ Perform basic task using threading and multiprocessing
    """
    def __init__(
        self, src, dst, topdown, show, empty, del_empty, copy, move, del_folder
    ):
        super().__init__
        self.src = src
        self.dst = dst
        self.topdown = topdown
        self.show = show
        self.empty = empty
        self.del_empty = del_empty
        self.copy = copy
        self.move = move
        self.del_folder = del_folder

    def main(self):
        if self.show:
            self.isShow()
        if self.empty:
            self.isEmpty()
        if self.del_empty:
            self.delEmpty()

        # with concurrent.futures.ProcessPoolExecutor() as executor:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # ThreadPoolExecutor is Faster compare to ProcessPoolExecutor
            lst = os.listdir(self.src)

            if self.copy:
                create_folder(self.dst)
                for _ in tqdm(
                    executor.map(self.isCopy, lst), total=len(lst), desc="Copying"
                ):
                    continue

            if self.move:
                create_folder(self.dst)
                for _ in tqdm(
                    executor.map(self.isMove, lst), total=len(lst), desc="Moving"
                ):
                    continue

            if self.del_folder:
                for _ in tqdm(
                    executor.map(self.isDel, lst), total=len(lst), desc="Deleting"
                ):
                    continue


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--src", default="", required=True, help="Input folder")
    parser.add_argument("-d", "--dst", default="", help="Output folder")
    parser.add_argument("--topdown", type=bool, default=False, help="Set Topdown")
    parser.add_argument(
        "--show", default=False, action="store_true", help="Show folder"
    )
    parser.add_argument(
        "--empty", default=False, action="store_true", help="Check empty folder"
    )
    parser.add_argument(
        "--del_empty", default=False, action="store_true", help="Delete empty folder"
    )
    parser.add_argument(
        "--copy", default=False, action="store_true", help="Copy folder"
    )
    parser.add_argument(
        "--move", default=False, action="store_true", help="Move folder"
    )
    parser.add_argument(
        "--del_folder", default=False, action="store_true", help="Delete folder"
    )

    opt = parser.parse_args()
    mltprocess = True
    t0 = time.perf_counter()
    if mltprocess:
        snif = mpsniffer(**vars(opt))
        snif.main()
    else:
        snif = sniffer(**vars(opt))
        snif.main()
    t1 = time.perf_counter()
    print(f"Finished in {t1 - t0:.2f} sec")
