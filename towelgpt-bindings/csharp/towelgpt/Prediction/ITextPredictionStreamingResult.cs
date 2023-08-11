namespace towelgpt;

public interface ITextPredictionStreamingResult : ITextPredictionResult
{
    IAsyncEnumerable<string> GetPredictionStreamingAsync(CancellationToken cancellationToken = default);
}
