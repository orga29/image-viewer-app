using System;
using System.Diagnostics;
using System.IO;

class Program {
    static void Main(string[] args) {
        try {
            string baseDir = AppDomain.CurrentDomain.BaseDirectory;
            string pythonwPath = @"d:\NextCloud\AI-workroom\.venv\Scripts\pythonw.exe";
            if (!File.Exists(pythonwPath)) {
                pythonwPath = Path.GetFullPath(Path.Combine(baseDir, @"..\..\.venv\Scripts\pythonw.exe"));
            }
            string mainPyPath = Path.Combine(baseDir, "main.py");

            ProcessStartInfo psi = new ProcessStartInfo();
            psi.FileName = pythonwPath;
            string fileArg = args.Length > 0 ? "\"" + args[0] + "\"" : "";
            psi.Arguments = "\"" + mainPyPath + "\" " + fileArg;
            psi.UseShellExecute = false;
            psi.CreateNoWindow = true;

            Process.Start(psi);
        } catch (Exception) {
        }
    }
}
