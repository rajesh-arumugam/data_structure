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
        self.count = 0

    def treadTruckRec(self, value):
        try:
            if self.root == None:
                if self.max_count is None:
                    self.max_count = value
                    # print('Assigning the maxmium deleiveries :', value)
                else:
                    self.root = TruckNode(value)
                    # print('setting root node - {}, counter - {}'.format(value, self.root.chkoutCtr))
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
                # print('less than root node - {}, counter - {}'.format(tNode.UId, tNode.chkoutCtr))
            elif Uid > tNode.UId:
                if tNode.right is None:
                    tNode.right = TruckNode(Uid)
                else:
                    self._readTruckRec(tNode.right, Uid)
                # print('greater than root node - {}, counter - {}'.format(tNode.UId, tNode.chkoutCtr))
            else:
                tNode.chkoutCtr += 1
                # print('Value {} already inserted, counter - {}'.format(Uid, tNode.chkoutCtr))
            if tNode.chkoutCtr > 4:
                pass
                # print('vehicle id {} no longer available for service'.format(Uid))
        except:
            print('vehicle {} no longer available for service'.format(Uid))

    def tupdateTruckRec(self, prompt):
        if prompt is not None:
            # print('tupdateTruckRec')
            split_prompt = prompt.split(':')
            # print(split_prompt)
            truck_id = int(split_prompt[1].lstrip())
            # print(truck_id)
            self._updateTruckRec(self.root, truck_id)

    def _updateTruckRec(self, tNode, Uid):
        if type(Uid)==int:
            self._readTruckRec(tNode, Uid)
            print(f'Vehicle Id {Uid} record updated')
            print('------------------------------------')
        return

    def tprintTruckRec(self, prompt):
        if prompt is not None:
            self._printTruckRec(self.root)

    def countTrucks(self, root):
        if root is None:
            return -1
        else:
            count = 1
            if root.left is not None:
                count += self.countTrucks(root.left)
            if root.right is not None:
                count += self.countTrucks(root.right)
            return count

    def inorder(self, root):
        if root is not None:
            self.inorder(root.left)
            print(root.UId,", ",root.chkoutCtr)
            self.inorder(root.right)

    def _printTruckRec(self, tNode):
        count = self.countTrucks(tNode)
        print(f'Total number of vehicles entered in the warehouse: {count}')
        self.inorder(tNode)
        print('------------------------------------')

    def tcheckTruckRec(self, prompt):
        if prompt is not None:
            # print('tupdateTruckRec')
            split_prompt = prompt.split(':')
            # print(split_prompt)
            truck_id = int(split_prompt[1].lstrip())
            # print(truck_id)
            self._checkTruckRec(self.root, truck_id)

    def searchTree(self, root, key):
        # if root in None:
        #     print(f'Vehicle id {key} did not come to the warehouse today')
        if root.UId == key:
            return root.UId,2, root.chkoutCtr
        if root.UId < key:
            if root.right is None:
                return key, -1, root.chkoutCtr
            return self.searchTree(root.right, key)
        if root.UId > key:
            if root.left is None:
                return key, -1, root.chkoutCtr
            return self.searchTree(root.left, key)
        # else:
        #     return str(key)+' found'


    def _checkTruckRec(self, tNode, Uid):
        if type(Uid) == int:
            print(Uid)
            result = self.searchTree(tNode, Uid)
            # print(result)
            if result[1] == -1:
                print(f'Vehicle id {result[0]} did not come to the warehouse today')
            else:
                if result[1] == 0:
                    print(f'Vehicle id {result[0]} just reached the warehouse')
                if result[1] % 2 == 0:
                    print(f'Vehicle id {result[0]} entered {result[2]} times into the system. It just completed an order')
                if result[1] % 2 != 0:
                    print(f'Vehicle id {result[0]} entered {result[2]} times into the system. It is currently fulfilling an open order')
            print('------------------------------------')

    def tprintOrderStatus(self, prompt):
        if prompt is not None:
            # print('tupdateTruckRec')
            split_prompt = prompt.split(':')
            # print(split_prompt)
            truck_id = int(split_prompt[1].lstrip())
            print(f'The following status of {truck_id} orders:')
            self._printOrderStatus(truck_id)
            

    def _printOrderStatus(self, targetorders):
        result = list(self.getList(self.root))
        result = filter(lambda y: y[1]> 0, result)
        print(list(result))
        for x in list(result):
            print(x)
        # print(data(result))
        print('Open Orders: {}')
        print('Closed Orders: {}')
        print('Yet to be fulfilled: {}')
        print('------------------------------------')

    def getList(self, root):
        if not root:
            return
        yield from self.getList(root.left)
        yield root.UId,root.chkoutCtr
        yield from self.getList(root.right)

    def thighFreqTrucks(self, prompt):
        if prompt is not None:
            # print('tupdateTruckRec')
            split_prompt = prompt.split(':')
            # print(split_prompt)
            frequency = int(split_prompt[1].lstrip())
            print(f'Vehicles that moved in/out more than {frequency} times are:')
            self._highFreqTrucks(self.root, frequency)

    def _highFreqTrucks(self, tNode, frequency):
        tree = list(self.getList(tNode))
        for x in tree:
            if x[1] > frequency:
                print(x)
        print('------------------------------------')

    def tmaxDeliveries(self, prompt):
        self._maxDeliveries(self.root)

    def _maxDeliveries(self, tNode):
        print(f'maxDeliveries: {self.max_count}')
        tree = list(self.getList(tNode))
        # print(tree)
        count = []
        for x in tree:
            if x[1] >= 2*self.max_count:
                # print(x)
                count.append(x)
        print(f'{len(count)} Vehicle Ids did their maximum deliveries:')
        print(count)
        print('------------------------------------')

    # def tavailTrucks(self, prompt):
    #     self._availTrucks(self.root)

    def searchTreeRecord(self, root):
        # print(printCount)
        if root is None:
                return
        else:
            self.searchTreeRecord(root.left)
            if (root.chkoutCtr % 2 == 0 and root.chkoutCtr < 2*self.max_count) or root.chkoutCtr == 0:
                print(root.UId)
            self.searchTreeRecord(root.right)


    def countAvailTruck(self, root):
        try:
            if root is None:
                return 0
            else:
                self.countAvailTruck(root.left)
                if (root.chkoutCtr % 2 == 0 and root.chkoutCtr < 2*self.max_count) or root.chkoutCtr == 0:
                    self.count += 1
                self.countAvailTruck(root.right)
        except Exception as e:
            print(str(e))

    def _availTrucks(self, tNode):
        self.countAvailTruck(tNode)
        print(f'{self.count} Vehicle Ids that are currently available to deliver supplies:')
        self.searchTreeRecord(tNode)
        print('------------------------------------')

    def checkPrompt(self, prompt):
        if prompt is not None:
            print(f'--------- {prompt} -----------')
            if 'updateTruckRec' in prompt:
                self.tupdateTruckRec(prompt)
            if 'printTruckRec' in prompt:
                self.tprintTruckRec(prompt)
            if 'checkTruckRec' in prompt:
                self.tcheckTruckRec(prompt)
            if 'printOrderStatus' in prompt:
                self.tprintOrderStatus(prompt)
            if 'highFreqTrucks' in prompt:
                self.thighFreqTrucks(prompt)
            if 'maxDeliveries' in prompt:
                self.tmaxDeliveries(prompt)
            if 'availTrucks' in prompt:
                self._availTrucks(self.root)


def main():
    tree = AVLTree()
    truck_ids = [2,34,453,56,34,643,231,31,31,453,34,34,34]
    for truck in truck_ids:
        tree.treadTruckRec(truck)
    prompts = ["printTruckRec", "checkTruckRec: 31", "checkTruckRec: 542",
               "printOrderStatus: 11", "highFreqTrucks: 2", "maxDeliveries",
               "availTrucks", "updateTruckRec: 112", "updateTruckRec: 453",
               "printTruckRec"]
    for prompt in  prompts:
        tree.checkPrompt(prompt)


if __name__ == '__main__':
    main()
