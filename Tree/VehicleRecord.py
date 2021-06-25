import sys


class TruckNode:
    def __init__(self, Uid):
        self.UId = Uid
        self.chkoutCtr = 0
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None
        self.max_count = None
        self.count = 0

    def countTrucks(self, root):
        """
        helper function to count the total trucks
        :param root:
        :return: count
        """
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
            print(root.UId, ", ", root.chkoutCtr)
            self.inorder(root.right)

    def searchTree(self, root, key):
        """
        binary search function
        :param root: root node of the tree
        :param key: key to be searched in the tree
        :return: Truck ID, status, chkoutCtr
        """
        if root.UId == key:
            return root.UId, 2, root.chkoutCtr
        if root.UId < key:
            if root.right is None:
                return key, -1, root.chkoutCtr
            return self.searchTree(root.right, key)
        if root.UId > key:
            if root.left is None:
                return key, -1, root.chkoutCtr
            return self.searchTree(root.left, key)

    def getList(self, root):
        if not root:
            return
        yield from self.getList(root.left)
        yield root.UId, root.chkoutCtr
        yield from self.getList(root.right)

    def searchTreeRecord(self, root):
        # print(printCount)
        if root is None:
            return
        else:
            self.searchTreeRecord(root.left)
            if (root.chkoutCtr % 2 == 0 and root.chkoutCtr < 2 * self.max_count) or root.chkoutCtr == 0:
                print(root.UId)
            self.searchTreeRecord(root.right)

    def countAvailTruck(self, root):
        try:
            if root is None:
                return 0
            else:
                self.countAvailTruck(root.left)
                if (root.chkoutCtr % 2 == 0 and root.chkoutCtr < 2 * self.max_count) or root.chkoutCtr == 0:
                    self.count += 1
                self.countAvailTruck(root.right)
        except Exception as e:
            print(str(e))

    def getHeight(self, current):
        if current is None:
            return 0
        else:
            return current.height

    def getBalance(self, current):
        if current is None:
            return 0
        else:
            return self.getHeight(current.left) - self.getHeight(current.right)

    def rotateRight(self, current):
        y = current.left
        temp = y.right

        y.right = current
        current.left = temp

        current.height = max(self.getHeight(current.left), self.getHeight(current.right)) + 1
        y.height = max(self.getHeight(y.left), self.getHeight(y.right)) + 1
        return y

    def rotateLeft(self, current):
        y = current.right
        temp = y.left
        y.left = current
        current.right = temp
        current.height = max(self.getHeight(current.left), self.getHeight(current.right)) + 1
        y.height = max(self.getHeight(y.left), self.getHeight(y.right)) + 1
        return y

    def triggerReadTruckRec(self, value):
        """
        trigger function for _readTruckRec
        :param value: truck_id from inputPS2.txt
        :return: assign max delivery value
        """
        if self.root is None:
            if self.max_count is None:
                self.max_count = value
                # print('Assigning the maximum deliveries :', value)
            else:
                self.root = TruckNode(value)
                # print('setting root node - {}, counter - {}'.format(value, self.root.chkoutCtr))
        else:
            self._readTruckRec(self.root, value)

    def _readTruckRec(self, tNode, Uid):
        """
        create tree from the truck_ids, update chkoutCtr
        :param tNode: root node of the tree
        :param Uid: truck_id to be inserted
        :return: increment chkoutCtr for every subsequent occurrence of that truck
        """
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
            # print('Value {} already inserted, counter - {}'.format(Uid, tNode.chkoutCtr))
            tNode.chkoutCtr += 1
            if tNode.chkoutCtr > 2 * self.max_count:
                print(f'vehicle id {Uid} no longer available for service')
        tNode.height = max(self.getHeight(tNode.left), self.getHeight(tNode.right)) + 1
        balance = self.getBalance(tNode)
        # left left
        if balance > 1 and Uid < tNode.left.UId:
            return self.rotateRight(tNode)
        # right right
        if balance < -1 and Uid > tNode.right.UId:
            return self.rotateLeft(tNode)
        # left right
        if balance > 1 and Uid > tNode.left.UId:
            tNode.left = self.rotateLeft(tNode.left)
            return self.rotateRight(tNode)
        # right left
        if balance < -1 and Uid < tNode.right.UId:
            tNode.right = self.rotateRight(tNode.right)
            return self.rotateLeft(tNode)
        return tNode

    def triggerUpdateTruckRec(self, prompt):
        """
        function to read Truck ID and trigger _updateTruckRec
        :param prompt: updateTruckRec
        :return: None
        """
        if prompt is not None:
            split_prompt = prompt.split(':')
            truck_id = int(split_prompt[1].lstrip())
            self._updateTruckRec(self.root, truck_id)

    def _updateTruckRec(self, tNode, Uid):
        """
         function to update the existing system with IDs
         entering and leaving the warehouse from the promptsPS2.txt file
        :param tNode: root node of the tree
        :param Uid: Truck ID to be updated in the system
        :return: increment chkoutCtr
        """
        if type(Uid) == int:
            self._readTruckRec(tNode, Uid)
            print(f'Vehicle Id {Uid} record updated')
            print('------------------------------------')

    def _printTruckRec(self, tNode):
        """
        function to count the total number of vehicles that came to the warehouse
        :param tNode: root node of the tree
        :return: outputPS2.txt
        """
        count = self.countTrucks(tNode)
        print(f'Total number of vehicles entered in the warehouse: {count}')
        self.inorder(tNode)
        print('------------------------------------')

    def triggerCheckTruckRec(self, prompt):
        """
        function to read Truck ID and trigger _checkTruckRec
        :param prompt: checkTruckRec
        :return: None
        """
        if prompt is not None:
            split_prompt = prompt.split(':')
            truck_id = int(split_prompt[1].lstrip())
            self._checkTruckRec(self.root, truck_id)

    def _checkTruckRec(self, tNode, Uid):
        """
        function to check the status of the Truck ID
        :param tNode: root node of the tree
        :param Uid: Truck ID to be searched in the tree
        :return: outputPS2.txt
        """
        if type(Uid) == int:
            result = self.searchTree(tNode, Uid)
            if result[1] == -1:
                print(f'Vehicle id {result[0]} did not come to the warehouse today')
            else:
                if result[1] == 0:
                    print(f'Vehicle id {result[0]} just reached the warehouse')
                if result[1] % 2 == 0:
                    print(f'Vehicle id {result[0]} entered {result[2]} times into the system. '
                          f'It just completed an order')
                if result[1] % 2 != 0:
                    print(f'Vehicle id {result[0]} entered {result[2]} times into the system. '
                          f'It is currently fulfilling an open order')
            print('------------------------------------')

    def triggerPrintOrderStatus(self, prompt):
        """
        function to read Orders and trigger _printOrderStatus
        :param prompt: printOrderStatus
        :return: None
        """
        if prompt is not None:
            split_prompt = prompt.split(':')
            truck_id = int(split_prompt[1].lstrip())
            print(f'The following status of {truck_id} orders:')
            self._printOrderStatus(truck_id)

    def _printOrderStatus(self, targetorders):
        """
        function to get the number of open, closed and yet to be fulfilled orders
        :param targetorders: Target Order count for the day
        :return: outputPS2.txt
        """
        result = list(self.getList(self.root))
        open_order = filter(lambda y: (y[1] % 2) != 0, result)
        close_order = filter(lambda y: ((y[1] % 2) == 0 and y[1] != 0), result)
        open = list(open_order)
        close = list(close_order)
        close_order_count = 0
        for x in close:
            result = x[1] // 2
            close_order_count += result
        open_order_count = 0
        for x in open:
            result = x[1] + 1 // 2
            open_order_count += result
        balance = targetorders - (open_order_count + close_order_count)
        print(f'Open Orders: {open_order_count}')
        print(f'Closed Orders: {close_order_count}')
        print(f'Yet to be fulfilled: {balance}')
        print('------------------------------------')

    def triggerHighFreqTrucks(self, prompt):
        """
        function to read limit and trigger _highFreqTrucks
        :param prompt: highFreqTrucks
        :return: None
        """
        if prompt is not None:
            split_prompt = prompt.split(':')
            frequency = int(split_prompt[1].lstrip())
            print(f'Vehicles that moved in/out more than {frequency} times are:')
            self._highFreqTrucks(self.root, frequency)

    def _highFreqTrucks(self, tNode, frequency):
        """
        function to generate the list of vehicles
        that have moved in/out of the warehouse more than ‘z’ number of times
        :param tNode: root node of the tree
        :param frequency: frequency limit (z)
        :return: Truck ID, counter
        """
        tree = list(self.getList(tNode))
        if len(tree) == 0:
            print('No such vehicle present in the system')
        else:
            for x in tree:
                if x[1] > frequency:
                    # print(x)
                    print(', '.join(map(str, x)))
        print('------------------------------------')

    def tmaxDeliveries(self, prompt):
        self._maxDeliveries(self.root)

    def traverse(self, root):
        if root is not None:
            self.traverse(root.left)
            if root.chkoutCtr > self.max_count:
                print(root.UId)
            self.traverse(root.right)

    def _maxDeliveries(self, tNode):
        print(f'maxDeliveries: {self.max_count}')
        tree = list(self.getList(tNode))
        count = []
        for x in tree:
            if x[1] >= 2 * self.max_count:
                count.append(x)
        print(f'{len(count)} Vehicle Ids did their maximum deliveries:')
        self.traverse(tNode)

        print('------------------------------------')

    # def tavailTrucks(self, prompt):
    #     self._availTrucks(self.root)

    def _availTrucks(self, tNode):
        self.countAvailTruck(tNode)
        print(f'{self.count} Vehicle Ids that are currently available to deliver supplies:')
        self.searchTreeRecord(tNode)
        print('------------------------------------')

    def checkPrompt(self, prompt):
        if prompt is not None:
            print(f'--------- {prompt} -----------')
            if 'updateTruckRec' in prompt:
                self.triggerUpdateTruckRec(prompt)
            if 'printTruckRec' in prompt:
                self._printTruckRec(self.root)
            if 'checkTruckRec' in prompt:
                self.triggerCheckTruckRec(prompt)
            if 'printOrderStatus' in prompt:
                self.triggerPrintOrderStatus(prompt)
            if 'highFreqTrucks' in prompt:
                self.triggerHighFreqTrucks(prompt)
            if 'maxDeliveries' in prompt:
                self.tmaxDeliveries(prompt)
            if 'availTrucks' in prompt:
                self._availTrucks(self.root)


def main():
    tree = AVLTree()

    def readfile(file):
        """ function to read the input files
        :param file: input files(inputPS2.txt, promptsPS2.txt)
        :return: list data
        """
        with open(file, 'r') as f:
            data = f.read().splitlines()
        return data

    # input_file = 'inputPS2.txt'
    # promp_file = 'promptsPS2.txt'
    # input_data = readfile(input_file)
    # truck_ids = list(map(int, input_data))
    # prompts = readfile(promp_file)
    truck_ids = [2, 34, 453, 56, 34, 643, 231, 31, 31, 453, 34, 34, 34]
    for truck in truck_ids:
        print(truck)
        tree.triggerReadTruckRec(truck)
    sys.stdout = open("outputsPS2.txt", "w")
    prompts = ["printTruckRec", "checkTruckRec: 31", "checkTruckRec: 542",
               "printOrderStatus: 11", "highFreqTrucks: 2", "maxDeliveries",
               "availTrucks", "updateTruckRec: 112", "updateTruckRec: 453",
               "printTruckRec", "highFreqTrucks: 2", "maxDeliveries"]
    for prompt in prompts:
        tree.checkPrompt(prompt)
    sys.stdout.close()


if __name__ == '__main__':
    main()
