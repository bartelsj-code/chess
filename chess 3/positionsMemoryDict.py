import csv

class PositionsMemoryDict:
    def __init__(self, memoryFileName):
        self.fileName = memoryFileName
        self.dict = {}
        self.importMemory()
        # Import from storage file
        # id : [depth, eval]
        pass

    def hasEval(self, id, depth):
        if id in self.dict:
            try:
                if self.dict[id][0] >= depth:
                    return True
            except:
                print(self.dict[id])
        return False

    def getEval(self, id):
        return self.dict[id][1]    

    def update(self, id, depth, eval):
        self.dict[id] = [depth, eval]

    def importMemory(self):
        with open(self.fileName, 'r') as file:
            content = csv.reader(file)
            for row in content:
                id = row[0]
                depth = int(row[1])
                eval = float(row[2])
                self.dict[id] = [depth, eval]
        file.close()

    def exportMemory(self):
        with open(self.fileName, 'w', newline = '') as file:
            writer = csv.writer(file, delimiter=',')
            for id in self.dict:
                row = [id] + self.dict[id]
                writer.writerow(row)
        file.close()


    





