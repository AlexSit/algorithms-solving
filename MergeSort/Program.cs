using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MergeSort
{
    internal class Program
    {
        private static void Main(string[] args)
        {            
            var length = 100;
            var input = new int[length];
            var random = new Random();
            for (int i = 0; i < input.Length - 1; i++)
            {
                input[i] = random.Next(length);
            }

            input = input.Distinct().ToArray();

            Console.WriteLine("input: " + string.Join(", ", input));
            input = MergeSort(input);

            Console.WriteLine("sorted input: " + string.Join(", ", input));

            Console.ReadKey();
        }

        private static int[] MergeSort(int[] input)
        {
            if (input.Length == 1)
                return input;

            var left = new int[input.Length / 2];
            Array.Copy(input, 0, left, 0, left.Length);
            var leftSorted = MergeSort(left);

            var right = new int[input.Length - left.Length];
            Array.Copy(input, input.Length / 2, right, 0, right.Length);
            var rightSorted = MergeSort(right);

            var result = Merge(leftSorted, rightSorted);
            return result;
        }

        private static int[] Merge(int[] leftSorted, int[] rightSorted)
        {            
            var totalLength = leftSorted.Length + rightSorted.Length;
            var result = new int[totalLength];

            var i = 0;
            var j = 0;
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
                        j++;
                    }
                }
            }

            return result;
        }
    }
}