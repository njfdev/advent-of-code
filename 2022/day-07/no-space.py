class File:
    def __init__(self, name: str, fileSize: int):
        self.name = name
        self.size = fileSize

    def __str__(self) -> str:
        return f"{self.name} - {self.size}"


class Directory:
    subdiretories: []
    files: [File]

    def __init__(self, name: str, parent):
        self.name = name
        self.parent = parent
        self.subdiretories = []
        self.files = []

    def size(self) -> int:
        total = 0
        for sub in self.subdiretories:
            total += sub.size()

        for file in self.files:
            total += file.size

        return total

    def addSub(self, other):
        self.subdiretories.append(other)

    def addFile(self, file: File):
        self.files.append(file)

    def __str__(self) -> str:
        rv = f"Dir: {self.name} - {self.size()}\n"
        for file in self.files:
            rv += f"\t File: {file}\n"

        for sub in self.subdiretories:
            rv += f"\t {sub}\n"

        return rv


def checkAllowedDirs(currDir: Directory):
    for sub in currDir.subdiretories:
        if sub.size() < 100000:
            allowedDirs.append(sub)

        checkAllowedDirs(sub)


def checkDeletable(currDir: Directory):
    for sub in currDir.subdiretories:
        if sub.size() >= SPACENEEDEDTOBECLREAED:
            possibleDeletes.append(sub)
        checkDeletable(sub)


if __name__ == "__main__":
    with open("logs.txt", "r") as f:
        raw = [line.replace("\n", "") for line in f.readlines()]

    currentlyLS = False

    fileSystem = Directory("ROOT", "")
    currentDir: Directory = fileSystem

    for line in raw:
        if line.startswith("$"):
            if "cd" in line:
                where = line.split(" ")[2]
                if where == "..":
                    currentDir = currentDir.parent
                else:
                    createdDir = Directory(where, currentDir)
                    currentDir.addSub(createdDir)
                    currentDir = createdDir
        else:
            size, currentName = line.split(" ")
            if size.isnumeric():
                currentDir.addFile(File(currentName, int(size)))

    allowedDirs = []
    checkAllowedDirs(fileSystem)
    print(f"Solution 1: {sum([allowedDir.size() for allowedDir in allowedDirs])}")

    possibleDeletes = []

    TOTALSPACE = 70000000
    SPACEREQUIRED = 30000000
    USEDSPACE = fileSystem.size()
    SPACENEEDEDTOBECLREAED = SPACEREQUIRED - (TOTALSPACE - USEDSPACE)

    checkDeletable(fileSystem)

    print(
        f"Solution 2: {min([possibleDelete.size() for possibleDelete in possibleDeletes])}"
    )
