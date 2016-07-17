using System;
using System.IO;
using System.Linq;

namespace CountInversions
{
    class Program
    {
        static void Main(string[] args)
        {
            var paths = new[] { "mytest2" };

            foreach (var path in paths)
            {
                Console.WriteLine($"test case: {path}");
                using (var file = File.OpenText(path))
                {
                    var text = file.ReadToEnd();
                    var input = text.Split('\n').Select(int.Parse).ToArray();
                    var inversionsCount = DoCountInversions(input, 0);
                    Console.WriteLine($"Inversions count = {inversionsCount}");
                }
                Console.WriteLine("-------------------");
                Console.WriteLine();
            }            
        }

        private static int DoCountInversions(int[] input, int level)
        {
            Console.WriteLine($"level = {level}");
            var middlePosition = input.Length / 2;

            var left = new int[middlePosition];
            Array.Copy(input, 0, left, 0, left.Length);
            int leftInversionsCount;
            var leftSorted = DoCountAndSort(left, out leftInversionsCount);

            var right = new int[input.Length - left.Length];
            Array.Copy(input, middlePosition, right, 0, right.Length);
            int rightInversionsCount;
            var rightSorted = DoCountAndSort(right, out rightInversionsCount);

            var splitInversionsCount = CountSplitInversions(leftSorted, rightSorted);

            return leftInversionsCount + rightInversionsCount + splitInversionsCount;
        }

        private static int[] DoCountAndSort(int[] input, out int initialCount)
        {
            
        }
    }
}
