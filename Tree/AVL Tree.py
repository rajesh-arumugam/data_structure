class TruckNode:
    def __init__(self, Uid=None):
        self.UId = Uid
        self.chkoutCtr = 0
        self.left = None
        self.right = None


class AVLTree:
    def __init__(self):
        self.root = None
        self.max_count = None

    def treadTruckRec(self, value):
        try:
            if self.root == None:
                if self.max_count is None:
                    self.max_count = value
                    print('Assigning the maxmium deleiveries :', value)
                else:
                    self.root = TruckNode(value)
                    print('setting root node - {}, counter - {}'.format(value, self.root.chkoutCtr))
            else:
                self._readTruckRec(self.root, value)
        except:
            print('Input is empty!')

    def _readTruckRec(self, tNode, Uid):
        try:
            if Uid < tNode.UId:
                if tNode.left is None:
                    tNode.left = TruckNode(Uid)
                else:
                    self._readTruckRec(tNode.left, Uid)
                print('less than root node - {}, counter - {}'.format(tNode.UId, tNode.chkoutCtr))
            elif Uid > tNode.UId:
                if tNode.right is None:
                    tNode.right = TruckNode(Uid)
                else:
                    self._readTruckRec(tNode.right, Uid)
                print('greater than root node - {}, counter - {}'.format(tNode.UId, tNode.chkoutCtr))
            else:
                tNode.chkoutCtr += 1
                print('Value {} already inserted, counter - {}'.format(Uid, tNode.chkoutCtr))
        except:
            print('vehicle id {} no longer available for service'.format(Uid))


def main():
    tree = AVLTree()
    truck_ids = [2,10,10,20,10,40,50,10,30,20,10,20, 5, 2, 8, 3, 1,1]
    # truck_ids = []
    for truck in truck_ids:
        print(truck)
        tree.treadTruckRec(truck)


if __name__ == '__main__':
    main()
