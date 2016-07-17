using System;
using System.Diagnostics;

namespace BinarySearch
{
    class Program
    {
        static void Main(string[] args)
        {
            var stopWatch = new Stopwatch();
            stopWatch.Start();
            var input = new int[999999];
            var randomizer = new Random(input.Length * 2);
            for (int i = 0; i < input.Length; i++)
            {
                input[i] = randomizer.Next();
            }            
            Array.Sort(input);            

            var predefinedSuccessPosition = new Random().Next(input.Length);
            PrintLine("Input array: " + string.Join(", ", input));
            Console.WriteLine("Input length: " + input.Length);
            Console.WriteLine($"Predefined position: {predefinedSuccessPosition}");
            var numberToFind = input[predefinedSuccessPosition];
            Console.WriteLine($"Number to find: {numberToFind}");            
            
            var position = DoBinarySearch(input, 0, numberToFind, 0);

            Console.WriteLine($"Result position: {position}");
            if (position == predefinedSuccessPosition)
            {
                Console.WriteLine("Succeed!");                
            }
            else
            {
                Console.WriteLine("Failed!");
            }

            stopWatch.Stop();
            Console.WriteLine($"It took: {stopWatch.Elapsed}");
            Console.WriteLine("Press any key...");
            Console.ReadKey();
        }

        private static int DoBinarySearch(int[] sortedInput, int offset, int numberToFind, int level)
        {
            Print(new string('\t', level));
            PrintLine("DoBinarySearch, offset: " + offset + "; input: " + string.Join(", ", sortedInput));
            PrintLine($"level: {level}");
            if (sortedInput.Length == 1)
            {
                return sortedInput[0] == numberToFind ? offset : -1;
            }

            var middlePosition = sortedInput.Length/2;
            var numberInMiddle = sortedInput[middlePosition];
            if (numberInMiddle > numberToFind)
            {
                var half = new int[middlePosition];
                Array.Copy(sortedInput, 0, half, 0, middlePosition);
                return DoBinarySearch(half, offset, numberToFind, level + 1);
            }

            if (numberInMiddle < numberToFind)
            {
                var half = new int[sortedInput.Length - middlePosition - 1];
                Array.Copy(sortedInput, middlePosition + 1, half, 0, sortedInput.Length - middlePosition - 1);
                return DoBinarySearch(half, offset + middlePosition + 1, numberToFind, level + 1);
            }

            return offset + middlePosition;
        }

        private static void Print(string output)
        {
            //Console.Write(output);
        }

        private static void PrintLine(string output)
        {
            //Console.WriteLine(output);
        }
    }
}
