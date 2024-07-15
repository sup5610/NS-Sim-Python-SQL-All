using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
using Newtonsoft.Json.Serialization;
using Newtonsoft.Json.Converters;
using Newtonsoft.Json.Linq;
using System.IO;

namespace ModelThatJSON
{
    class Program
    {
        static void Main(string[] args)
        {
            string fileName = @"C:\Users\supsu\OneDrive\School Python\Project\Data Transfer\ModelThatJSON\ModelThatJSON\sample.json";
            //Console.WriteLine(fileName);

            string jsonText = File.ReadAllText(fileName);
            //Console.WriteLine(jsonText);

            var data = Newtonsoft.Json.JsonConvert.DeserializeObject<MyModel>(jsonText);// already have the object layout set up and this will assign from json to the pre existing object
            //Console.WriteLine(data);
        }
    }
}
