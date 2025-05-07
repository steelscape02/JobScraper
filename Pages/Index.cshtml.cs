using System.Text;
using System.Text.Json;
using System.Text.RegularExpressions;
using JobScraper.Model;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace JobScraper.Pages;

public class IndexModel(ILogger<IndexModel> logger) : PageModel
{
    public int MaxValue { get; set; } = 1;

    private readonly ILogger<IndexModel> _logger = logger;

    private readonly List<Job> _jobs = ListScraper.Jobs;

    public required List<Job> Jobs { get; set; } = [];

    private int[] FindAllNumbers(string? input)
    {
        if (string.IsNullOrEmpty(input))
        {
            return [];
        }
        
        // Regular expression to find one or more consecutive digits
        MatchCollection matches = Regex.Matches(input.Replace(",",""), @"\d+"); //remove commas

        // Convert the matched strings to integers and create an array
        return matches.Cast<Match>()
                      .Select(match => int.Parse(match.Value))
                      .ToArray();
    }

    public void OnGet()
    {
        Jobs.Clear();
    }

    public void UpdateMaxValue(string? input)
    {
        if (string.IsNullOrEmpty(input))
        {
            return;
        }
        
        var val = FindAllNumbers(input);
        if (val == null || val.Length == 0)
        {
            return;
        }

        var max = val.Max();
        Console.WriteLine($"Max: {max} - MaxValue: {MaxValue}");
        if(max > MaxValue)
        {
            Console.WriteLine($"New max value: {max}");
            MaxValue = max;
        }
        
    }

    public async Task<IActionResult> OnGetUpdateTable()
    {
        await ListScraper.Scrape();
        Jobs = ListScraper.Jobs;
        foreach (var job in Jobs)
        {
            var nums = FindAllNumbers(job.Wage ?? string.Empty); //TODO: does not work on nums with decimal value
        }
        return new JsonResult(Jobs);
    }
}
