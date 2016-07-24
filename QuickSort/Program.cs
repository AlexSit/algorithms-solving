using System;
using Common;

namespace QuickSort
{
    class Program
    {
        static void Main(string[] args)
        {
            //var paths = new[]
            //{
            //    "testcase1-first.txt",
            //    "testcase2-first.txt",
            //    "testcase3-first.txt"
            //};
            //var pivotType = PivotTypes.First;


            //var paths = new[]
            //{
            //    "testcase1-last.txt",
            //    "testcase2-last.txt",
            //    "testcase3-last.txt"
            //};
            //var pivotType = PivotTypes.Last;

            //var paths = new[]
            //{
            //    "testcase1-median.txt",
            //    "testcase2-median.txt",
            //    "testcase3-median.txt"
            //};
            //var pivotType = PivotTypes.Median;

            var paths = new[]
            {
                "input_QuickSort.txt"
            };
            //var pivotType = PivotTypes.First;
            //var pivotType = PivotTypes.Last;
            var pivotType = PivotTypes.Median;

            var testCases = Helpers.ReadTestCasesFromInputs(paths);
            foreach (var testCase in testCases)
            {
                Console.WriteLine($"test case: {testCase.FilePath}");

                long comparisonsCount;
                var input = testCase.Input;
                QsortCountingComparisons(input, pivotType, 0, 0, input.Length - 1, out comparisonsCount);
                Console.WriteLine($"Expected: {testCase.InversionsCount}, Actual: {comparisonsCount}");
                if (testCase.InversionsCount != comparisonsCount && testCase.InversionsCount != -1)
                {
                    throw new Exception($"Test case {testCase.FilePath} failed!");
                }
                Console.WriteLine("-------------------");
                Console.WriteLine();
            }

            Console.WriteLine("the end");
            Console.ReadKey();
        }

        private static void QsortCountingComparisons(int[] input, PivotTypes pivotType, int level, int leftIndex, int rightIndex, out long comparisonsCount)
        {
            if (rightIndex - leftIndex == 0)
            {
                comparisonsCount = 0;
                return;
            }

            int pivotIndex;
            switch (pivotType)
            {
                case PivotTypes.First:
                    pivotIndex = QsortHelpers.ChooseFirstAsPivotIndex(leftIndex, rightIndex);
                    break;
                case PivotTypes.Last:
                    pivotIndex = QsortHelpers.ChooseLastAsPivotIndex(leftIndex, rightIndex);
                    break;
                case PivotTypes.Median:
                    pivotIndex = QsortHelpers.ChooseMedianAsPivotIndex(input, leftIndex, rightIndex);
                    break;
                default:
                    throw new NotImplementedException();
            }

            long currentComparisonsCount;
            int lessThanPivotLeftIndex;
            int lessThanPivotRightIndex;
            int moreThanPivotLeftIndex;
            int moreThanPivotRightIndex;
            PartitionAroundPivot(
                input, 
                leftIndex, 
                rightIndex, 
                pivotIndex, 
                out currentComparisonsCount,
                out lessThanPivotLeftIndex, 
                out lessThanPivotRightIndex, 
                out moreThanPivotLeftIndex,
                out moreThanPivotRightIndex);            

            long leftComparisonsCount = 0;
            long rightComparisonsCount = 0;
            if (lessThanPivotLeftIndex != -1 && lessThanPivotRightIndex != -1)
            {
                QsortCountingComparisons(input, pivotType, level + 1, lessThanPivotLeftIndex, lessThanPivotRightIndex,
                    out leftComparisonsCount);
            }
            if (moreThanPivotLeftIndex != -1 && moreThanPivotRightIndex != -1)
            {
                QsortCountingComparisons(input, pivotType, level + 1, moreThanPivotLeftIndex, moreThanPivotRightIndex,
                    out rightComparisonsCount);
            }
            comparisonsCount = currentComparisonsCount + leftComparisonsCount + rightComparisonsCount;
        }                

        private static void PartitionAroundPivot(
            int[] input, 
            int leftIndex, 
            int rightIndex, 
            int pivotIndex,
            out long currentComparisonsCount,
            out int lessThanPivotLeftIndex,
            out int lessThanPivotRightIndex,
            out int moreThanPivotLeftIndex,
            out int moreThanPivotRightIndex)
        {            
            if (pivotIndex < leftIndex || rightIndex < pivotIndex)
                throw new Exception("Wrong pivot index");

            if (pivotIndex != leftIndex)
            {
                SwapArrayElements(input, pivotIndex, leftIndex);
                pivotIndex = leftIndex;
            }

            var startIndex = pivotIndex == leftIndex ? leftIndex + 1 : leftIndex;
            var i = startIndex;
            var pivot = input[pivotIndex];
            for (var j = startIndex; j <= rightIndex; j++)
            {                
                if (input[j] < pivot)
                {                    
                    SwapArrayElements(input, j, i);
                    i++;
                }
            }
            if (pivot > input[i - 1])
            {
                SwapArrayElements(input, pivotIndex, i - 1);
                pivotIndex = i - 1;
            }

            lessThanPivotLeftIndex = leftIndex == pivotIndex ? -1 : leftIndex;
            lessThanPivotRightIndex = leftIndex == pivotIndex ? -1 : pivotIndex - 1;
            moreThanPivotLeftIndex = rightIndex == pivotIndex ? -1 : pivotIndex + 1;
            moreThanPivotRightIndex = rightIndex == pivotIndex ? -1 : rightIndex;

            currentComparisonsCount = rightIndex - leftIndex;
        }

        private static void SwapArrayElements(int[] input, int elementIndex1, int elementIndex2)
        {
            int temp = input[elementIndex1];
            input[elementIndex1] = input[elementIndex2];
            input[elementIndex2] = temp;
        }        
    }
}
