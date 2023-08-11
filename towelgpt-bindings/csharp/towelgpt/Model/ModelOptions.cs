namespace towelgpt;

public record ModelOptions
{
    public int Threads { get; init; } = 4;

    public ModelType ModelType { get; init; } = ModelType.GPTJ;
}
