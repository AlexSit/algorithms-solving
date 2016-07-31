using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace Common
{
    public static class Helpers
    {
        public static TestCase[] ReadTestCasesFromInputs(string[] paths)
        {
            var testCases = new TestCase[paths.Length];

            for (int index = 0; index < paths.Length; index++)
            {
                var path = paths[index];
                using (var file = File.OpenText(path))
                {
                    var text = file.ReadToEnd();

                    int[] input;
                    int answer;
                    ProcessTestCaseText(text, out input, out answer);

                    testCases[index] = new TestCase
                    {
                        FilePath = path,
                        Input = input,
                        Answer = answer
                    };
                }
            }
            return testCases;
        }

        private static void ProcessTestCaseText(string text, out int[] input, out int answer)
        {
            var lines = text.Split('\n');

            answer = -1;
            var onlyDataLinesCount = lines.Count(x => !string.IsNullOrWhiteSpace(x) && !x.ToLower().Contains("ans"));
            input = new int[onlyDataLinesCount];

            for (int i = 0; i < lines.Length; i++)
            {
                if (!string.IsNullOrWhiteSpace(lines[i]))
                {

                    if (lines[i].ToLower().Contains("ans"))
                    {
                        answer = int.Parse(lines[i].Split('-')[1].Trim());
                        return;
                    }

                    input[i] = int.Parse(lines[i]);
                }
            }
        }
    }
}

