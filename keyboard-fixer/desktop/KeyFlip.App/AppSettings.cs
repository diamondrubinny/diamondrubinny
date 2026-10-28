using System.Text.Json;

namespace KeyFlip.App;

/// <summary>User settings stored in %APPDATA%\KeyFlip\settings.json. Contains no typed text.</summary>
internal sealed class AppSettings
{
    /// <summary>Browsers are skipped by default because the Chrome extension handles them (and password fields there are undetectable).</summary>
    public static readonly string[] BrowserProcesses = { "chrome", "msedge", "firefox", "brave", "opera", "vivaldi" };

    /// <summary>Processes that hold secrets, are terminals, or are remote-control tools.</summary>
    public static readonly string[] DefaultIgnoredProcesses =
    {
        "keepass", "keepassxc", "1password", "bitwarden", "lastpass", "dashlane",
        "windowsterminal", "cmd", "powershell", "pwsh", "conhost", "mintty", "putty",
        "mstsc", "vmconnect", "teamviewer", "anydesk",
        // Code editors and IDEs: identifiers and abbreviations there must not be "corrected".
        "code", "code - insiders", "cursor", "devenv", "rider64", "idea64", "pycharm64", "webstorm64",
        "clion64", "goland64", "phpstorm64", "studio64", "sublime_text", "atom",
    };

    /// <summary>Bumped when the default ignore list grows; older settings files get the new defaults added once.</summary>
    private const int CurrentVersion = 2;

    public int Version { get; set; }

    /// <summary>Window classes where Ctrl+C means "interrupt", so the clipboard path is never used.</summary>
    public static readonly string[] ConsoleWindowClasses =
    {
        "ConsoleWindowClass", "CASCADIA_HOSTING_WINDOW_CLASS", "mintty", "PuTTY", "VirtualConsoleClass",
    };

    public bool Auto { get; set; } = true;

    /// <summary>When true the desktop app also corrects text typed in browsers (use it if the extension is not installed).</summary>
    public bool IncludeBrowsers { get; set; }

    public List<string> IgnoredProcesses { get; set; } = new(DefaultIgnoredProcesses);

    private static string FilePath => Path.Combine(
        Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "KeyFlip", "settings.json");

    public static AppSettings Load()
    {
        try
        {
            if (File.Exists(FilePath))
            {
                AppSettings? loaded = JsonSerializer.Deserialize<AppSettings>(File.ReadAllText(FilePath));
                if (loaded is not null)
                {
                    // Older files listed browsers here; they are governed by IncludeBrowsers now.
                    loaded.IgnoredProcesses.RemoveAll(p => BrowserProcesses.Contains(p, StringComparer.OrdinalIgnoreCase));
                    if (loaded.Version < CurrentVersion)
                    {
                        foreach (string name in DefaultIgnoredProcesses)
                        {
                            if (!loaded.IgnoredProcesses.Contains(name, StringComparer.OrdinalIgnoreCase)) loaded.IgnoredProcesses.Add(name);
                        }
                        loaded.Version = CurrentVersion;
                        loaded.Save();
                    }
                    return loaded;
                }
            }
        }
        catch (Exception)
        {
            // Corrupt settings fall back to defaults.
        }
        return new AppSettings { Version = CurrentVersion };
    }

    public void Save()
    {
        try
        {
            Directory.CreateDirectory(Path.GetDirectoryName(FilePath)!);
            File.WriteAllText(FilePath, JsonSerializer.Serialize(this, new JsonSerializerOptions { WriteIndented = true }));
        }
        catch (Exception)
        {
            // Read-only profile: the setting just won't persist.
        }
    }

    public bool IsProcessIgnored(string? processName)
    {
        if (processName is null) return true; // unknown or elevated: input cannot be injected anyway
        if (BrowserProcesses.Contains(processName, StringComparer.OrdinalIgnoreCase)) return !IncludeBrowsers;
        return IgnoredProcesses.Any(p => string.Equals(p, processName, StringComparison.OrdinalIgnoreCase));
    }
}
