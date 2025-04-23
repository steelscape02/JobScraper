using System.Text.RegularExpressions;
using AngleSharp;

namespace JobScraper.Model;

public abstract partial class ListScraper
{
    public static List<Job> Jobs { get; set; } = new List<Job>();
    public static async Task Scrape()
    {
        const string url = "https://www.byui.edu/help-wanted-postings";
        Jobs.Clear();
        await ScrapeAllJobs(Jobs,url);
    }

    private static async Task ScrapeAllJobs(List<Job> jobs, string baseUrl,string ext="")
    {
        
        try
        {
            var config = Configuration.Default.WithDefaultLoader();
            var context = BrowsingContext.New(config);
            var document = await context.OpenAsync(baseUrl + ext);
            // Example: Extract all links from the page
            var links = document.QuerySelectorAll("a");

            foreach (var link in links)
            {
                var href = link.GetAttribute("href");
                var text = link.TextContent;
                if(text.Contains("Get Involved"))
                {
                    if (href != null) await ScrapeJob(jobs, href);
                }
                else if (text.Contains("Next"))
                {
                    if (href != null) await ScrapeAllJobs(jobs, baseUrl,href);
                }
            }
        }
        catch (Exception e)
        {
            Console.WriteLine($"Error: {e.Message}");
        }
    }

    private static async Task ScrapeJob(List<Job> jobs, string url)
    {
        var config = Configuration.Default.WithDefaultLoader();
        var context = BrowsingContext.New(config);
        var document = await context.OpenAsync(url);
        var job = new Job(url);

        job.Url = url;

        var postedDate = document.GetElementsByClassName("ArticlePage-datePublished");
        job.PostedOn = postedDate[0].TextContent;
        var headers = document.GetElementsByClassName("RichTextArticleBody");
        
        
        foreach (var header in headers)
        {
            var title = ExtractTitle(header.TextContent);
            if (title == "Job Title Name") continue;
            job.Title = title;
            job.Description = ExtractDescription(header.TextContent);
            job.Requirements = ExtractRequirements(header.TextContent);
            if(string.IsNullOrEmpty(job.Requirements))
            {
                job.Requirements = ExtractRequirementsAdvanced(header.TextContent);
            }
            job.Contact = ExtractContactName(header.TextContent);
            job.Phone = ExtractPhone(header.TextContent);
            job.Email = ExtractEmail(header.TextContent);
            job.Company = ExtractCompanyName(header.TextContent);
            job.Location = ExtractAddress(header.TextContent);
            if(string.IsNullOrEmpty(job.Location))
            {
                job.Location = ExtractAddressAdvanced(header.TextContent);
            }

            job.Hours = ExtractHours(header.TextContent);
            job.Wage = ExtractWage(header.TextContent);
            if(string.IsNullOrEmpty(job.Wage))
            {
                job.Wage = ExtractWageAdvanced(header.TextContent);
            }
            job.Start = ExtractStart(header.TextContent);
            job.Duration = ExtractDuration(header.TextContent);
            if(string.IsNullOrEmpty(job.Duration))
            {
                job.Duration = ExtractDurationAdvanced(header.TextContent);
            }
            job.Apply = ExtractApply(header.TextContent);
            job.Deadline = ExtractDeadline(header.TextContent);
            job.Comments = ExtractComments(header.TextContent);
            if(string.IsNullOrEmpty(job.Comments))
            {
                job.Comments = ExtractCommentsAdvanced(header.TextContent);
            }
            jobs.Add(job);
        }
        
    }

    private static string? ExtractContactName(string input)
    {
        var regex = ContactRegex();
        var match = regex.Match(input);
        
        return match.Success ? match.Value.Trim() : null;
    }

    private static string? ExtractCompanyName(string input)
    {
        var regex = CompanyRegex();
        var match = regex.Match(input);
        
        return match.Success ? match.Value.Trim() : null;
    }

    private static string ExtractPhone(string input)
    {
        var regex = PhoneRegex();
        var match = regex.Match(input);
        
        return match.Success ? match.Value.Trim() : string.Empty;
    }

    private static string ExtractAddress(string input)
    {
        var regex = AddressRegex();
        var match = regex.Match(input);

        if (!match.Success) return string.Empty;
        var value = match.Value.Trim();
        var index = value.IndexOf(", City, State", StringComparison.Ordinal);
        return index >= 0 ? value.Remove(index) : match.Value.Trim();
    }

    private static string ExtractAddressAdvanced(string input)
    {
        var regex = AdvancedAddressRegex();
        var match = regex.Match(input);
        
        return match.Success ? match.Value.Trim() : string.Empty;
    }

    private static string ExtractEmail(string input)
    {
        var regex = EmailRegex();
        var match = regex.Match(input);
        
        return match.Success ? match.Value.Trim() : string.Empty;
    }
    
    private static string ExtractTitle(string input)
    {
        var regex = TitleRegex();
        var match = regex.Match(input);
        
        return match.Success ? match.Value.Trim() : string.Empty;
    }
    
    private static string ExtractDescription(string input)
    {
        var regex = DescriptionRegex();
        var match = regex.Match(input);
        
        return match.Success ? match.Value.Trim() : string.Empty;
    }
    
    private static string ExtractRequirements(string input)
    {
        var regex = RequirementsRegex();
        var match = regex.Match(input);
        
        return match.Success ? match.Value.Trim() : string.Empty;
    }

    private static string ExtractRequirementsAdvanced(string input)
    {
        var regex = AdvancedRequirementsRegex();
        var match = regex.Match(input);
        
        return match.Success ? match.Value.Trim() : string.Empty;
    }
    
    private static string ExtractStart(string input)
    {
        var regex = StartRegex();
        var match = regex.Match(input);
        
        return match.Success ? match.Value.Trim() : string.Empty;
    }

    private static string ExtractDuration(string input)
    {
        var regex = DurationRegex();
        var match = regex.Match(input);
        
        return match.Success ? match.Value.Trim() : string.Empty;
    }
    
    private static string ExtractDurationAdvanced(string input)
    {
        var regex = AdvancedDurationRegex();
        var match = regex.Match(input);
        
        return match.Success ? match.Value.Trim() : string.Empty;
    }

    private static string ExtractHours(string input)
    {
        var regex = HoursRegex();
        var match = regex.Match(input);
        
        return match.Success ? match.Value.Trim() : string.Empty;
    }
    
    private static string ExtractWage(string input)
    {
        var regex = WageRegex();
        var match = regex.Match(input);
        
        return match.Success ? match.Value.Trim() : string.Empty;
    }
    
    private static string ExtractWageAdvanced(string input)
    {
        var regex = AdvancedWageRegex();
        var match = regex.Match(input);
        
        return match.Success ? match.Value.Trim() : string.Empty;
    }

    private static string ExtractApply(string input)
    {
        var regex = ApplyRegex();
        var match = regex.Match(input);
        
        return match.Success ? match.Value.Trim() : string.Empty;
    }
    
    private static string ExtractDeadline(string input)
    {
        var regex = DeadlineRegex();
        var match = regex.Match(input);
        
        return match.Success ? match.Value.Trim() : string.Empty;
    }
    
    private static string ExtractComments(string input)
    {
        var regex = CommentsRegex();
        var match = regex.Match(input);
        
        return match.Success ? match.Value.Trim() : string.Empty;
    }

    private static string ExtractCommentsAdvanced(string input)
    {
        var regex = AdvancedCommentsRegex();
        var match = regex.Match(input);
        
        return match.Success ? match.Value.Trim() : string.Empty;
    }

    [GeneratedRegex(@"(?<=Contact Name\s*)([\s\S]*?)(?=\s*Company)")]
    private static partial Regex ContactRegex();
    
    [GeneratedRegex(@"(?<=Company\s*)([\s\S]*?)(?=\s*Contact Phone Number)")]
    private static partial Regex CompanyRegex();
    
    [GeneratedRegex(@"(?<=Contact Phone Number\s*)([\s\S]*?)(?=\s*Address)")]
    private static partial Regex PhoneRegex();
    
    [GeneratedRegex(@"(?<=Address\s*)(.*)(?=\s*Email Address)")]
    private static partial Regex AddressRegex();

    [GeneratedRegex(@"(?<=Address, City, State\s*)(.*)(?=\s*Email Address)")]
    private static partial Regex AdvancedAddressRegex();
    
    [GeneratedRegex(@"(?<=Email Address\s*)([\s\S]*?)(?=\s*Job Title)")]
    private static partial Regex EmailRegex();
    
    [GeneratedRegex(@"(?<=Job Title\s*)([\s\S]*?)(?=\s*Job Description)")]
    private static partial Regex TitleRegex();
    
    [GeneratedRegex(@"(?<=Job Description\s*)([\s\S]*?)(?=\s*Requirements)")]
    private static partial Regex DescriptionRegex();
    
    [GeneratedRegex(@"(?<=Requirements/Qualifications\s*)(.*)(?=\s*Start Date)")]
    private static partial Regex RequirementsRegex();

    [GeneratedRegex(@"(?<=Requirements / Qualifications\s*)(.*)(?=\s*Start Date)")]
    private static partial Regex AdvancedRequirementsRegex();
    
    [GeneratedRegex(@"(?<=Start Date\s*)([\s\S]*?)(?=\s*Duration)")]
    private static partial Regex StartRegex();
    
    [GeneratedRegex(@"(?<=Duration/End Date\s*)([\s\S]*?)(?=\s*Hours)")]
    private static partial Regex DurationRegex();

    [GeneratedRegex(@"(?<=Duration / End Date\s*)([\s\S]*?)(?=\s*Hours)")]
    private static partial Regex AdvancedDurationRegex();
    
    [GeneratedRegex(@"(?<=Hours\s*)([\s\S]*?)(?=\s*Pay)")]
    private static partial Regex HoursRegex();
    
    [GeneratedRegex(@"(?<=Pay/Wage\s*)([\s\S]*?)(?=\s*How to Apply)")]
    private static partial Regex WageRegex();

    [GeneratedRegex(@"(?<=Pay / Wage\s*)([\s\S]*?)(?=\s*How to Apply)")]
    private static partial Regex AdvancedWageRegex();
    
    [GeneratedRegex(@"(?<=How to Apply\s*)([\s\S]*?)(?=\s*Application Deadline)")]
    private static partial Regex ApplyRegex();
    
    [GeneratedRegex(@"(?<=Application Deadline:\s*)([\s\S]*?)(?=\s*Other Questions)")]
    private static partial Regex DeadlineRegex();
    
    [GeneratedRegex(@"(?<=Other Questions/Comments:\s*)([\s\S]*)$")]
    private static partial Regex CommentsRegex();

    [GeneratedRegex(@"(?<=Other Questions / Comments:\s*)([\s\S]*)$")]
    private static partial Regex AdvancedCommentsRegex();

}