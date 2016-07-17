using System;
using System.IO;
using System.Linq;

namespace CountInversions
{
    class Program
    {
        static void Main(string[] args)
        {
            var paths = new[] { "mytest2.txt" };

            foreach (var path in paths)
            {
                Console.WriteLine($"test case: {path}");
                using (var file = File.OpenText(path))
                {
                    var text = file.ReadToEnd();
                    var input = text.Split('\n').Select(int.Parse).ToArray();
                    int inversionsCount;
                    SortAndCount(input, 0, out inversionsCount);
                    Console.WriteLine($"Inversions count = {inversionsCount}");
                }
                Console.WriteLine("-------------------");
                Console.WriteLine();
            }            
        }

        private static int[] SortAndCount(int[] input, int level, out int initialCount)
        {
            Console.WriteLine($"level = {level}");
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
            int leftInversionsCount;
            var leftSorted = SortAndCount(left, level + 1,  out leftInversionsCount);

            var right = new int[input.Length - left.Length];
            Array.Copy(input, middlePosition, right, 0, right.Length);
            int rightInversionsCount;
            var rightSorted = SortAndCount(right, level + 1, out rightInversionsCount);
            int splitInversionsCount;
            var fullSorted = CountSplitInversions(leftSorted, rightSorted, out splitInversionsCount);

            initialCount = (leftInversionsCount + rightInversionsCount + splitInversionsCount);
            return fullSorted;
        }

        private static int[] CountSplitInversions(int[] leftSorted, int[] rightSorted, out int splitInversionsCount)
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
                        splitInversionsCount += (leftSorted.Length - i - 1);
                        j++;
                    }
                    else
                    {
                        result[index] = rightSorted[j];
                        splitInversionsCount += (leftSorted.Length - i - 1);
                        j++;
                    }
                }
            }

            return result;
        }
    }
}
