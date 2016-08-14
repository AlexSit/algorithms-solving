using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SccIdeas
{
    class Program
    {
        static void Main(string[] args)
        {
            List<Tuple<int, int, bool>> input;            
            using (var file = File.OpenText("input.txt"))
            {
                var text = file.ReadToEnd();                
                int[] answer;
                ProcessTestCaseText(text, out input, out answer);                
            }
            var convertedInput = PrepareInput(input);

            var findables = input.Skip(input.Count / 2).Take(100).Select(x=>x.Item1).Distinct().ToList();
            foreach (var findable in findables)
            {
                var s1 = new Stopwatch();
                s1.Start();
                var list = input.Where(x => x.Item2 == findable).ToList();
                s1.Stop();
                Console.WriteLine("1: " + s1.Elapsed);

                var s2 = new Stopwatch();
                s2.Start();
                var list2 = convertedInput.Where(x => x.DestinationNodes.Contains(findable)).ToList();
                s2.Stop();
                Console.WriteLine("2: " + s2.Elapsed);
                Console.WriteLine("--------------------");
            }

            Console.WriteLine("Finish");
            Console.ReadKey();
        }

        private static void ProcessTestCaseText(string text, out List<Tuple<int, int, bool>> input, out int[] answer)
        {
            var lines = text.Split('\n')
                .Where(x => !string.IsNullOrWhiteSpace(x))
                .ToList();

            answer = null;
            input = new List<Tuple<int, int, bool>>();

            for (int i = 0; i < lines.Count; i++)
            {
                if (lines[i].ToLower().Contains("ans"))
                {
                    var answerString = lines[i].Split(':', '-')[1];
                    answer = answerString.Split(',').Select(int.Parse).ToArray();
                    return;
                }

                input.Add(ProcessLine(lines[i]));
            }
        }

        private static Tuple<int, int, bool> ProcessLine(string line)
        {
            var numbers = line
                .Split(' ')
                .Where(x => !string.IsNullOrWhiteSpace(x))
                .Select(x => int.Parse(x.Trim()))
                .ToList();

            return new Tuple<int, int, bool>(numbers[0], numbers[1], false);
        }

        private static List<NodeInfo> PrepareInput(List<Tuple<int, int, bool>> input)
        {            
            var convertedInput = input.GroupBy(x => x.Item1, x => x.Item2, (key, values) => new NodeInfo
            {
                I = key,
                Explored = false,
                DestinationNodes = values.ToArray()
            })
            .ToList();
            
            var count = convertedInput.Count;
            for (int i = 0; i < count; i++)
            {
                if (convertedInput[i].I != i + 1)
                {
                    convertedInput.Insert(i, new NodeInfo
                    {
                        I = i + 1,
                        Explored = false,
                        DestinationNodes = new int[0]
                    });
                    count++;
                }
            }
            
            return convertedInput.OrderBy(x => x.I).ToList();
        }
    }

    class NodeInfo
    {
        public int I { get; set; }
        public bool Explored { get; set; }
        public int[] DestinationNodes { get; set; }
    }
}
