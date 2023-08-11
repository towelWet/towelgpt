using towelgpt;

var modelFactory = new towelgptModelFactory();
if (args.Length < 2)
{
    Console.WriteLine($"Usage: towelgpt.Samples <model-path> <prompt>");
    return;
}

var modelPath = args[0];
var prompt = args[1];

using var model = modelFactory.LoadModel(modelPath);

var result = await model.GetStreamingPredictionAsync(
    prompt,
    PredictRequestOptions.Defaults);

await foreach (var token in result.GetPredictionStreamingAsync())
{
    Console.Write(token);
}
