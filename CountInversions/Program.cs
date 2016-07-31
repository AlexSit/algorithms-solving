using System;
using Common;

namespace CountInversions
{
    class Program
    {
        static void Main(string[] args)
        {
            //var paths = new[]
            //{
            //    "mytest2.txt",
            //    "mytest.txt",
            //    "pa-cases-1.txt",
            //    "pa-cases-2.txt",
            //    "pa-cases-3.txt",
            //    "pa-cases-4.txt",
            //    "pa-cases-5.txt",
            //    "pa-cases-6.txt",
            //    "pa-cases-7.txt"
            //};

            var paths = new[]
            {
                "input-week1.txt"
            };
            

            var testCases = Helpers.ReadTestCasesFromInputs(paths);

            foreach (var testCase in testCases)
            {
                Console.WriteLine($"test case: {testCase.FilePath}");

                long inversionsCount;
                SortAndCount(testCase.Input, 0, out inversionsCount);
                Console.WriteLine($"Expected: {testCase.Answer}, Actual: {inversionsCount}");
                if (testCase.Answer != inversionsCount && testCase.Answer != -1)
                {
                    throw new Exception($"Test case {testCase.FilePath} failed!");
                }
                Console.WriteLine("-------------------");
                Console.WriteLine();
            }

            Console.WriteLine("the end");
            Console.ReadKey();
        }        
        
        private static int[] SortAndCount(int[] input, int level, out long initialCount)
        {
            //Console.WriteLine($"level = {level}");
            if (input.Length == 1)
            {
                initialCount = 0;
                return input;
            }

            if (input.Length == 2)
            {
                if (input[0] > input[1])
                {
                    initialCount = 1;
                    var swap = input[0];
                    input[0] = input[1];
                    input[1] = swap;
                }
                else
                {
                    initialCount = 0;
                }
                return input;
            }

            var middlePosition = input.Length / 2;

            var left = new int[middlePosition];
            Array.Copy(input, 0, left, 0, left.Length);
            long leftInversionsCount;
            var leftSorted = SortAndCount(left, level + 1,  out leftInversionsCount);

            var right = new int[input.Length - left.Length];
            Array.Copy(input, middlePosition, right, 0, right.Length);
            long rightInversionsCount;
            var rightSorted = SortAndCount(right, level + 1, out rightInversionsCount);
            long splitInversionsCount;
            var fullSorted = CountSplitInversions(leftSorted, rightSorted, out splitInversionsCount);

            initialCount = (leftInversionsCount + rightInversionsCount + splitInversionsCount);
            return fullSorted;
        }

        private static int[] CountSplitInversions(int[] leftSorted, int[] rightSorted, out long splitInversionsCount)
        {
            var totalLength = leftSorted.Length + rightSorted.Length;
            var result = new int[totalLength];

            var i = 0;
            var j = 0;
            splitInversionsCount = 0;

            for (int index = 0; index < totalLength; index++)
            {
                if (j >= rightSorted.Length)
                {
                    result[index] = leftSorted[i];
                    i++;
                }
                else if (i >= leftSorted.Length)
                {
                    result[index] = rightSorted[j];
                    j++;
                }
                else
                {
                    if (leftSorted[i] < rightSorted[j])
                    {
                        result[index] = leftSorted[i];
                        i++;
                    }
                    else if (leftSorted[i] > rightSorted[j])
                    {
                        result[index] = rightSorted[j];
                        splitInversionsCount += (leftSorted.Length - i);
                        j++;
                    }
                    else
                    {
                        result[index] = rightSorted[j];
                        splitInversionsCount += (leftSorted.Length - i);
                        j++;
                    }
                }
            }

            return result;
        }
    }
}
