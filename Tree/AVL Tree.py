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

    def tprintOrderStatus(self, prompt):
        print('tprintOrderStatus')

    def _printOrderStatus(self, targetorders):
        return

    def thighFreqTrucks(self, prompt):
        print('thighFreqTrucks')

    def _highFreqTrucks(self, tNode, frequency):
        return

    def tmaxDeliveries(self, prompt):
        print('tmaxDeliveries')

    def _maxDeliveries(self, tNode):
        return

    def tavailTrucks(self, prompt):
        print('tmaxDeliveries')

    def _availTrucks(self, tNode):
        return

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
                self.tavailTrucks(prompt)


def main():
    tree = AVLTree()
    truck_ids = [2,34,453,56,34,643,231,31,31,453,34,34,34]
    for truck in truck_ids:
        # print(truck)
        tree.treadTruckRec(truck)
    prompts = ["printTruckRec", "checkTruckRec: 31", "checkTruckRec: 542",
               "printOrderStatus: 11", "highFreqTrucks: 2", "maxDeliveries",
               "availTrucks", "updateTruckRec: 112", "updateTruckRec: 453",
               "printTruckRec"]
    # prompts = ["checkTruckRec: 21","checkTruckRec: 20","checkTruckRec: 30",
    #            "checkTruckRec: 10"]
    for prompt in  prompts:
        # print(prompt)
        tree.checkPrompt(prompt)


if __name__ == '__main__':
    main()
