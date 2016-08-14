using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;

namespace SCC
{
    class Program
    {
        private static int _t;
        private static Dictionary<int, int> _finishingTimes = new Dictionary<int, int>();
        private static int _currentLeaderNumber;
        private static Dictionary<int, List<int>> _leaders = new Dictionary<int, List<int>>();

        private static Dictionary<int, NodeInfo> _convertedInput;
                
        private static int[] _answer = new int[5];

        static void Main(string[] args){
            var stackSize = 100 * 1000 * 1000;
            var thread = new Thread(Target, stackSize);
            thread.Start();
            thread.Join();
        }

        private static void Target()
        {
            Console.WriteLine("START START START");
            var basePath = "../../inputs";
            var paths = new List<string>
            {                
                //"tc1.txt",
                //"tc2.txt",
                //"tc3.txt",
                //"tc4.txt",
                "input.txt"
            };

            var testCases = new List<TestCase>();

            foreach (var path in paths)
            {
                using (var file = File.OpenText(Path.Combine(basePath, path)))
                {
                    var text = file.ReadToEnd();

                    List<Tuple<int, int>> input;
                    int[] answer;
                    ProcessTestCaseText(text, out input, out answer);

                    testCases.Add(
                        new TestCase
                        {
                            FilePath = path,
                            Input = input,
                            Answer = answer
                        }
                    );
                }
            }
            foreach (var testCase in testCases)
            {
                AssertTestCase(testCase);
            }

            Console.WriteLine("the end");
            Console.ReadKey();
        }

        private static void AssertTestCase(TestCase testCase)
        {
            ResetInputData();

            Console.WriteLine($"test case: {testCase.FilePath}");

            int[] actualAnswer;
                        
            try
            {
                Scc(testCase.Input);
                actualAnswer = _answer;
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
                Console.WriteLine(ex.StackTrace);
                return;
            }
        
            if (actualAnswer == null)
            {
                throw new Exception("Couldn't find the answer!");
            }           

            if (testCase.Answer != null)
            {
                if (!testCase.Answer.SequenceEqual(actualAnswer) && testCase.Answer != null)
                {
                    throw new Exception($"Test case {testCase.FilePath} failed!");
                }
                Console.WriteLine(
                    $"Expected: {string.Join(", ", testCase.Answer)}, Actual: {string.Join(", ", actualAnswer)}");
            }
            else
            {
                Console.WriteLine(
                    $"Actual: {string.Join(", ", actualAnswer)}");
            }

            Console.WriteLine("-------------------");
            Console.WriteLine();
        }

        private static void ResetInputData()
        {
            _t = 0;
            _finishingTimes = new Dictionary<int, int>();
            _leaders.Clear();
            _currentLeaderNumber = 0;

            _answer = new int[5];
        }

        private static void Scc(List<Tuple<int, int>> input)
        {
            _convertedInput = PrepareInputForFinishingTimes(input);
            for (int i = 0; i < _convertedInput.Keys.Count; i++)
            {
                if (!_convertedInput.ContainsKey(i + 1))
                {
                    throw new Exception("Обратите внимание!");
                }
            }
            DfsForFinishingTimes();

            Console.WriteLine("\n --- Finishing times done --- \n");
            _convertedInput.Clear();
            _convertedInput = PrepareInputForScc(input);            
            DfsForScc();

            CollectTop5Leaders();
        }

        private static Dictionary<int, NodeInfo> PrepareInputForFinishingTimes(List<Tuple<int, int>> input)
        {
            var convertedInput = input.GroupBy(x => x.Item2, x => x.Item1, (key, values) => new
            {
                I = key,
                DestinationNodes = values.ToArray()
            })
                .OrderBy(x => x.I).ToList();

            var maxItem1 = input.Max(x=>x.Item1);
            var maxItem2 = input.Max(x => x.Item2);
            var maxNodeNumber = Math.Max(maxItem1, maxItem2);

            var count = convertedInput.Count;            
            for (int i = 0; i < count; i++)
            {
                if (convertedInput[i].I != i + 1)
                {
                    convertedInput.Insert(i, new 
                    {
                        I = i + 1,                        
                        DestinationNodes = new int[0]
                    });
                    count++;
                }
            }

            if (maxNodeNumber > count)
            {
                for (int i = count + 1; i <= maxNodeNumber; i++)
                {
                    convertedInput.Add(new
                    {
                        I = i,
                        DestinationNodes = new int[0]
                    });
                }
            }

            return convertedInput.OrderBy(x => x.I)
                .ToDictionary(x => x.I, x => new NodeInfo
                {
                    Explored = false,
                    DestinationNodes = x.DestinationNodes
                });
        }

        private static void CollectTop5Leaders()
        {
            var topLeaders = _leaders.OrderByDescending(x => x.Value.Count).Take(5).ToList();
            for (int i = 0; i < topLeaders.Count; i++)
            {
                _answer[i] = topLeaders[i].Value.Count;
            }
        }

        private static Dictionary<int, NodeInfo> PrepareInputForScc(List<Tuple<int, int>> input)
        {            
            var convertedInput = input.GroupBy(x => x.Item1, x=>x.Item2, (key, values) => new
            {
                I = key,                
                DestinationNodes = values.ToArray()
            })
            .ToList();

            var maxItem1 = input.Max(x => x.Item1);
            var maxItem2 = input.Max(x => x.Item2);
            var maxNodeNumber = Math.Max(maxItem1, maxItem2);

            var count = convertedInput.Count;
            for (int i = 0; i < count; i++)
            {
                if (convertedInput[i].I != i + 1)
                {
                    convertedInput.Insert(i, new
                    {
                        I = i + 1,
                        DestinationNodes = new int[0]
                    });
                    count++;
                }
            }

            if (maxNodeNumber > count)
            {
                for (int i = count + 1; i <= maxNodeNumber; i++)
                {
                    convertedInput.Add(new
                    {
                        I = i,
                        DestinationNodes = new int[0]
                    });
                }
            }

            return convertedInput.OrderBy(x=>x.I)
                .ToDictionary(x => x.I, x => new NodeInfo
            {
                Explored = false,
                DestinationNodes = x.DestinationNodes
            });
        }

        private static void DfsForFinishingTimes()
        {
            _t = 0;
            var keysFromLargestToSmallest = _convertedInput.Keys.OrderByDescending(x => x);
            foreach(var key in keysFromLargestToSmallest) // (var i = _convertedInputMaxReversed; i >= 1; i--)
            {
                if (!_convertedInput[key].Explored)
                {                    
                    DfsReversed(key);
                }
            }
        }

        private static void DfsReversed(int i)
        {
            var node = _convertedInput[i];
            node.Explored = true;

            var destinationNodes = node.DestinationNodes; // _convertedInput.Where(x => x.DestinationNodes.Contains(_currentDfsReversedNumber));
            //Console.WriteLine($"node: {i}, dstNodes: {string.Join(", ", destinationNodes)}");
            foreach (var dstNodeIndex in destinationNodes)
            {
                    var dstNode = _convertedInput[dstNodeIndex]; //_convertedInput[dstNodeIndex.I - 1];
                    if (!dstNode.Explored)
                    {
                        DfsReversed(dstNodeIndex);
                    }
            }
            _t++;            
            _finishingTimes[_t] = i;
            PrintIntermediateResult(_t);
        }

        private static void Dfs(int i)
        {
            var node = _convertedInput[i];
            node.Explored = true;
            if (!_leaders.ContainsKey(_currentLeaderNumber))
            {
                _leaders.Add(_currentLeaderNumber, new List<int>());
            }
            _leaders[_currentLeaderNumber].Add(i);
            foreach (var dstNodeIndex in node.DestinationNodes)
            {
                if (_convertedInput.ContainsKey(dstNodeIndex))
                {
                    var dstNode = _convertedInput[dstNodeIndex];
                    if (!dstNode.Explored)
                    {
                        PrintIntermediateResult(dstNodeIndex);
                        Dfs(dstNodeIndex);
                    }
                }
            }
        }

        private static void DfsForScc()
        {
            _currentLeaderNumber = 0;

            var finishingTimes = _finishingTimes.Keys.OrderByDescending(x => x);
            foreach (var finishingTime in finishingTimes)
            {                
                var i = _finishingTimes[finishingTime];
                if (!_convertedInput[i].Explored)
                {
                    _currentLeaderNumber = i;                    
                    Dfs(i);
                }
            }
        }

        private static void PrintIntermediateResult(int i)
        {
            if (i > 0 && i < 1000 && i % 100 == 0)
            {
                Console.WriteLine(i);
            }
            else if (i >= 1000 && i < 10000 && i % 1000 == 0)
            {
                Console.WriteLine(i);
            }
            else if (i >= 10000 && i % 10000 == 0)
            {
                Console.WriteLine(i);
            }
        }

        private static void ProcessTestCaseText(string text, out List<Tuple<int, int>> input, out int[] answer)
        {
            var lines = text.Split('\n')
                .Where(x => !string.IsNullOrWhiteSpace(x))
                .ToList();

            answer = null;
            input = new List<Tuple<int, int>>();

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

        private static Tuple<int, int> ProcessLine(string line)
        {
            var numbers = line
                .Split(' ')
                .Where(x => !string.IsNullOrWhiteSpace(x))
                .Select(x => int.Parse(x.Trim()))
                .ToList();

            return new Tuple<int, int>(numbers[0], numbers[1]);
        }
    }
}
