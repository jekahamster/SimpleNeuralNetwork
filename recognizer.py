import numpy as np
import NeuralNetwork2 as NN


class Recognizer():
    operatorsLabel = ['+', '-', '/', '*', '']
    numbersLabel = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    def __init__(self):
        self.nNumbers = NN.NeuralNetwork()
        self.nOperators = NN.NeuralNetwork()
        self.nNumbers.loadFrom("NNNumbers.json")
        self.nOperators.loadFrom("NNOperators.json")


    def recognize(self, imgList):
        result = []

        for img in imgList:
            img = np.ravel(img)
            inputs = (np.asfarray(img) / 255 * 0.98) + 0.01
            output = self.nOperators.query(inputs)

            if self.operatorsLabel[np.argmax(output)] == "":
                output = self.nNumbers.query(inputs)
                result.append(str(np.argmax(output)))
            else:
                result.append(self.operatorsLabel[np.argmax(output)])
        return result

    def adjust(self, imgList, correctLabel):
        for i in range(len(correctLabel)):
            img = np.ravel(imgList[i])
            inputs = (np.asfarray(img) / 255 * 0.98) + 0.01

            if correctLabel[i] in self.operatorsLabel:
                operatorsTargets = np.zeros(len(self.operatorsLabel)) + 0.01
                operatorsTargets[self.operatorsLabel.index(correctLabel[i])] = 0.99
                while(np.argmax(self.nOperators.query(inputs)) != self.operatorsLabel.index(correctLabel[i])):
                    self.nOperators.train(inputs, operatorsTargets)
                    print("Oper")
            else:
                operatorsTargets = np.zeros(len(self.operatorsLabel)) + 0.01
                operatorsTargets[4] = 0.99
                self.nOperators.train(inputs, operatorsTargets)

                label = int(correctLabel[i])
                numbersTargets = np.zeros(len(self.numbersLabel)) + 0.01
                numbersTargets[label] = 0.99
                while(np.argmax(self.nNumbers.query(inputs)) != label):
                    self.nNumbers.train(inputs, numbersTargets)
                    print("Number")
        nNumbers.saveAs("NNNumbers.json")
        nOperators.saveAs("NNOperators.json")
