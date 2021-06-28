import sys

class Node(object):
    def __init__(self, Uid):
        self.UId = Uid
        self.left = None
        self.right = None
        self.height = 0
        self.chkoutCtr = 0


class AVLTree(object):
    def __init__(self):
        self.root = None
        self.max_count = None
        self.count = 0

    def height(self, node):
        if node is None:
            return -1
        else:
            return node.height

    # left left
    def singleLeftRotate(self, node):
        k1 = node.left
        node.left = k1.right
        k1.right = node
        node.height = max(self.height(node.right), self.height(node.left)) + 1
        k1.height = max(self.height(k1.left), node.height) + 1
        return k1

    # right right
    def singleRightRotate(self, node):
        k1 = node.right
        node.right = k1.left
        k1.left = node
        node.height = max(self.height(node.right), self.height(node.left)) + 1
        k1.height = max(self.height(k1.right), node.height) + 1
        return k1

    # right left
    def doubleLeftRotate(self, node):
        node.left = self.singleRightRotate(node.left)
        return self.singleLeftRotate(node)

    # left right
    def doubleRightRotate(self, node):
        node.right = self.singleLeftRotate(node.right)
        return self.singleRightRotate(node)

    def triggerReadTruckRec(self, key):
        if not self.root:
            if self.max_count is None:
                self.max_count = key
            else:
                self.root = Node(key)
        else:
            self.root = self._readTruckRec(self.root, key)

    def _readTruckRec(self, tNode, Uid):
        if tNode is None:
            tNode = Node(Uid)
        elif Uid < tNode.UId:
            tNode.left = self._readTruckRec(tNode.left, Uid)
            if (self.height(tNode.left) - self.height(tNode.right)) == 2:
                if Uid < tNode.left.UId:
                    tNode = self.singleLeftRotate(tNode)
                else:
                    tNode = self.doubleLeftRotate(tNode)

        elif Uid > tNode.UId:
            tNode.right = self._readTruckRec(tNode.right, Uid)
            if (self.height(tNode.right) - self.height(tNode.left)) == 2:
                if Uid < tNode.right.UId:
                    tNode = self.doubleRightRotate(tNode)
                else:
                    tNode = self.singleRightRotate(tNode)
        else:
            tNode.chkoutCtr += 1
            if tNode.chkoutCtr > 2 * self.max_count:
                print(f'vehicle id {Uid} no longer available for service')
        tNode.height = max(self.height(tNode.right), self.height(tNode.left)) + 1
        return tNode

    def traverse(self, root):
        if root is not None:
            self.traverse(root.left)
            if root.chkoutCtr > self.max_count:
                print(root.UId)
            self.traverse(root.right)

    def inorder(self, node):
        if node:
            self.inorder(node.left)
            print(node.UId, ", ", node.chkoutCtr)
            self.inorder(node.right)

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
            if result:
                if result[1] == -1:
                    print(f'Vehicle id {result[0]} did not come to the warehouse today')
                else:
                    if result[2] == 0:
                        print(f'Vehicle id {result[0]} just reached the warehouse')
                    if result[2] % 2 == 0 and result[2] != 0:
                        print(f'Vehicle id {result[0]} entered {result[2]} times into the system. '
                              f'It just completed an order')
                    if result[2] % 2 != 0 and result[2] != 0:
                        print(f'Vehicle id {result[0]} entered {result[2]} times into the system. '
                              f'It is currently fulfilling an open order')
                print('------------------------------------')

    def searchTree(self, root, key):
        """
        binary search function
        :param root: root node of the tree
        :param key: key to be searched in the tree
        :return: Truck ID, status, chkoutCtr
        """
        if root:
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
        else:
            return

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
        if balance < 0:
            balance = 0
        print(f'Open Orders: {open_order_count}')
        print(f'Closed Orders: {close_order_count}')
        print(f'Yet to be fulfilled: {balance}')
        print('------------------------------------')

    def getList(self, root):
        if not root:
            return
        yield from self.getList(root.left)
        yield root.UId, root.chkoutCtr
        yield from self.getList(root.right)

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
        result = list(self.getList(tNode))
        tree = [i for i in result if i[1] > frequency]
        if len(tree) == 0:
            print('No such vehicle present in the system')
        else:
            for x in tree:
                if x[1] > frequency:
                    print(', '.join(map(str, x)))
        print('------------------------------------')


    def _maxDeliveries(self, tNode):
        print(f'maxDeliveries: {self.max_count}')
        result = list(self.getList(tNode))
        tree = [i for i in result if i[1] >= 2*self.max_count]
        print(f'{len(tree)} Vehicle Ids did their maximum deliveries:')
        self.traverse(tNode)

        print('------------------------------------')

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

    def searchTreeRecord(self, root):
        if root is None:
            return
        else:
            self.searchTreeRecord(root.left)
            if (root.chkoutCtr % 2 == 0 and root.chkoutCtr < 2*self.max_count) or root.chkoutCtr == 0:
                print(root.UId)
            self.searchTreeRecord(root.right)

    def _availTrucks(self, tNode):
        # self.countAvailTruck(tNode)
        print(f'Vehicle Ids that are currently available to deliver supplies:')
        self.searchTreeRecord(tNode)
        print('------------------------------------')

    # mapping tagname with respective functions
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
                self._maxDeliveries(self.root)
            if 'availTrucks' in prompt:
                self._availTrucks(self.root)


def main():
    myTree = AVLTree()
    def readfile(file):
        """ function to read the input files
        :param file: input files(inputPS2.txt, promptsPS2.txt)
        :return: list data
        """
        with open(file, 'r') as f:
            data = f.read().splitlines()
        return data

    input_file = "inputPS2.txt"
    promp_file = "promptsPS2.txt"
    input_data = readfile(input_file)
    truck_ids = list(map(int, input_data))
    prompts = readfile(promp_file)
    truck_ids = [1, 34, 453, 56, 34, 643, 231, 31, 31, 453, 34, 34, 34]
    sys.stdout = open("outputsPS2.txt", "w")
    if len(truck_ids) > 1:
        for num in truck_ids:
            myTree.triggerReadTruckRec(num)
    elif len(truck_ids) == 1:
        print('Only max Delivery is present')
    else:
        print('Tree is empty!')
    prompts = ["printTruckRec", "checkTruckRec: 31", "checkTruckRec: 542",
                   "printOrderStatus: 11", "highFreqTrucks: 2", "maxDeliveries",
                   "availTrucks", "updateTruckRec: 112", "updateTruckRec: 453",
                   "printTruckRec", "highFreqTrucks: 10", "maxDeliveries","checkTruckRec: 643"]

    for prompt in prompts:
        myTree.checkPrompt(prompt)
    sys.stdout.close()



if __name__ == '__main__':
    main()