namespace JobScraper.Model;

public class Job(string url)
{
    public string Url { get; set; } = url;
    public string? Title { get; set; } = string.Empty;
    public string? Description { get; set; } = string.Empty;
    public string? Requirements { get; set; } = string.Empty;
    public string? Contact { get; set; } = string.Empty;
    public string? Phone { get; set; } = string.Empty;
    public string? Email { get; set; } = string.Empty;
    public string? Company { get; set; } = string.Empty;
    public string? Location { get; set; } = string.Empty;
    public string? PostedOn { get; set; } = string.Empty;
    public string? Hours { get; set; } = string.Empty;
    public string? Wage { get; set; } = string.Empty;
    public string? Start { get; set; } = string.Empty;
    public string? Duration { get; set; } = string.Empty;
    public string? Apply { get; set; } = string.Empty;
    public string? Deadline { get; set; } = string.Empty;
    public string? Comments { get; set; } = string.Empty;

    public override string ToString()
    {
        var summary = $"Title: {Title}\n";
        if (!string.IsNullOrEmpty(Description)) summary += $"Description: {Description}\n";
        if (!string.IsNullOrEmpty(Requirements)) summary += $"Requirements: {Requirements}\n";
        if (!string.IsNullOrEmpty(Contact)) summary += $"Contact: {Contact}\n";
        if (!string.IsNullOrEmpty(Phone)) summary += $"Phone: {Phone}\n";
        if (!string.IsNullOrEmpty(Email)) summary += $"Email: {Email}\n";
        if (!string.IsNullOrEmpty(Company)) summary += $"Company: {Company}\n";
        if (!string.IsNullOrEmpty(Location)) summary += $"Location: {Location}\n";
        if (!string.IsNullOrEmpty(PostedOn)) summary += $"Posted On: {PostedOn}\n";
        if (!string.IsNullOrEmpty(Hours)) summary += $"Hours: {Hours}\n";
        if (!string.IsNullOrEmpty(Wage)) summary += $"Wage: {Wage}\n";
        if (!string.IsNullOrEmpty(Start)) summary += $"Start: {Start}\n";
        if (!string.IsNullOrEmpty(Duration)) summary += $"Duration: {Duration}\n";
        if (!string.IsNullOrEmpty(Apply)) summary += $"Apply: {Apply}\n";
        if (!string.IsNullOrEmpty(Deadline)) summary += $"Deadline: {Deadline}\n";
        if (!string.IsNullOrEmpty(Comments)) summary += $"Comments: {Comments}\n";
        return summary;
    }
}