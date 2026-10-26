using System.Windows.Automation;

namespace KeyFlip.App;

/// <summary>
/// Decides whether the focused control may be touched. Fails closed: the answer is "safe" only when
/// the focused element was positively identified and is not a password field.
/// </summary>
internal static class PasswordGuard
{
    private const int TimeoutMs = 400;

    public static async Task<bool> IsSafeToTouchAsync()
    {
        // Classic Win32 edit controls with ES_PASSWORD (cheap, no UI Automation round trip).
        if (WindowInfo.IsPasswordFieldFocused()) return false;

        try
        {
            Task<bool> query = Task.Run(() =>
            {
                AutomationElement? focused = AutomationElement.FocusedElement;
                return focused is not null && !focused.Current.IsPassword;
            });
            Task finished = await Task.WhenAny(query, Task.Delay(TimeoutMs));
            return finished == query && query.Result;
        }
        catch (Exception)
        {
            return false; // cannot tell: leave the field alone
        }
    }
}
