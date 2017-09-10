def generateTuplesWithoutReturnInAscending(startNumber, maxNumber, itemsToSelect): # NOTE Can do in parallel?
    result = []    
    if itemsToSelect == 0:        
        return [()]

    subCaseStartNumberStart = startNumber
    subCaseStartNumberEnd = maxNumber + 1 - itemsToSelect + 1
    for i in range(subCaseStartNumberStart, subCaseStartNumberEnd):   
        subCollections = generateTuplesWithoutReturnInAscending(i + 1, maxNumber, itemsToSelect - 1)        
        for subCollection in subCollections:
            subCollection = (i,) + subCollection
            # subCollection.insert(0, i)
            result.append(subCollection)                
    return result

if __name__ == '__main__':
    testCases = [
        (0, 4, 2, [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]), 
        (0, 4, 3, [(0, 1, 2), (0, 1, 3), (0, 1, 4), (0, 2, 3), (0, 2, 4), (0, 3, 4), (1, 2, 3), (1, 2, 4), (1, 3, 4), (2, 3, 4)])
    ]

    for testCase in testCases:
        (startNumber, maxNumber, itemsToSelect, expectedResult) = testCase
        actualResult = generateTuplesWithoutReturnInAscending(startNumber, maxNumber, itemsToSelect)
        assert(actualResult == expectedResult)
        print('actualResult:')
        print(actualResult)

    print('before')
    generateTuplesWithoutReturnInAscending(0, 24, )
    print('end')

'''
0 1 2 3 4; itemsToSelect = 3 

0 1 2
0 1 3
0 1 4
0 2 3
0 2 4
0 3 4

1 2 3
1 2 4
1 3 4

2 3 4
'''