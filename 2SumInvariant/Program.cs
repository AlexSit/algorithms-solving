using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace _2SumInvariant
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("START START START");
            var basePath = "../../inputs";
            var paths = new List<string>
            {                
                //"tc1.txt",
                //"tc2.txt",
                "2sum.txt"
            };

            foreach (var path in paths)
            {
                using (var file = File.OpenText(Path.Combine(basePath, path)))
                {
                    var text = file.ReadToEnd();
                    var answer = ReadInputAndSolve(text);

                    //var answer = GetAnswer(input);

                    Console.WriteLine($"Actual ANSWER: {answer}");
                }
            }
            Console.WriteLine("the end");
            Console.ReadKey();
        }
        
        private static long ReadInputAndSolve(string text)
        {
            var sums = new List<long>();

            const int minT = -10000;
            const int maxT = 10000;

            for (long i = minT; i <= maxT; i++)
            {
                sums.Add(i);
            }

            long currentSumCount = 0;

            var inputHashtable = new Hashtable();
            var inputList = text
                .Split('\n')
                .Where(x => !string.IsNullOrWhiteSpace(x))
                .Select(long.Parse)
                .Distinct()
                .ToList();
            inputList.Sort();
            
            var min = inputList.Min();
            var max = inputList.Max();
            long? maxLimit;
            long? minLimit;
            DefineLimits(min, max, maxT, minT, out maxLimit, out minLimit);

            if (minLimit.HasValue || maxLimit.HasValue)
            {
                inputList = TruncateInputList(inputList, minLimit, maxLimit);
            }                

            var inputListCount = inputList.Count;
            for (var inputIndex = 0; inputIndex < inputListCount; inputIndex++)
            {
                var inputItem = inputList[inputIndex];
                inputHashtable.Add(inputItem, true);                

                currentSumCount += CheckSumCriteria(inputHashtable, inputItem, ref sums);                
            }

            return currentSumCount;
        }

        private static List<long> TruncateInputList(List<long> inputList, long? minLimit, long? maxLimit)
        {
            if (minLimit.HasValue)
            {
                return inputList.Where(x => x >= minLimit.Value).ToList();
            }
            else if (maxLimit.HasValue)
            {
                return inputList.Where(x => x <= maxLimit.Value).ToList();
            }

            return inputList;
        }

        /// <summary>
        /// Если возможно, сокращает границы входного массива на основании того, что не все элементы дадут сумму в нужных границах.
        /// </summary>
        /// <param name="min">Минимум во входном массиве</param>
        /// <param name="max">Максимум во входном массиве</param>
        /// <param name="maxT">Максимально возможная сумма (верхняя граница)</param>
        /// <param name="minT">Минимально возможная сумма (нижняя граница)</param>
        /// <param name="maxLimit">Результат: максимальное значение во входном массиве, дальше которого искать элементы суммы бесполезно</param>
        /// <param name="minLimit">Результат: минимальное значение во входном массиве, раньше которого искать элементы суммы бесполезно</param>
        private static void DefineLimits(long min, long max, int maxT, int minT, out long? maxLimit, out long? minLimit)
        {            
            maxLimit = null;
            minLimit = null;
            
            if (min + max > maxT)
            {
                maxLimit = maxT - min;
            }
            else if (min + max < minT)
            {
                minLimit = minT - max;
            }
        }

        private static long CheckSumCriteria(Hashtable input, long inputItem, ref List<long> sums)
        {
            long foundSumCount = 0;            
            var count = sums.Count;
            for (int sumIndex = 0; sumIndex < count; sumIndex++)
            {                                
                var t = sums[sumIndex];

                var y = (t - inputItem);                
                if (inputItem != y && input[y] != null)
                {
                    //Console.WriteLine($"{inputItem} + {y} = {t}");
                    sums.Remove(t);
                    count--;
                    sumIndex--;
                    foundSumCount++;
                }                
            }

            return foundSumCount;
        }
    }
}
