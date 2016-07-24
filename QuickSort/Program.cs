using System;
using Common;

namespace QuickSort
{
    class Program
    {
        static void Main(string[] args)
        {
            var paths = new[]
            {
                "testcase1-first.txt",
                "testcase2-first.txt",
                "testcase3-first.txt"
            };

            var testCases = Helpers.ReadTestCasesFromInputs(paths);
            foreach (var testCase in testCases)
            {
                Console.WriteLine($"test case: {testCase.FilePath}");

                long comparisonsCount;
                var input = testCase.Input;
                QsortCountingComparisons(input, 0, 0, input.Length - 1, out comparisonsCount);
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

        private static void QsortCountingComparisons(int[] input, int level, int leftIndex, int rightIndex, out long comparisonsCount)
        {
            if (input.Length == 1)
            {
                comparisonsCount = 0;
                return;
            }

            var pivotIndex = ChooseFirstAsPivotIndex(input);

            int lessThanPivotLeftIndex;
            int lessThanPivotRightIndex;
            int moreThanPivotLeftIndex;
            int moreThanPivotRightIndex;
            PartitionAroundPivot(
                input, 
                leftIndex, 
                rightIndex, 
                pivotIndex, 
                out lessThanPivotLeftIndex, 
                out lessThanPivotRightIndex, 
                out moreThanPivotLeftIndex,
                out moreThanPivotRightIndex);            

            int leftComparisonsCount;
            int rightComparisonsCount;
            QsortCountingComparisons(input, level + 1, lessThanPivotLeftIndex, lessThanPivotRightIndex, out leftComparisonsCount);
            QsortCountingComparisons(input, level + 1, moreThanPivotLeftIndex, moreThanPivotRightIndex, out rightComparisonsCount);
            comparisonsCount = leftComparisonsCount + rightComparisonsCount;
        }

        private static void PartitionAroundPivot(
            int[] input, 
            int leftIndex, 
            int rightIndex, 
            int pivotIndex,
            out int lessThanPivotLeftIndex,
            out int lessThanPivotRightIndex,
            out int moreThanPivotLeftIndex,
            out int moreThanPivotRightIndex)
        {
            
        }

        private static int ChooseFirstAsPivotIndex(int[] input)
        {
            if (input.Length == 0)
                throw new Exception("Can't choose pivot! Array length is 0!");

            return 0;
        }
    }
}
