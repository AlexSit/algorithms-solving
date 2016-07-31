using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;
using Common;

namespace KargerContractionMincut
{
    class Program
    {
        static void Main(string[] args)
        {
            var paths = new List<string>
            {
                //"tc1.txt",
                //"tc2.txt",
                //"tc3.txt",
                //"tc4.txt",
                //"tc5.txt",
                //"tc6.txt"
                "kargerMinCut.txt"
            };

            var testCases = new List<TestCase>();

            foreach (var path in paths)
            {                
                using (var file = File.OpenText(path))
                {
                    var text = file.ReadToEnd();

                    Dictionary<int, List<int>> input;
                    int answer;
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
            Console.WriteLine($"test case: {testCase.FilePath}");

            //TODO ASIT do it multiple times
            long actualAnswer = -1;

            // let's take number of times to run algorithm such that
            // probability that all runs will fail equals to (1/n) which is pretty good

            // as theory says the number of times needed is n^2*ln(n)

            var originalInput = testCase.Input;
            var timesToRun = Math.Ceiling(Math.Pow(originalInput.Count, 2)*Math.Log(originalInput.Count));

            for (int i = 0; i <= timesToRun; i++)
            {
                var randomForPointNumber = new Random(DateTime.Now.Millisecond + 643423);
                var randomForAdjacent = new Random(DateTime.Now.Millisecond - 213423);

                //var log = "";
                try
                {
                    var inputCopy = CopyOriginalInput(originalInput);
                    var minCutCrossEdgesCount = ContractionMincut(inputCopy, randomForPointNumber, randomForAdjacent/*, ref log*/);
                    if (minCutCrossEdgesCount < actualAnswer || actualAnswer == -1)
                    {
                        actualAnswer = minCutCrossEdgesCount;
                    }
                }
                catch (Exception ex)
                {                    
                    return;
                }
            }

            if (actualAnswer == -1)
            {
                throw new Exception("Couldn't find minimum cut!");
            }

            Console.WriteLine($"Expected: {testCase.Answer}, Actual: {actualAnswer}");
            if (testCase.Answer != actualAnswer && testCase.Answer != -1)
            {
                throw new Exception($"Test case {testCase.FilePath} failed!");
            }
            Console.WriteLine("-------------------");
            Console.WriteLine();
        }

        private static Dictionary<int, List<int>> CopyOriginalInput(Dictionary<int, List<int>> originalInput)
        {
            var result = new Dictionary<int, List<int>>();

            foreach (var pair in originalInput)
            {
                var clonedValues = new List<int>();
                foreach (var val in pair.Value)
                {
                    clonedValues.Add(val);
                }
                result.Add(pair.Key, clonedValues);
            }

            return result;
        }

        private static int ContractionMincut(Dictionary<int, List<int>> input, Random randomForPointNumber, Random randomForAdjacent/*, ref string log*/)
        {
            ContractRandomEdge(input, randomForPointNumber, randomForAdjacent/*, ref log*/);
            
            if (input.Count == 2)
            {
                // check that both points have same adjacents count
                if (input.ElementAt(0).Value.Count != input.ElementAt(1).Value.Count)
                    throw new Exception("Different amout of edges");

                return input.ElementAt(0).Value.Count;
            }

            return ContractionMincut(input, randomForPointNumber, randomForAdjacent/*, ref log*/);
        }        

        private static void ContractRandomEdge(Dictionary<int, List<int>> input, Random randomForPointNumber, Random randomForAdjacent/*, ref string log*/)
        {
            try
            {
                var pointsCount = input.Count;
                var randomPointNumberPosition = randomForPointNumber.Next(0, pointsCount - 1);

                var randomPointNumber = input.ToList().ElementAt(randomPointNumberPosition).Key;
                var adjacents = input[randomPointNumber];
                var adjacentsCount = adjacents.Count;

                // choose point to delete of contracted edge   

                var randomAdjacent = adjacents[randomForAdjacent.Next(0, adjacentsCount - 1)];
#if DEBUG
                //var inputFormatted = string.Join("\n", input.Select(x => $"{x.Key} {string.Join(" ", x.Value)}"));
                //log += $"input:\n {inputFormatted}\n ({randomPointNumber}, {randomAdjacent}) \n";
#endif
                // retrieve the adjacents of the record of point that corresponds to to randomAdjacent
                var deletedPointAdjacents = input[randomAdjacent];

                // delete record
                input.Remove(randomAdjacent);

                // add adjacents of the deleted point (except randomPointNumber) to randomPointNumber
                input[randomPointNumber].AddRange(deletedPointAdjacents.Where(x => x != randomPointNumber));

                // iterate over adjacents of the deleted point (record) and exclude deleted point from their adjacents lists
                foreach (var deletedPointAdjacent in deletedPointAdjacents)
                {
                    input[deletedPointAdjacent].Remove(randomAdjacent);
                    if (deletedPointAdjacent != randomPointNumber)
                    {
                        input[deletedPointAdjacent].Add(randomPointNumber);
                    }
                }
            }
            catch (Exception ex)
            {
                //Console.WriteLine($"Error occured: {ex.Message}, Stack: {ex.StackTrace}");
                //Console.WriteLine($"Log: {log}");
                //Console.ReadKey();
                throw;
            }
        }

        private static void ProcessTestCaseText(string text, out Dictionary<int, List<int>> input, out int answer)
        {
            var lines = text.Split('\n')
                .Where(x => !string.IsNullOrWhiteSpace(x))
                .ToList();

            answer = -1;
            input = new Dictionary<int, List<int>>();

            for (int i = 0; i < lines.Count; i++)
            {                
                if (lines[i].ToLower().Contains("ans"))
                {
                    answer = int.Parse(lines[i].Split('-')[1].Trim());
                    return;
                }
                                
                var pointNumberAndAdjacents = ProcessLine(lines[i]);
                input.Add(pointNumberAndAdjacents.Key, pointNumberAndAdjacents.Value);
            }
        }

        private static KeyValuePair<int, List<int>> ProcessLine(string line)
        {            
            var numbers = line
                .Split('\t')
                .Where(x => !string.IsNullOrWhiteSpace(x))
                .Select(x => int.Parse(x.Trim()))
                .ToList();
                        
            var adjacentsList = numbers.GetRange(1, numbers.Count - 1).ToList();            
            return new KeyValuePair<int, List<int>>(numbers[0], adjacentsList);
        }
    }
}
