using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace Median
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("START START START");
            var basePath = "../../inputs";
            var paths = new List<string>
            {                
                "tc1.txt",                
                //"median.txt"
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

        private static int ReadInputAndSolve(string text)
        {
            var lines = text.Split('\n').Where(x => !string.IsNullOrWhiteSpace(x)).ToList();
            var linesCount = lines.Count;

            var m = new int[linesCount];
            var heap = new Heap();
            for (var i = 0; i < linesCount; i++)
            {
                var number = int.Parse(lines[i]);
                heap.Add(number);
                var mk = heap.GetMedian();
                m[i] = mk;
            }

            var medianSum = m.Aggregate(0, (i, i1) => i + i1);
            var answer = medianSum%10000;
            return answer;
        }        
    }

    internal class Heap
    {
        private readonly SortedDictionary<int, bool>  _sortedDictionary = new SortedDictionary<int, bool>();

        public void Add(int number)
        {
            _sortedDictionary.Add(number, true);
        }

        public int GetMedian()
        {
            var count = _sortedDictionary.Count;
            var medianPosition = count%2 == 0 ? count/2 - 1 : count/2;
            return _sortedDictionary.ElementAt(medianPosition).Key;
        }
    }
}
