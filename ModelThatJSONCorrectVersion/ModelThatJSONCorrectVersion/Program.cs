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

namespace ModelThatJSONCorrectVersion
{
    class Program
    {
        static void Main(string[] args)
        {
            string fileName = @"C:\Users\supsu\OneDrive\Proj\Data Transfer C#\ModelThatJSONCorrectVersion\ModelThatJSONCorrectVersion\PredatorPopulation.json";
            string jsonText = File.ReadAllText(fileName);

            var data = JsonConvert.DeserializeObject<List<Animal>>(jsonText);// already have the object layout set up and this will assign from json to the pre existing object
            //PopulationModel data = Newtonsoft.Json.JsonConvert.DeserializeObject<PopulationModel>(jsonText);// already have the object layout set up and this will assign from json to the pre existing object

            foreach (var i in data)
            {
                Console.WriteLine(i.isProgenitor);
            }

        }
    }

    
}
