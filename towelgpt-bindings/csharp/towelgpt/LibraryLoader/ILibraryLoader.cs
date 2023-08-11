namespace towelgpt.LibraryLoader;

public interface ILibraryLoader
{
    LoadResult OpenLibrary(string? fileName);
}
